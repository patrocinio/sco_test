import time

INSTANCE_NAME="WinguInstance"
PATTERN_NAME="WinguPattern"
PROFILE_NAME="My Environment Profile"
CLOUD_NAME="RegionOne_nova"
IP_GROUP_NAME="RegionOne_public_10.20.0.0/24"
PART_LABEL="RHEL63"
PASSWORD="password"

#def search_object(list, expression):
#  for object in list:
#    if object.name == expression:
#      return object
#  return None


def get_pattern():
  patterns = deployer.patterns[PATTERN_NAME]
  return patterns[0] if patterns else None

def get_profile():
  return deployer.environmentprofiles[PROFILE_NAME][0]

def get_cloud():
  return deployer.clouds[CLOUD_NAME][0]

def get_ip_group():
  return deployer.ipgroups[IP_GROUP_NAME][0]

def get_instance():
  instances = deployer.virtualsystems[INSTANCE_NAME]
  return instances[0] if instances else None

def get_flavor(cloud):
  return cloud.flavors["m1.tiny"][0]

def get_part():
  return deployer.parts[PART_LABEL][0]


def wait_for_instance():
  instance = get_instance()
  while instance.currentstatus != 'RM01006':
    print "status:", instance.currentstatus_text
    time.sleep(1)
    instance = get_instance()
  return instance

def wait_for_instance_deleted():
  instance = get_instance()
  while instance != None:
    time.sleep(1)
    instance = get_instance()

def delete_instance(instance):
  print "Deleting the instance"
  instance.delete(ignoreErrors=True, deleteRecord=True)
  wait_for_instance_deleted ()

def deploy_instance():
  print "Deploying instance"

  ### Delete the instance
  instance = get_instance()
  if instance != None:
    delete_instance(instance)

  ### Create the instance
  pattern = get_pattern()
  print "Pattern: ", pattern.name

  profile = get_profile()
  print "Profile: ", profile.name
  
  cloud = get_cloud()
  print "Cloud: ", cloud.name
  
  ipgroup = get_ip_group()
  print "IP Group: ", ipgroup.name
  
  flavor = get_flavor(cloud)
  print "Flavor: ", flavor.name
  
  deployer.virtualsystems.create(
    {'name': INSTANCE_NAME, 
     'environmentprofile': profile, 
     'pattern': pattern, 
     'part-1.cloud': cloud, 
     'part-1.vm-1.nic-1.ipgroup': ipgroup,
     'part-1.OpenStackConfig.flavorid': flavor.id,
     'part-1.ConfigPWD_ROOT.password': PASSWORD})
  
  instance = wait_for_instance()
  
  ### Delete the instance
  delete_instance(instance)

def delete_pattern(pattern):
  print "Deleting pattern"
  pattern.delete()

def create_part():
  part = get_part()
  if part == None:
    print "Creating part"
    part = deployer.parts.create({"label": PART_LABEL})
  return part

def create_pattern():
  pattern = get_pattern()
  if pattern != None:
    delete_pattern(pattern)
  print "Creating pattern"
  pattern = deployer.patterns.create({"name": PATTERN_NAME})
  part = create_part()
  pattern.parts.create(part.id)
  return pattern
  
print "Welcome to SCO testing!"
pattern = create_pattern()
deploy_instance()
delete_pattern(pattern)
print "Congratulations!! Test completed successfully"



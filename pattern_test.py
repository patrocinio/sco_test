import time

INSTANCE_NAME="WinguInstance"
PATTERN_NAME="WinguPattern"
PROFILE_NAME="VmwareDev03_EP"
CLOUD_NAME="VmwareDev03_nova_vmware"
IP_GROUP_NAME="VmwareDev03_public_130.9.218.0/23"
PART_LABEL="rhel6template_mope_ae"
PASSWORD="password"

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
  parts = deployer.parts[PART_LABEL]
  if len(parts) == 0:
     return None
  return parts[0]


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



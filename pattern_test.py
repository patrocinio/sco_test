import time

INSTANCE_NAME="MyInstance2"
PATTERN_NAME="test"
PROFILE_NAME="My Environment Profile"
CLOUD_NAME="RegionOne_nova"
IP_GROUP_NAME="RegionOne_public_10.20.0.0/24"

#def search_object(list, expression):
#  for object in list:
#    if object.name == expression:
#      return object
#  return None


def get_pattern():
  return deployer.patterns.list({'name': PATTERN_NAME})[0]

def get_profile():
  return deployer.environmentprofiles.list({'name': PROFILE_NAME})[0]

def get_cloud():
  return deployer.clouds.list({'name': CLOUD_NAME})[0]

def get_ip_group():
  return deployer.ipgroups.list({'name': IP_GROUP_NAME})[0]

def get_instance():
  instances = deployer.virtualsystems.list({'name': INSTANCE_NAME})
  if instances:
    return instances[0]
  return None
  

def wait_for_instance():
  instance = get_instance()
  while True:
    print "status:", instance.currentstatus
    time.sleep(1)
    instance = get_instance()

def wait_for_instance_deleted():
  instance = get_instance()
  while instance != None:
    time.sleep(1)
    instance = get_instance()

print "Welcome to SCO testing!"

### Delete the instance
instance = get_instance()
if instance != None:
  print "Deleting the instance"
  instance.delete(ignoreErrors=True, deleteRecord=True)
  wait_for_instance_deleted ()

### Create the instance

pattern = get_pattern()
print "Pattern: ", pattern.name

profile = get_profile()
print "Profile: ", profile.name

cloud = get_cloud()
print "Cloud: ", cloud.name

ipgroup = get_ip_group()
print "IP Group: ", ipgroup.name

response = deployer.virtualsystems.create(
  {'name': INSTANCE_NAME, 
   'environmentprofile': profile, 
   'pattern': pattern, 
   'part-1.cloud': cloud, 
   'part-1.vm-1.nic-1.ipgroup': ipgroup})

wait_for_instance()



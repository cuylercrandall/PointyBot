import urllib2
import json
import time

startTime = time.time()

while time.time()-startTime < 15:
  req = urllib2.Request("http://api.open-notify.org/iss-now.json")
  response = urllib2.urlopen(req)
  obj = json.loads(response.read())
  
  if obj['message'] == "success":
    print obj['timestamp']
    print obj['iss_position']['latitude'], obj['iss_position']['longitude']
  else:
    print "Failed to get ISS position"
  time.sleep(1)
#print obj['iss_position']['latitude'], obj['data']['iss_position']['latitude']

# Example prints:
#   1364795862
#   -47.36999493 151.738540034
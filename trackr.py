#!/usr/bin/python

import requests

restbase="https://phonehalocloud.appspot.com/rest/"

class Trackr:
    def getToken(self,user,password):
        params={"email":user, "password":password}
        r = requests.get(restbase + "user", params = params)
        return r.json()["usertoken"]
    def getFeatureVersion(self,token):
        params = {"usertoken":token}
        r = requests.get(restbase + "user/featureversion", params = params)
        return r.content
    def getUsersInRadius(self, lat, lon):
        data = {
            "searchLocation" : {
                "latitude": lat,
                "longitude": lon                                    
            }
        }
        r = requests.put(restbase + "tracker/radius", json=data)
        return r.content
    def getTracker(self,token,itemid):
        params = {"usertoken":token}    
        r = requests.get(restbase + "tracker/secure/%s" % itemid, params=params)
        return r.json()
    def getTrackers(self,token):
        params = {"usertoken":token}
        r = requests.get(restbase + "item", params=params)
        return r.json()
    def getTrackerByName(self, token, name):
        trackers=self.getTrackers(token)
        for tracker in trackers:
            if tracker['customName'] == name:
                return tracker
        return None
    def createItemWithTracker(self, token, customName, typ, trackerId, icon, timeElapsedSync):
        params = {"usertoken":token}
        data = {"customName":customName, "type":typ, "trackerId":trackerId, "icon":icon, "timeElapsedSync":timeElapsedSync}
        r = requests.post(restbase + "item", params=params, json=data)
        return r.content
    def updateTracker(self, trackerId, battery, lat,lon,connected, timeDiff ): 
        data = [{
            "trackerId":trackerId,
            "battery":battery,
            "lastKnownLocation": {
                "longitude": lon,
                "latitude": lat
            },
            "connected": connected,
            "clientTimeDiff":timeDiff
            }]
        r = requests.put(restbase + "tracker/batch/secure/$2a$10$Rif.csF02tlXv5OVOBiWauXpGN6lrdWIc5A9cr2V7yCVIhIHt0.SG" , json=data)
        return r.json()
    def deleteTrackr(self, token, itemid, deltasync):
        params = {"usertoken":token, "timeElapsedSync":deltasync}
        r = requests.delete(restbase + "item/%s" % itemid, params=params)
        return r.content




if __name__ == "__main__":
    import sys
    import pprint

    if len(sys.argv) > 1:
        lat = float(sys.argv[1])
    else:
        lat = 59.44586

    if len(sys.argv) > 2:
        lon=float(sys.argv[2])
    else:
        lon = 18.134482

    if len(sys.argv) > 3:
        user=sys.argv[3]
    else:
        print "Trackr username: ",
        user=sys.stdin.readline().rstrip("\n")
        print "\r",
        
    if len(sys.argv) > 4:
        password=sys.argv[4]
    else:
        print "Trackr password: ",
        password=sys.stdin.readline().rstrip("\n")
        print "\r",
    
    pp=pprint.PrettyPrinter(indent=4)
    t = Trackr()

    try: token
    except NameError:
        print "Getting token for " + user
        token = t.getToken(user, password)
    print("Got Token:" + token)


    print("FeatureVersion: %s" % t.getFeatureVersion(token))
    print("UsersInRadius:  %s" % t.getUsersInRadius(lat, lon))

    tracker = t.getTrackerByName(token, "TestTracker")
    if False:
        if tracker:
            print("Deleting tracker")
            t.deleteTrackr(token, tracker['trackerId'], 0)
            tracker = None

    if not tracker:
        print("Creating tracker")
        ttid = t.createItemWithTracker(token, "TestTracker", "Bluetooth",
                                       "00000042-00000001", "trackr", 0)
    else:
        ttid = tracker['trackerId']

    print "Updating tracker %s" % ttid
    print(t.updateTracker(ttid, 99, 58.51234, 13.51234, False, 1))


    print("Tracker %s: " % ttid);
    pp.pprint(t.getTracker(token, ttid))
    trackers=t.getTrackers(token)
    print("Trackers:")
    pp.pprint(trackers)




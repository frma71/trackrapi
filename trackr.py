#!/usr/bin/python3

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
        return r.json()
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
        r = requests.get(restbase + "tracker/secure/{}".format(itemid), params=params)
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
        r = requests.delete(restbase + "item/{}".format(itemid), params=params)
        return r.content





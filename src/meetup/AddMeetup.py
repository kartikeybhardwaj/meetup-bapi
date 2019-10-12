import json
from bson.objectid import ObjectId

from utils.Utils import Utils
from database.user.UserDb import UserDb
from database.meetup.MeetupDb import MeetupDb

class AddMeetup:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__meetup = {
            "title": "",
            "description": "",
            "location": {
                "title": "",
                "country": "",
                "latitude": "",
                "longitude": ""
            },
            "timeline": {
                "from": "",
                "to": ""
            },
            "isPrivate": False,
            "joinedBy": [],
            "metadata": {
                "createdBy": "",
                "createdOn": ""
            }
        }

    def validateTitle(self):
        return True if self.__meetup["title"] else False
    
    def validateDescription(self):
        return True if self.__meetup["description"] else False
    
    def validateTimeline(self):
        return True if self.__meetup["timeline"]["from"] and self.__meetup["timeline"]["to"] else False

    def on_post(self, req, resp):
        reqData = req.media
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        utils = Utils()
        self.__meetup["title"] = reqData.get("title", "")
        self.__meetup["description"] = reqData.get("description", "")
        self.__meetup["location"]["title"] = reqData.get("location", "").get("title", "")
        self.__meetup["location"]["country"] = reqData.get("location", "").get("country", "")
        self.__meetup["location"]["latitude"] = reqData.get("location", "").get("latitude", "")
        self.__meetup["location"]["longitude"] = reqData.get("location", "").get("longitude", "")
        self.__meetup["timeline"]["from"] = utils.getDateFromUTCString(reqData.get("timeline", "").get("from", ""))
        self.__meetup["timeline"]["to"] = utils.getDateFromUTCString(reqData.get("timeline", "").get("to", ""))
        self.__meetup["isPrivate"] = reqData.get("isPrivate", False)
        self.__meetup["joinedBy"] = []
        self.__meetup["metadata"]["createdBy"] = ObjectId(req.params["userId"])
        self.__meetup["metadata"]["createdOn"] = utils.getDateFromUTCString(reqData.get("metadata", "").get("createdOn", ""))
        try:
            # validate required data
            if self.validateTitle() and self.validateDescription() and self.validateTimeline():
                if "_id" in self.__meetup:
                    del self.__meetup["_id"]
                meetupdb = MeetupDb()
                # insert meetup
                meetupId = meetupdb.insertMeetup(self.__meetup)
                # add user as joining user
                meetupdb.registerToMeetup(req.params["userId"], meetupId)
                userdb = UserDb()
                # add to created meetups by user
                userdb.addToCreatedMeetups(req.params["userId"], meetupId)
                # add to joined meetups by user
                userdb.addToJoinedMeetups(req.params["userId"], meetupId)
                # get this meetup data
                responseObj["returnData"] = meetupdb.findOneMeetup(meetupId)
                responseObj["responseId"] = 211
            else:
                responseObj["responseId"] = 111
                responseObj["message"] = "check if all the fields are valid"
        except Exception as ex:
            print(ex)
            responseObj["responseId"] = 111
            responseObj["message"] = "some error occurred"
        resp.body = json.dumps(responseObj)

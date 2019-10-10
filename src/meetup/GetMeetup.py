import json
from bson.objectid import ObjectId

from src.meetupdb.MeetupDb import MeetupDb

class GetMeetup:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__id = ""
    
    def validateId(self):
        success = False
        try:
            ObjectId(self.__id)
            success = True
        except Exception as ex:
            pass
        return success

    def on_post(self, req, resp):
        reqData = req.media
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        self.__id = reqData.get("_id", "")
        try:
            # validate id
            if (self.validateId()):
                meetupdb = MeetupDb()
                # get this meetup data
                meetup = meetupdb.findOneMeetup(self.__id)
                if meetup:
                    responseObj["returnData"] = meetup
                    responseObj["responseId"] = 211
                else:
                    responseObj["responseId"] = 111
                    responseObj["message"] = "this meetup does not exists"
            else:
                responseObj["responseId"] = 111
                responseObj["message"] = "this meetup does not exists"
        except Exception as ex:
            responseObj["responseId"] = 111
            responseObj["message"] = "some error occurred"
        resp.body = json.dumps(responseObj)
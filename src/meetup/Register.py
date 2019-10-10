import json
from bson.objectid import ObjectId

from database.user.UserDb import UserDb
from database.meetup.MeetupDb import MeetupDb

class Register:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__meetupId = ''

    def validateId(self):
        success = False
        try:
            ObjectId(self.__meetupId)
            success = True
        except Exception as ex:
            pass
        return success
    
    def on_post(self, req, resp):
        reqData = req.media
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        self.__meetupId = reqData.get("meetupId", "")
        try:
            # validate required data
            if self.validateId():
                meetupdb = MeetupDb()
                # add user in meetup
                if meetupdb.registerToMeetup(req.params["userId"], self.__meetupId):
                    userdb = UserDb()
                    # add meetup in user
                    userdb.addToJoinedMeetups(req.params["userId"], self.__meetupId)
                    responseObj["responseId"] = 211
                else:
                    responseObj["responseId"] = 111
                    responseObj["message"] = "this meetup does not exists"
            else:
                responseObj["responseId"] = 111
                responseObj["message"] = "this meetup does not exists"
        except Exception as ex:
            print(ex)
            responseObj["responseId"] = 111
        responseObj["message"] = "some error occurred"
        resp.body = json.dumps(responseObj)
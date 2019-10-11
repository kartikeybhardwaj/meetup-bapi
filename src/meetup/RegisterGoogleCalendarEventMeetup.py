import json

from database.meetup.MeetupDb import MeetupDb

class RegisterGoogleCalendarEventMeetup:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__meetupId = ''
        self.__userId = ''
        self.__htmlLink = ''
    
    def on_post(self, req, resp):
        reqData = req.media
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        self.__meetupId = reqData.get("meetupId", "")
        self.__userId = req.params["userId"]
        self.__htmlLink = reqData.get("htmlLink", "")
        try:
            meetupdb = MeetupDb()
            # add user in meetup
            if meetupdb.googleCalendarToMeetup(self.__userId, self.__meetupId, self.__htmlLink):
                responseObj["responseId"] = 211
            else:
                responseObj["responseId"] = 111
                responseObj["message"] = "this meetup does not exists"
        except Exception as ex:
            responseObj["responseId"] = 111
            responseObj["message"] = "some error occurred"
        resp.body = json.dumps(responseObj)
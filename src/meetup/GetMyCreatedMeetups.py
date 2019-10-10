import json

from database.meetup.MeetupDb import MeetupDb

class GetMyCreatedMeetups:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_get(self, req, resp):
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        meetupdb = MeetupDb()
        # get meetups data
        responseObj["returnData"] = meetupdb.findMyCreatedMeetups(req.params["userId"])
        responseObj["responseId"] = 211
        resp.body = json.dumps(responseObj)

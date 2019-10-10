from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import datetime

class MeetupDb:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__client = MongoClient('mongodb://kart:oon@127.0.0.1:27017/meetup')
        self.__db = self.__client.meetup

    def findOneMeetup(self, _id: str) -> dict:
        result = self.__db.meetups.find_one({
                "_id": ObjectId(_id)
            })
        return json.loads(dumps(result))

    def insertMeetup(self, meetup: str) -> str:
        _id = self.__db.meetups.insert_one(meetup).inserted_id
        return str(_id)

    def registerToMeetup(self, userId: str, meetupId: str) -> bool:
        return self.__db.meetups.update_one({
            "_id": ObjectId(meetupId)
        }, {
            "$push": {
                "joinedBy": ObjectId(userId)
            }
        }).modified_count == 1

    def findUpcomingMeetups(self):
        result = self.__db.meetups.find({
            "timeline.from": {
                "$gt": datetime.datetime.utcnow()
            },
            "isPrivate": False
        })
        return json.loads(dumps(result))

    def findLiveMeetups(self):
        result = self.__db.meetups.find({
            "timeline.from": {
                "$lt": datetime.datetime.utcnow()
            },
            "timeline.to": {
                "$gt": datetime.datetime.utcnow()
            },
            "isPrivate": False
        })
        return json.loads(dumps(result))

    def findPreviousMeetups(self):
        result = self.__db.meetups.find({
            "timeline.to": {
                "$lt": datetime.datetime.utcnow()
            },
            "isPrivate": False
        }).sort("timeline.to", DESCENDING)
        return json.loads(dumps(result))

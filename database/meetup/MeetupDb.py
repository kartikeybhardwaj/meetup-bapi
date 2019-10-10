from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import json

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

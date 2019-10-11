from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
import datetime

class UserDb:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__client = MongoClient('mongodb://kart:oon@127.0.0.1:27017/meetup')
        self.__db = self.__client.meetup

    def checkUserExistence(self, username="", email="") -> bool:
        isAlreadyExisting = False
        if username and email:
            isAlreadyExisting = self.__db.users.find({
                "$or": [{
                        "username": username
                    }, {
                        "email": email
                    }]}).count() > 0
        elif username:
            isAlreadyExisting = self.__db.users.find({
                        "username": username
                    }).count() > 0
        return isAlreadyExisting

    def findOneUser(self, username="", email="") -> dict:
        result = {}
        if username and email:
            result = self.__db.users.find_one({
                "$or": [{
                    "username": username
                }, {
                    "email": email
                }]})
        elif username:
            result = self.__db.users.find_one({
                    "username": username
                })
        return json.loads(dumps(result))

    def insertUser(self, username: str, password: str, email: str) -> str:
        _id = self.__db.users.insert_one({
            "username": username,
            "password": password,
            "displayname": username,
            "email": email,
            "emailMeta": {
                "isVerifiedEmail": False,
                "verifiedOn": None
            },
            "mobile": "",
            "mobileMeta": {
                "isVerifiedMobile": False,
                "verifiedOn": None
            },
            "createdMeetups": [],
            "joinedMeetups": [],
            "metadata": {
                "signupOn": datetime.datetime.utcnow()
            }
        }).inserted_id
        return str(_id)

    def addToCreatedMeetups(self, userId: str, meetupId: str) -> bool:
        return self.__db.users.update_one({
            "_id": ObjectId(userId)
        }, {
            "$addToSet": {
                "createdMeetups": {
                    "meetupId": ObjectId(meetupId)
                }
            }
        }).modified_count == 1

    def addToJoinedMeetups(self, userId: str, meetupId: str) -> bool:
        return self.__db.users.update_one({
            "_id": ObjectId(userId)
        }, {
            "$push": {
                "joinedMeetups": {
                    "meetupId": ObjectId(meetupId)
                }
            }
        }).modified_count == 1

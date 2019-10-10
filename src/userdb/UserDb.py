from pymongo import MongoClient
from bson.json_util import dumps
import json

class UserDb:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__client = MongoClient('mongodb://kart:oon@127.0.0.1:27017/meetup')
        self.__db = self.__client.meetup

    def checkUserExistence(self, username="", email=""):
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

    def findOneUser(self, username="", email=""):
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

    def insertUser(self, username, password, email):
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
            "joinedMeetups": []
        }).inserted_id
        return str(_id)

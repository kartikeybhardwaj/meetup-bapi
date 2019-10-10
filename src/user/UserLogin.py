import json

from database.user.UserDb import UserDb
from utils.Crypto import Crypto

class UserLogin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__username = ''
        self.__password = ''
        self.__encodedNumber = ''

    def on_post(self, req, resp):
        reqData = req.media
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        self.__username = reqData.get("username", "")
        self.__password = reqData.get("password", "")
        self.__encodedNumber = reqData.get("number", "")
        try:
            # validate required data
            if self.__username and self.__password:
                userdb = UserDb()
                # get user from db
                user = userdb.findOneUser(self.__username)
                # check if password matches
                if self.__password == Crypto(user["password"] + str(self.__encodedNumber)).SHA256():
                    # delete password key
                    del user["password"]
                    responseObj["returnData"] = user
                    responseObj["responseId"] = 211
                else:
                    responseObj["message"] = "invalid username or password"
                    responseObj["responseId"] = 111
            else:
                responseObj["responseId"] = 111
                responseObj["message"] = "check if all the fields are valid"
        except Exception as ex:
                responseObj["responseId"] = 111
                responseObj["message"] = "some error occurred"
        resp.body = json.dumps(responseObj)

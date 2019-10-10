import json, re

from database.user.UserDb import UserDb

class UserSignup:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__username = ''
        self.__email = ''
        self.__password = ''

    def validateUsername(self):
        success = False
        len_username = len(self.__username)
        if len_username >= 4 and len_username <= 12:
            success = True
        return success

    def validateEmail(self):
        success = False
        if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', self.__email):
            success = True
        return success

    def validatePassword(self):
        success = False
        len_password = len(self.__password)
        if len_password >= 4:
            success = True
        return success

    def on_post(self, req, resp):
        reqData = req.media
        responseObj = {}
        responseObj["message"] = ""
        responseObj["returnData"] = ""
        self.__username = reqData.get("username", "")
        self.__email = reqData.get("email", "")
        self.__password = reqData.get("password", "")
        try:
            # validate required data
            if self.validateUsername() and self.validateEmail() and self.validatePassword():
                userdb = UserDb()
                # check if user already exists
                if userdb.checkUserExistence(self.__username, self.__email):
                    responseObj["responseId"] = 111
                    responseObj["message"] = "username or email already exists"
                else:
                    # insert user
                    userdb.insertUser(self.__username, self.__password, self.__email)
                    # get this user data
                    responseObj["returnData"] = userdb.findOneUser(self.__username, self.__email)
                    responseObj["responseId"] = 211
            else:
                responseObj["responseId"] = 111
                responseObj["message"] = "check if all the fields are valid"
        except Exception as ex:
                responseObj["responseId"] = 111
                responseObj["message"] = "some error occurred"
        resp.body = json.dumps(responseObj)

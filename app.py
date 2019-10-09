import falcon
from falcon_cors import CORS

from middleware.AuthMiddleware import AuthMiddleware
from src.user.UserSignup import UserSignup
from src.user.UserLogin import UserLogin
from utils.Empty import Empty

cors = CORS(allow_origins_list = ['http://localhost:4200'],
            allow_all_headers = True,
            allow_all_methods = True)

api = falcon.API(middleware = [
    cors.middleware,
    AuthMiddleware()
])
api.add_route('/signup', UserSignup())
api.add_route('/login', UserLogin())
api.add_route('/fast-forward', Empty())

# pip3 install falcon
# pip3 install falcon-cors
# pip3 install pymongo
# pip3 install pyjwt
# pip3 install gunicorn
# gunicorn -b localhost:3200 app:api --reload

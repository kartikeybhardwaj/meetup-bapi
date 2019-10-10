import falcon
from falcon_cors import CORS

from middleware.AuthMiddleware import AuthMiddleware
from src.user.UserSignup import UserSignup
from src.user.UserLogin import UserLogin
from src.meetup.AddMeetup import AddMeetup
from src.meetup.GetMeetup import GetMeetup
from src.meetup.Register import Register
from src.meetup.GetLiveMeetups import GetLiveMeetups
from src.meetup.GetUpcomingMeetups import GetUpcomingMeetups
from src.meetup.GetPreviousMeetups import GetPreviousMeetups
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
api.add_route('/add-meetup', AddMeetup())
api.add_route('/get-meetup', GetMeetup())
api.add_route('/register-to-meetup', Register())
api.add_route('/get-live-meetups', GetLiveMeetups())
api.add_route('/get-upcoming-meetups', GetUpcomingMeetups())
api.add_route('/get-previous-meetups', GetPreviousMeetups())

# pip3 install falcon
# pip3 install falcon-cors
# pip3 install pymongo
# pip3 install pyjwt
# pip3 install gunicorn
# gunicorn -b localhost:3200 app:api --reload

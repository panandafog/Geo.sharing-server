from .users import HelloApi, SaveGeoApi, UserRegisterApi, LocationSaveApi
from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(HelloApi, '/')
    api.add_resource(SaveGeoApi, '/save_geo')
    api.add_resource(UserRegisterApi, '/user/register')
    api.add_resource(LocationSaveApi, '/location/save')
    api.add_resource(SignupApi, '/user/signup')
    api.add_resource(LoginApi, '/user/login')

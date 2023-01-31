from .users import HelloApi, SaveGeoApi, UserRegisterApi, LocationSaveApi, SearchUserApi
from .auth import SignupApi, LoginApi
from .friendship import CreateFriendshipRequestApi, DeleteFriendshipRequestApi, AcceptFriendshipRequestApi, \
    RejectFriendshipRequestApi, GetIncomingFriendshipRequests, GetOutgoingFriendshipRequests
from .friends import GetFriends, DeleteFriend

def initialize_routes(api):
    api.add_resource(HelloApi, '/')
    api.add_resource(SaveGeoApi, '/save_geo')
    api.add_resource(UserRegisterApi, '/user/register')
    api.add_resource(LocationSaveApi, '/location/save')
    api.add_resource(SignupApi, '/user/signup')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(SearchUserApi, '/user/search')

    api.add_resource(CreateFriendshipRequestApi, '/friendship/create_request')
    api.add_resource(DeleteFriendshipRequestApi, '/friendship/delete_request')
    api.add_resource(AcceptFriendshipRequestApi, '/friendship/accept_request')
    api.add_resource(RejectFriendshipRequestApi, '/friendship/reject_request')
    api.add_resource(GetIncomingFriendshipRequests, '/friendship/get_incoming_requests')
    api.add_resource(GetOutgoingFriendshipRequests, '/friendship/get_outgoing_requests')

    api.add_resource(GetFriends, '/friends/get')
    api.add_resource(DeleteFriend, '/friends/delete')

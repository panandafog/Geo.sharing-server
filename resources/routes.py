from .users import HelloApi, SaveGeoApi, LocationSaveApi, SearchUserApi, ProfilePictureApi, \
    RequestPasswordChangeApi, ChangePasswordApi
from .auth import SignupApi, LoginApi, ConfirmEmailApi, RefreshTokenApi
from .friendship import CreateFriendshipRequestApi, DeleteFriendshipRequestApi, AcceptFriendshipRequestApi, \
    RejectFriendshipRequestApi, GetIncomingFriendshipRequests, GetOutgoingFriendshipRequests
from .friends import GetFriends, DeleteFriend

def initialize_routes(api):
    api.add_resource(HelloApi, '/')
    api.add_resource(SaveGeoApi, '/save_geo')
    api.add_resource(LocationSaveApi, '/location/save')
    api.add_resource(SignupApi, '/user/signup')
    api.add_resource(RefreshTokenApi, '/user/refresh_token')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(ConfirmEmailApi, '/user/confirm_email')
    api.add_resource(SearchUserApi, '/user/search')
    api.add_resource(ProfilePictureApi, '/user/profile_picture')
    api.add_resource(RequestPasswordChangeApi, '/user/request_password_change')
    api.add_resource(ChangePasswordApi, '/user/change_password')

    api.add_resource(CreateFriendshipRequestApi, '/friendship/create_request')
    api.add_resource(DeleteFriendshipRequestApi, '/friendship/delete_request')
    api.add_resource(AcceptFriendshipRequestApi, '/friendship/accept_request')
    api.add_resource(RejectFriendshipRequestApi, '/friendship/reject_request')
    api.add_resource(GetIncomingFriendshipRequests, '/friendship/get_incoming_requests')
    api.add_resource(GetOutgoingFriendshipRequests, '/friendship/get_outgoing_requests')

    api.add_resource(GetFriends, '/friends/get')
    api.add_resource(DeleteFriend, '/friends/delete')

from .views import *
from django.urls import path

urlpatterns = [
    path('api/signup/', SignupView.as_view()),
    path('api/set-password/<int:user_id>/', SetPasswordView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/send/friend-request/', SendFriendRequestView.as_view()),
    path('api/update/friend-request/', ModifyRequestStatusView.as_view()),
    path('api/user-list/', UserListView.as_view()),
    path('api/user/friend-list/<int:user_id>/', UserFriendList.as_view()),
    path('api/user/pending-request/<int:user_id>/', UserPendingRequestView.as_view())
]
from django.urls import path

from users.views import UserCreateView, UsersListView

urlpatterns = [
    path('', UserCreateView.as_view(), name='users_create'),
    path('all/', UsersListView.as_view(), name='users_list_all'),
]

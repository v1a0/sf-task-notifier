from django.urls import path

from messaging.views import MessagingEventCreateView

urlpatterns = [
    path('', MessagingEventCreateView.as_view(), name='messaging_event_create'),
    # path('all/', AddresseesListView.as_view(), name='users_list_all'),
]

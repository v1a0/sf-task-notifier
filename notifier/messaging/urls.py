from django.urls import path

from messaging.views import MessagingEventCreateView, MessagingEventListView, MessagingEventRetrieveUpdateDestroyView

urlpatterns = [
    path('', MessagingEventCreateView.as_view(), name='messaging_event_create'),
    path('<int:pk>/', MessagingEventRetrieveUpdateDestroyView.as_view(), name='messaging_event_rud'),
    path('all/', MessagingEventListView.as_view(), name='users_list_all'),
]

from django.urls import path

from messaging.views import MessagingEventCreateView, MessagingEventListView, MessagingEventRetrieveUpdateDestroyView, \
    MessagingEventStatisticRetrieveView

urlpatterns = [
    path('', MessagingEventCreateView.as_view(), name='messaging_event_create'),
    path('<int:pk>/', MessagingEventRetrieveUpdateDestroyView.as_view(), name='messaging_event_rud'),
    path('<int:pk>/statistic', MessagingEventStatisticRetrieveView.as_view(), name='messaging_event_statistic'),
    path('all/', MessagingEventListView.as_view(), name='users_list_all'),
]

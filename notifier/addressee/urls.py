from django.urls import path

from addressee.views import AddresseeCreateView, AddresseesListView

urlpatterns = [
    path('', AddresseeCreateView.as_view(), name='users_create'),
    path('all/', AddresseesListView.as_view(), name='users_list_all'),
]

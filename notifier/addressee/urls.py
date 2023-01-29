from django.urls import path

from addressee.views import AddresseeCreateView, AddresseesListView, AddresseeRetrieveUpdateDestroyView

urlpatterns = [
    path('', AddresseeCreateView.as_view(), name='users_create'),
    path('<int:pk>/', AddresseeRetrieveUpdateDestroyView.as_view(), name='users_rud'),
    path('all/', AddresseesListView.as_view(), name='users_list_all'),
]

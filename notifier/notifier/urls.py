from django.urls import path, include
from django.urls import path
from django.conf import settings

urlpatterns = [
    # API
    path('api/addressees/', include('addressee.urls')),
    path('api/messaging/', include('messaging.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('docs/', include('api_doc.urls')),
    ]

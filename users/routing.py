from django.urls import path
from users.consumer import machineConsumer
from users.views import *
from django.views.generic import RedirectView

ws_urls = [
    path("machine-side",machineConsumer.as_asgi()),
]


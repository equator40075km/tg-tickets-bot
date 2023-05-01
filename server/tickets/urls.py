from django.urls import path

from .views import TicketsAPIView, TGAdminsAPIView

urlpatterns = [
    path('tickets/', TicketsAPIView.as_view()),
    path('tg-admins/', TGAdminsAPIView.as_view())
]

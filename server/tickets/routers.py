from rest_framework import routers
from .views import TicketViewSet, TGAdminViewSet, TGUserViewSet


ticket_router = routers.DefaultRouter()
ticket_router.register(r'', TicketViewSet, basename='tickets')


tg_admin_router = routers.DefaultRouter()
tg_admin_router.register(r'', TGAdminViewSet)


tg_user_router = routers.DefaultRouter()
tg_user_router.register(r'', TGUserViewSet)

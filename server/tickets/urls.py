from django.urls import path, include

from . import routers
from .views import OverdueTicketsAPIView, InactiveTGUsersAPIView


urlpatterns = [
    path('tickets/', include(routers.ticket_router.urls)),
    path('tickets/overdue', OverdueTicketsAPIView.as_view()),
    path('tg-admins/', include(routers.tg_admin_router.urls)),
    path('tg-users/', include(routers.tg_user_router.urls)),
    path('tg-users/inactive', InactiveTGUsersAPIView.as_view()),
]

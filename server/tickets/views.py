from rest_framework import viewsets, views
from datetime import date, datetime, timedelta
from rest_framework.response import Response

from .models import Ticket, TGAdmin, TGUser
from .serializers import TicketsSerializer, TGAdminSerializer, TGUserSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketsSerializer

    def get_queryset(self):
        if self.request.method == 'GET' and \
                'city' in self.request.data and \
                'date_since' in self.request.data and \
                'date_until' in self.request.data:
            return Ticket.objects.filter(
                city=self.request.data['city'],
                date__gte=date.fromisoformat(self.request.data['date_since']),
                date__lte=date.fromisoformat(self.request.data['date_until'])
            ).order_by('date')

        return Ticket.objects.all()


class OverdueTicketsAPIView(views.APIView):
    def delete(self, request):
        result = Ticket.objects.filter(date__lte=date.today()).delete()
        return Response({'count': result[0]})


class TGAdminViewSet(viewsets.ModelViewSet):
    serializer_class = TGAdminSerializer
    queryset = TGAdmin.objects.all()


class TGUserViewSet(viewsets.ModelViewSet):
    serializer_class = TGUserSerializer
    queryset = TGUser.objects.all()


class InactiveTGUsersAPIView(views.APIView):
    def delete(self, request):
        inactive_date: datetime = datetime.today() - timedelta(days=7)
        result = TGUser.objects.filter(last_action__lt=inactive_date.date()).delete()
        return Response({'count': result[0]})

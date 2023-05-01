from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date
from .models import Ticket, TGAdmin


class TicketsAPIView(APIView):
    def get(self, request):
        try:
            year = int(request.query_params.get('year', None))
            month = int(request.query_params.get('month', None))
            since = int(request.query_params.get('since', None))
            until = int(request.query_params.get('until', None))
        except Exception:
            return Response(status=400)

        date_since: date = date(year, month, since)
        date_until: date = date(year, month, until)

        tickets = Ticket.objects.filter(date__gte=date_since, date__lte=date_until).order_by('date')
        return Response({'tickets': list(tickets.values())})

    def post(self, request):
        try:
            new_ticket = Ticket.objects.create(
                title=request.data['title'],
                link=request.data['link'],
                text=request.data['text'],
                img_url=request.data['img_url'],
                date=request.data['date']
            )
        except Exception as e:
            print(e)
            return Response(status=500)

        return Response({'post': model_to_dict(new_ticket)})


class TGAdminsAPIView(APIView):
    def get(self, request):
        tg_admins = TGAdmin.objects.all()
        return Response({'tg_admins': list(tg_admins.values())})

    def post(self, request):
        try:
            new_tg_admin = TGAdmin.objects.create(
                user_id=request.data['user_id'],
                name=request.data['name'],
                can_appoint=request.data['can_appoint']
            )
        except Exception as e:
            print(e)
            return Response(status=500)

        return Response({'post': model_to_dict(new_tg_admin)})

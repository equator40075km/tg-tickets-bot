from rest_framework import serializers
from .models import Ticket, TGAdmin, TGUser


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TGAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TGAdmin
        fields = '__all__'


class TGUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TGUser
        fields = '__all__'

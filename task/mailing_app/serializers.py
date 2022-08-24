from rest_framework import serializers
from .models import Client, MailingList, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['phone', 'operator_code', 'tag', 'time_zone']


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ['start_date', 'text', 'filter', 'end_date']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['create_date', 'status', 'mailing_list', 'client']

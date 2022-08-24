import time
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer

from .models import Client, MailingList, Message


@api_view(['POST'])
def create_client(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        client_serializer = ClientSerializer(data=data)
        if client_serializer.is_valid():
            client_serializer.save()
            return JsonResponse(client_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def change_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except:
        JsonResponse({'message': 'The client does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        client_serializer = ClientSerializer(client, data=data)
        if client_serializer.is_valid():
            client_serializer.save()
            return JsonResponse(client_serializer.data)
        return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        client.delete()
        return JsonResponse({'message': 'The client deleted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_mailing(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        mailing_serializer = MailingSerializer(data=data)
        if mailing_serializer.is_valid():
            mailing_serializer.save()
            return JsonResponse(mailing_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(mailing_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def change_mailing(request, pk):
    try:
        mailing = MailingList.objects.get(pk=pk)
    except:
        JsonResponse({'message': 'The mailing does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        mailing_serializer = MailingSerializer(mailing, data=data)
        if mailing_serializer.is_valid():
            mailing_serializer.save()
            return JsonResponse(mailing_serializer.data)
        return JsonResponse(mailing_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        mailing.delete()
        return JsonResponse({'message': 'The client deleted'}, status=status.HTTP_200_OK)


class MailingListView(generics.ListAPIView):
    serializer_class = MailingSerializer

    def get_queryset(self):
        queryset = MailingList.objects.all()
        return queryset


class MessagesDetailView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.request.GET['pk']
        queryset = Message.objects.all().filter(mailing_list_id=pk)
        return queryset


def start_sending(request):
    url = 'https://probe.fbrq.cloud/v1/send/{msgID}'
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTI4ODc2NjIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IlNhcmdpc0FuZHJlYXN5YW4ifQ.xu0pcaHnY-6Xc72E6sthS4ko96fNa7fHuLRCXW5oZPk"
    while True:
        messages = Message.objects.all()
        for message in messages:
            if message.mailing_list.start_date < datetime.now().date() and message.mailing_list.start_date > datetime.now().date():
                try:
                    request.POST(url=url, data={"id": message.client.pk,
                                                "phone": message.client.phone,
                                                "text": message.mailing_list.text},
                                 headers={"Authorization": f"Bearer {token}"})
                except:
                    print('error!')
        time.sleep(60 * 60 * 24)

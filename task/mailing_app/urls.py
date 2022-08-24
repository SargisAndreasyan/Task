from django.urls import include, path
from .api import create_client, change_client, change_mailing, create_mailing,MailingListView,MessagesDetailView,start_sending

urlpatterns = [
    path('client', create_client, name='client'),
    path('client/<int:pk>', change_client, name='change_client'),
    path('mailing', create_mailing, name='mailing'),
    path('mailing/<int:pk>', change_mailing, name='change_mailing'),
    path('mailing_list',MailingListView.as_view(),name='mailing_list_view'),
    path('message_detail',MessagesDetailView.as_view(),name='message_details'),
    path('start_sending',start_sending)
]

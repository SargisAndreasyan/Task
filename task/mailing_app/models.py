from django.db import models


class MailingList(models.Model):
    start_date = models.DateField()
    text = models.TextField()
    filter = models.CharField(max_length=20)
    end_date = models.DateField()


class Client(models.Model):
    phone = models.CharField(max_length=11)
    operator_code = models.CharField(max_length=15)
    tag = models.CharField(max_length=10)
    time_zone = models.CharField(max_length=15)


class Message(models.Model):
    create_date = models.DateField()
    status = models.BooleanField(default=False)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

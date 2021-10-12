from django.db import models


class TelChannel(models.Model):
    tel_index = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=30)
    channel_url = models.CharField(max_length=100)
    risk = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tel_channel'


class TelChat(models.Model):
    chat_index = models.BigAutoField(primary_key=True)
    tel_index = models.ForeignKey(TelChannel, models.DO_NOTHING, db_column='tel_index')
    user_name = models.CharField(max_length=30)
    tel_message = models.CharField(max_length=300)
    date = models.DateField(db_column='DATE', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tel_chat'
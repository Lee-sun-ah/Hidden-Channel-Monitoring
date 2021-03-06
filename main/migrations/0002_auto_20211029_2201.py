# Generated by Django 3.2.8 on 2021-10-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelChannel',
            fields=[
                ('tel_index', models.AutoField(primary_key=True, serialize=False)),
                ('channel_name', models.CharField(max_length=30)),
                ('channel_url', models.CharField(max_length=100)),
                ('risk', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tel_channel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TelChat',
            fields=[
                ('chat_index', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30)),
                ('tel_message', models.CharField(max_length=300)),
                ('date', models.DateField(blank=True, db_column='DATE', null=True)),
                ('time', models.TimeField(blank=True, db_column='TIME', null=True)),
            ],
            options={
                'db_table': 'tel_chat',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.DeleteModel(
            name='First',
        ),
    ]

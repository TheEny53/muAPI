# Generated by Django 2.2 on 2019-06-04 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20190604_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

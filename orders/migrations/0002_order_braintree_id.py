# Generated by Django 4.1.2 on 2022-10-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="braintree_id",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]

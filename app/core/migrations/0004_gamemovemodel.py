# Generated by Django 3.2.18 on 2023-03-02 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20230302_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameMoveModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.gamemodel')),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.numbermodel')),
            ],
        ),
    ]
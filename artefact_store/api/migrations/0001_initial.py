# Generated by Django 3.2.7 on 2021-09-05 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtefactSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Artefact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.JSONField()),
                ('schema', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artefacts', to='api.artefactschema')),
            ],
        ),
    ]

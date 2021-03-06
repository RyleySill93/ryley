# Generated by Django 2.0.6 on 2019-11-19 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal_balance', models.CharField(choices=[('DEBIT', 'DEBIT'), ('CREDIT', 'CREDIT')], default='DEBIT', max_length=10000)),
                ('name', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JournalLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=22)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meow.Account')),
                ('journal_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meow.JournalEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10000, null=True)),
                ('left', models.IntegerField()),
                ('right', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NodeFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='node_family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meow.NodeFamily'),
        ),
        migrations.AddField(
            model_name='account',
            name='node',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='meow.Node'),
        ),
    ]

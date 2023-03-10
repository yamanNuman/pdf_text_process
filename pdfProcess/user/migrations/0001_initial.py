# Generated by Django 4.0 on 2021-12-11 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfLoad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdPdf', models.FileField(upload_to='', verbose_name='PDF Ekle')),
                ('createdDatwe', models.DateField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Öğretim Elemanı')),
            ],
        ),
        migrations.CreateModel(
            name='DataPdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.TextField(verbose_name='Üniversite')),
                ('faculty', models.TextField(verbose_name='Fakülte')),
                ('department', models.TextField(verbose_name='Bölüm')),
                ('lecture', models.TextField(verbose_name='Ders')),
                ('projectTitle', models.TextField(verbose_name='Proje Başlığı')),
                ('studentInfo', models.TextField(verbose_name='Öğrenci Bilgileri')),
                ('superVisor', models.TextField(verbose_name='Danışman Bilgileri')),
                ('jury1', models.TextField(verbose_name='1. Juri Bilgileri')),
                ('jury2', models.TextField(verbose_name='2. Juri Bilgileri')),
                ('presentationDate', models.TextField(verbose_name='Savunma Dönemi')),
                ('abstract', models.TextField(verbose_name='Özet')),
                ('keyWords', models.TextField(verbose_name='Anahtar Kelimeler')),
                ('pdfFile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.pdfload', verbose_name='Eklenen PDF')),
            ],
        ),
    ]

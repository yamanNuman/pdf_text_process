from django.db import models

# Create your models here.

class PdfLoad(models.Model):
    lecturer = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Öğretim Elemanı")
    createdPdf = models.FileField(verbose_name="PDF Ekle")
    createdDate = models.DateField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    def __str__(self):
        return str(self.lecturer)


class DataPdf(models.Model):
    pdfFile = models.ForeignKey(PdfLoad, on_delete=models.CASCADE, verbose_name="Eklenen PDF")
    okul = models.TextField(verbose_name="Okul", null=True)
    lecture = models.TextField(verbose_name="Ders")
    projectTitle = models.TextField(verbose_name="Proje Başlığı")
    studentInfo = models.TextField(verbose_name="Öğrenci Bilgileri")
    superVisor = models.TextField(verbose_name="Danışman Bilgileri")
    juries = models.TextField(verbose_name="Juri Bilgileri", null=True)
    presentationDate = models.TextField(verbose_name="Savunma Dönemi")
    abstract = models.TextField(verbose_name="Özet")
    keyWords = models.TextField(verbose_name="Anahtar Kelimeler")




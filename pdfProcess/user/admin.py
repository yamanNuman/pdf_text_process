from django.contrib import admin
import django.db
from .models import PdfLoad, DataPdf

# Register your models here.

@admin.register(PdfLoad)
class PDFLoadAdmin(admin.ModelAdmin):
    
    list_display = ['lecturer', 'createdDate', 'createdPdf']
    list_filter = ['lecturer', 'createdDate']
    search_fields = ['lecturer', 'createdDate']
    
    class Meta:
        model = PdfLoad

@admin.register(DataPdf)
class DataPdfAdmin(admin.ModelAdmin):

    list_display = ['pdfFile', 'projectTitle', 'presentationDate', 'studentInfo']
    search_fields = ['presentationDate','studentInfo','lecture','projectTitle','keyWords']
    list_filter = ['pdfFile','presentationDate','studentInfo','lecture','projectTitle','keyWords']
    class Meta:
        model = DataPdf

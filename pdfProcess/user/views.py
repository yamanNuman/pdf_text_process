from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PdfLoadForm
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re
from .models import DataPdf 
from .models import PdfLoad
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url="loginUser")
def dashBoard(request):
    pdfLoads = PdfLoad.objects.filter(lecturer= request.user)
    ids    = pdfLoads.values_list('id', flat=True)
    dataPdfs = DataPdf.objects.filter(pdfFile_id__in = ids) 
    
    context = {"dataPdfs": dataPdfs, "pdfLoads": pdfLoads}
    return render(request, "dashBoard.html", context)

@login_required(login_url="loginUser")
def addPDF(request):
    form = PdfLoadForm(request.POST or None, request.FILES or None) 
    dataPdf = DataPdf()
    ozetSayfaStr = request.POST.get("ozet")
    
    if form.is_valid():
        if ozetSayfaStr:
            pdfUpload = form.save(commit=False)
            pdfUpload.lecturer = request.user
            pdfUpload.save()
            file = request.FILES['createdPdf']   
            ozetSayfa = int(ozetSayfaStr)    
            pdfVerileri = pdfHandler("media/{0}".format(pdfUpload.createdPdf),ozetSayfa)
            dataPdf.pdfFile_id = pdfUpload.id
            dataPdf.okul = pdfVerileri["okul"]
            dataPdf.lecture = pdfVerileri["ders"]
            dataPdf.projectTitle = pdfVerileri["projeAdi"]
            dataPdf.studentInfo = pdfVerileri["isim"]
            dataPdf.superVisor = pdfVerileri["danisman"]
            dataPdf.juries = pdfVerileri["juri"]
            dataPdf.presentationDate = pdfVerileri["donem"]
            dataPdf.abstract = pdfVerileri["ozet"]
            dataPdf.keyWords = pdfVerileri["anahtar"]
            dataPdf.save()
            messages.success(request, "Pdf eklendi. Analiz başarılı şekilde yapıldı.")
            return redirect("dashBoard")
        else:
            messages.warning(request, "Dosya seçilmedi yada özetin sayfası girilmedi")
            return redirect("addPdf")

    context = {"form":form}
    return render(request, "addPdf.html", context)

def pdfHandler(pdfAdres, ozetSayfa):

    output_string = StringIO()

    with open(pdfAdres, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams(boxes_flow=None))
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        for pageNumber, page in enumerate(PDFPage.create_pages(doc)):
            if pageNumber != 0:
                interpreter.process_page(page)
            
                if pageNumber == ozetSayfa-1: #kullanıcıdan özetin olduğu sayfa alınmalı ve 1 eksiği olmalı
                    break


    context = splitEmptyLines(output_string.getvalue())

    context = list(filter(str.strip, context)) #boşlukları sil
    clearContext = []


    for i in context:
        i= re.sub(r'[\x0c]', '', i)
        clearContext.append(i.rstrip().lower())


    onsozIndex = clearContext.index('İÇİNDEKİLER'.lower())
    ozetIndex = clearContext.index('Özet'.lower()) 

    del clearContext[onsozIndex:ozetIndex]
    isim = []
    sonIsimIndex = 0
    okul = []
    ozetIndex = -1
    anahtarKelimelerIndex = -1
    anahtarKelimeler = []
    donem = []
    danisman = ""
    juriler = []
    for i in clearContext:
        
        if "adısoyadı" in i.replace(" ",""):
            sep = i.index(":")
            isim.append(i[sep+1:].strip()) 
        if "üni̇versi̇tesi̇" in i:
            okul.insert(0,i)
        if "fakültesi" in i:
            okul.insert(2,i)
        if "bölümü" in i:
            okul.insert(4,i)
        if "öğrencino" in i.replace(" ",""):
            sep = i.index(":")
            isim.append(i[sep+1:].strip())
            if (i[sep+1:].strip()[3:6]) == "201":
                isim.append("normal öğretim")
            if (i[sep+1:].strip()[3:6]) == "202":
                isim.append("ikinci öğretim")

        if "anahtarkelimeler" in i.replace(" ",""):        
            anahtarKelimelerIndex = clearContext.index(i)                     
        if "özet" == i:      
            ozetIndex = clearContext.index(i)
        if "tezinsavunulduğutarih" in i.replace(" ",""):
            sep = i.index(":")
            tarih = i[sep+1:].strip()       
            donem.append(tarih[6:10])

            if 1 < int(tarih[3:5]) and int(tarih[3:5]) < 7:
                donem.append("Bahar")

            if 13 > int(tarih[3:5]) and int(tarih[3:5]) > 6 or int(tarih[3:5]) ==1 :
                donem.append("Güz")
        
        if "danışman," in i.replace(" ",""):
            danisman = clearContext[clearContext.index(i)-1]
            juriler.append(clearContext[clearContext.index(i)+2])
            juriler.append(clearContext[clearContext.index(i)+5])
            sonIsimIndex = clearContext.index(clearContext[clearContext.index(i)-2])
            
        
    for i in clearContext[anahtarKelimelerIndex:]:
        if i.endswith(".") or i.endswith(","):
            anahtarKelimeler.append(i)

    isimElemanSayisi = int(len(isim)/2)-1
    dersAdi = clearContext[3]
    ozetText = clearContext[ozetIndex+1:anahtarKelimelerIndex]
    projeAdi = clearContext[4:(sonIsimIndex-isimElemanSayisi)]
    okulBilgileri = listToString(okul)
    isimBilgileri = listToString(isim)
    anahtarKelimelerBilgisi = listToString(anahtarKelimeler)
    ozetBilgisi = listToString(ozetText)
    projeAdiBilgisi = listToString(projeAdi)
    donemBilgisi = listToString(donem)
    juriBilgisi = listToString(juriler)

    tumBilgiler = {"okul":okulBilgileri, 
                "isim":isimBilgileri, 
                "anahtar": anahtarKelimelerBilgisi,
                "donem": donemBilgisi,
                "juri": juriBilgisi,
                "ders": dersAdi,
                "ozet": ozetBilgisi,
                "projeAdi": projeAdiBilgisi,
                "danisman": danisman
                 }
    return tumBilgiler
     
def listToString(s): 
    
    str1 = " "   
    return (str1.join(s))

def splitEmptyLines(outputString):

    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){1,}"
        
    return re.split(blank_line_regex, outputString.strip())

@login_required(login_url="loginUser")
def searchData(request):
    
    radioCheck = request.POST.get("flexRadioDefault")
    pdfLoads = PdfLoad.objects.filter(lecturer= request.user)
    ids    = pdfLoads.values_list('id', flat=True)
    ara = request.POST.get("aramaYap")

    if ara != "":
        messages.success(request, "Arama başarılı. Sonuçlar listelendi.")
        if radioCheck == "1":
            donem = request.POST.get("aramaYap2")
            dataPdfs = DataPdf.objects.filter(Q(pdfFile_id__in = ids) & Q(lecture__contains=ara) & Q(presentationDate__contains=donem))
            
            context = {"dataPdfs":dataPdfs}       
            return render(request, "dashBoard.html", context)

        if radioCheck == "2":
            
            dataPdfs = DataPdf.objects.filter(Q(pdfFile_id__in = ids) 
                                                & (
                                                Q(projectTitle__contains=ara) 
                                                | Q(studentInfo__contains=ara)
                                                | Q(superVisor__contains=ara)
                                                | Q(juries__contains=ara)
                                                | Q(abstract__contains=ara)
                                                | Q(keyWords__contains=ara)
                                                | Q(okul__contains=ara)
                                                ))
            context = {"dataPdfs":dataPdfs}       
            return render(request, "dashBoard.html", context)
    else:
        messages.warning(request, "Arama kelimesi girilmedi.")
        return redirect("dashBoard")

@login_required(login_url="loginUser")
def details(request, id):
    pdfData = DataPdf.objects.filter(id = id)
    pdfID = 0
    for i in pdfData:
        pdfID = i.pdfFile_id
    pdfLoad = PdfLoad.objects.filter(id = pdfID)
    print(pdfID)
    context = {"pdfData": pdfData, "pdfLoad":pdfLoad}
    return render (request, "details.html", context)

@login_required(login_url="loginUser")
def deletePdf(request, id):
    pdfLoad = PdfLoad.objects.filter(id = id)
    pdfLoad.delete()
    messages.success(request, "Silme işlemi başarılı")
    return redirect("dashBoard")

def loginUser(request):
    usr = request.POST.get("usr")
    pwd = request.POST.get("pwd")
    user = authenticate(username = usr, password=pwd)
    if user is None:     
        return render(request, "loginUser.html")
    
    else:
        login(request, user)
        messages.success(request, "Giriş başarılı")
        return redirect("index")

@login_required(login_url="loginUser")
def logOut(request):
    logout(request)
    messages.success(request, "Çıkış başarılı")
    return redirect("loginUser")



    
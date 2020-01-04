from django.shortcuts import render, HttpResponse
import random
from string import ascii_lowercase, ascii_uppercase, digits
from hashlib import md5
from django.db import connections
from datetime import datetime
import math
from sys import getsizeof

def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;")
    )

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def sql_get(query,*args):
    cur = connections['default'].cursor()
    cur.execute(query,args)
    return cur.fetchall()

def sql_post(query,*args):
    cur = connections['default'].cursor()
    cur.execute(query,args)

chars = ascii_lowercase+ascii_uppercase+str(digits)
def genchar():
    x = str(datetime.now().time())
    x += ''.join([random.choice(chars) for i in range(20)])
    return md5(x.encode()).hexdigest()


def main(request):
    if request.method == 'POST':
        ch = genchar()
        content = request.POST['cont'].encode('ascii', 'ignore').decode('ascii')
        langs = ['python', 'javascript', 'php', 'ruby', 'perl', 'c', 'css', 'html']
        if request.POST['lang'] in langs:
            sql_post("insert into pastes (url, data, lang) values(%s,%s,%s)",ch,content,request.POST['lang'])
        else:
            sql_post("insert into pastes (url, data, lang) values(%s,%s,'none')",ch,content)
        return HttpResponse(f'<script>document.location="{request.get_raw_uri()+ch}";</script>')
    return render(request,'new.html')

def paste(request,name):
    content = sql_get("select data from pastes where url=%s",name)
    if len(content) == 0:
        return HttpResponse("Paste Not Found")
    lang = sql_get("select lang from pastes where url=%s",name)[0][0]
    cont = htmlspecialchars(content[0][0])
    size = convert_size(getsizeof(cont))
    return render(request, 'paste.html', {'paste':cont, 'url':name,'size':size,'lang':lang})

def view(request):
    if request.method == 'POST':
        paste_id = request.POST['id']
        if not len(sql_get("select lang from pastes where url=%s",paste_id)):
            return render(request,'view.html',{'msg':'Paste not found'})
        return HttpResponse(f'<script>document.location="/{paste_id}";</script>')
    return render(request,'view.html')


def raw(request,name):
    content = sql_get("select data from pastes where url=%s",name)
    if len(content) == 0:
        return HttpResponse("Paste Not Found")
    else:
        return HttpResponse(content[0][0], content_type='text/plain')

def download(request,name):
    content = sql_get(f"select data from pastes where url=%s",name)
    if len(content) == 0:
        return HttpResponse("Paste Not Found")
    else:
        return HttpResponse(content[0][0], content_type='application/octet-stream')

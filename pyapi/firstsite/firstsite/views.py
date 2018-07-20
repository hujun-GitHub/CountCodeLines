from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import os
import pymysql

@csrf_exempt
def test_api(request):
    print('computer_name=' + request.GET.get('computer_name', ''))
    if '' == request.GET.get('computer_name',''):
        return render_to_response("hello.html")
    else:
        computer_name = request.GET.get('computer_name','')
    dic = {}
    dic['computer_name'] = computer_name

    return render_to_response("hello.html", dic)


@csrf_exempt
def img_api(request):
    request.encoding='utf-8'

    img = request.FILES.get('imgfile') 
    computer_name = request.POST.get('computer_name')
    if img is None:
        return render_to_response("hello.html")
    
    print('===>判断这个程序员的付款图片是否存在。')
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Abc12345~', db='locc_db')
    cursor = db.cursor()
    cursor.execute("select pay_image from payinfo_t where computer_name = '"+computer_name+"'")
    row = cursor.fetchone()
    print('===>查询结果：' + str(row))
    if row is not None:
        print('===>存在,就更新')
        cursor.execute("update payinfo_t set pay_image = '"+img.name+"' where computer_name = '"+computer_name+"'")
        print('===>删除老的图片')
        os.remove(os.path.join(os.getcwd() + '/static/upload', row[0]))

    else:
        print('===>不存在，就插入')
        cursor.execute("insert into payinfo_t(computer_name,pay_image) values('"+computer_name+"', '"+img.name+"')")
    
    print('===>保存新图片')
    f = open(os.path.join(os.getcwd() + '/static/upload', img.name), 'wb')
    for chunk in img.chunks(chunk_size=1024):
        f.write(chunk)
        f.close()
    
    db.commit()
    db.close()

    return render_to_response("hello1.html")

@csrf_exempt
def get_pay_img_api(request):
    computer_name = request.GET.get('computer_name','')
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Abc12345~', db='locc_db')
    cursor = db.cursor()
    cursor.execute("select pay_image from payinfo_t where computer_name = '" + computer_name + "'")
    row = cursor.fetchone()
    if row is not None:
        return JsonResponse({"result": row[0]})
    else:
        return JsonResponse({"result": ""})


@csrf_exempt
def is_pay_info_exist(request):
    computer_name = request.GET.get('computer_name')
    print('views.py - is_pay_info_exist:' + computer_name)
    request.encoding = 'utf-8'

    print('===>判断这个程序员的付款图片记录是否存在。')
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Abc12345~', db='locc_db')
    cursor = db.cursor()
    cursor.execute("select pay_image from payinfo_t where computer_name = '" + computer_name + "'")
    row = cursor.fetchone()

    print('查询结果===>' + str(row))
    if row is None:
        print('记录不存在')
        return JsonResponse({"result": "NOT_EXIST"})
    else:
        print('记录存在')
        return JsonResponse({"result": "EXIST"})

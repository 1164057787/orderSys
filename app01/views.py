from django.shortcuts import render
from django.shortcuts import HttpResponse, render, redirect
# from django.db import models
# Create your views here.
from tools import gettime

from django.core.paginator import Paginator  # 分页管理

from app01 import models


def index(request):
    # 业务逻辑
    # 返回结果
    # return HttpResponse('INDEX') #返回一个字符串
    return render(request, 'index.html')





def usertest(request):
    # 业务逻辑
    # 返回结果
    # return HttpResponse('INDEX') #返回一个字符串
    return render(request, 'usertest.html')


def orderpage(request):
    # 业务逻辑
    user = request.COOKIES.get("username")  # 用户名
    uid = models.User.objects.get(username=user).id  # 用户id
    oobj = models.Order.objects.filter(orderuser=uid).last()  # 该用户最后一个单子 即未完成那个
    # print(type(oobj))
    # print(oobj.id,oobj.title,oobj.ordertime,oobj.state)
    title = oobj.title
    otime = oobj.ordertime

    ouobj = models.userorder.objects.filter(orderid=oobj.id)  # 该单子内容的对象列表

    # 对ouobj进行重新封装，因为里面东西太多一些是不需要的
    # print(type(ouobj))

    page_number = request.GET.get('page', default='1')
    p = Paginator(ouobj, 8)
    page = p.page(int(page_number))
    # print(type(page))
    # print(ouobj[1].id.username)
    # print(ouobj[1].id)

    # for item in  ouobj:
    # print(item.ordercontent)

    return render(request, "orderpage.html", {"ouobj": ouobj, "page": page, "p": p, "title": title})
    # return render(request,"orderpage.html")


def ordersubmit(request):
    if request.method == 'GET':
        return render(request, 'ordersubmit.html')

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = request.COOKIES.get("username")
        # print(request.type(request))
        # print(request.method,type(request.method))
        uobj = models.User.objects.get(username=user)  # 得到当前用户的Id
        # print(obj.id)
        # 插入数据库，先插入表单
        rt = models.Order.objects.create(title=title, state=1, orderuser=uobj)  # 插入成功后返回值是当前插入的对象
        # rt.save()
        # 再插入到用户工单表 这里不能插入数字要插入实例
        time = gettime.getnowtime()
        ourt = models.userorder.objects.create(ordercontent=content, orderid=rt, userid=uobj)
        ourt.outime = time

        return render(request, 'test.html')

    # 业务逻辑
    # 返回结果
    # return HttpResponse('INDEX') #返回一个字符串


def userlogin(request):
    # print(request.type(request))
    # print(request.method,type(request.method))
    if request.method == 'POST':
        # print(request.POST,type(request.POST))
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # print(user,pwd)
        # if user=="fuqc" and pwd =="123":
        if models.User.objects.filter(username=user, password=pwd,userstate=0):
            # return HttpResponse("chenggong")
            rt = redirect('/userunfinorder/')
            rt.set_cookie('username', value=user)

            # return redirect('/usertest/')
            return rt
            # return redirect("http://www.baidu.com")  可以返回地址或者路径 都是可以的

    return render(request, 'userlogin.html')


def admintest(request):
    # 业务逻辑
    # 返回结果
    # return HttpResponse('INDEX') #返回一个字符串
    print(request.COOKIES)
    # for i in request.COOKIES:
    #     print()
    # u=request.COOKIES['currentuser']
    # print(u)
    return render(request, 'admintest.html')


def adminlogin(request):
    # print(request.type(request))
    # print(request.method,type(request.method))
    if request.method == 'POST':
        # print(request.POST,type(request.POST))
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        # rt=redirect("/admintest/")

        # print(response.COOKIES)
        # print(type(rt))
        # print(user,pwd)
        # print(request.COOKIES)
        # print(type((request.COOKIES)))
        # if user=="fuqc" and pwd =="123":
        # if models.User.objects.filter(username=user,password=pwd):
        if models.Admin.objects.filter(adminname=user, adminpwd=pwd):
            # setuser=redirect('ok')

            # r.set_cookie('currentuser',"ttt")
            # rt = HttpResponse("设置cookie")
            # rt = redirect('/admintest/')
            # rt.set_cookie('username', value=user)
            # print(type(ogin))l
            # return HttpResponse("chenggong")
            return redirect('/unfinorder/')
            # return rt
            # return redirect("http://www.baidu.com")  可以返回地址或者路径 都是可以的

    return render(request, 'adminlogin.html')


def register(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # print(user,pwd)
        if len(user) == 0 or len(pwd) == 0:
            error = '用户名和密码不能为空！'
            return render(request, 'register.html', locals())
        elif models.User.objects.filter(username=user):
            error = '该用户名已存在！'
            return render(request, 'register.html', locals())
        else:
            models.User.objects.create(username=user, password=pwd,userstate=1)
            error = '注册成功，等待审核！！'
            return render(request, 'register.html', locals())
    else:
        return render(request, 'register.html')


def test(request):  # c测试方法
    # ret = models.User.objects.all()  # 获取表中所哟数据，返回的是一个对象 列表 打印如下
    # for i in ret:
    #     print(i.userid, i.username, i.password, type(i.userid))
    # print(ret, type(ret))



    # ret=models.User.objects.get(username='fuqc',password='123') #获取数据 返回对象  ；但获取不到；或者多条数据会报错
    # ret=models.User.objects.filter()  #获取满足条件的对象列表 返回一个对象、空对象、

    return render(request, 'replysuccess.html')


def about(request):
    # 业务逻辑
    # 返回结果
    # return HttpResponse('INDEX') #返回一个字符串
    return render(request, 'about.html')


def help(request):
    # 业务逻辑
    # 返回结果
    # return HttpResponse('INDEX') #返回一个字符串
    return render(request, 'help.html')

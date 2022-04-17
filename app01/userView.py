from django.shortcuts import render
from django.shortcuts import HttpResponse, render, redirect
# from django.db import models
# Create your views here.
from tools import gettime,redisCache

from django.core.paginator import Paginator  # 分页管理

from app01 import models

#发起工单（首次提交）
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
        # ourt.save()
        # newourt=models.userorder.objects.filter(orderid=ourt.id).order_by("id")

        # print(ourt.id,ourt.ordercontent)

        #这里的ourt是插入成功后返回的对象，已经是对象,但是却不是queryset 要再查一遍得到queryset
        #或者把这个类型转换为queryset
        # 分页管理
        # page_number = request.GET.get('page', default='1')
        # p = Paginator(newourt, 8)
        # page = p.page(int(page_number))

        # return HttpResponse(ourt)
        return render(request, "usersubsucess.html", {"content": content, "time": ourt.outime, "title": title, "replyinfo": "工单发起成功！"})



#查看已完成工单
def userfinorder(request):

    user = request.COOKIES.get("username")
    userid=models.User.objects.get(username=user).id

    ret = models.Order.objects.filter(state=0,orderuser=userid).order_by("id")

    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    # return 0
    return render(request,"userfinorder.html",{"ufinorder":ret,"page":page,"p":p})

# 查看未完成工单
def userunfinorder(request):
    user = request.COOKIES.get("username")
    userid = models.User.objects.get(username=user).id

    ret = models.Order.objects.filter(state=1,orderuser=userid).order_by("id")

    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    return render(request, "userunfinorder.html", {"unorder": ret, "page": page, "p": p})




#工单详情页
def userodetail(request):
    oid = request.GET.get("orderid")
    # print(oid)  从链接里拿到工单的ID 再去查找该工单的具体内容
    title = models.Order.objects.get(id=oid).title  # 如果这里做分页显示，用get 如果为空回报差，而filter拿到空不报错
    ret = models.userorder.objects.filter(orderid=oid).order_by("id")  # 查找到该工单 返回queryset

    redisorder = "order" + str(oid)
    print(redisorder)
    count = 1
    if redisCache.exist(redisorder):
        cont = redisCache.getvalue(key=redisorder)

        for i in ret:
            if i.ordercontent in cont:
                count = count + 1


            else:
                # break
                redisCache.lpush(key=redisorder,value=i.ordercontent)

    else:

        for i in ret:
            # print(i.ordercontent)
            # print(type(i.ordercontent))
            redisCache.lpush(redisorder, i.ordercontent)

    # 分页管理
    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    # return render(request,"odetail.html",{"ouobj":ret,"page":page,"p":p,"title":title})
    return render(request, "userodetail.html", {"odetail": ret, "page": page, "p": p, "title": title})




#回复工单
def userorply(request):

    oid = request.GET.get("orderid")
    title = models.Order.objects.get(id=oid).title
    ret = models.userorder.objects.filter(orderid=oid).order_by("id")  # 查找到该工单 返回queryset

    # 分页管理
    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    if request.method == 'GET':  # 返回到基本的渲染页面

        return render(request, "useroreply.html", {"oreply": ret, "page": page, "p": p, "title": title})

    elif request.method == 'POST':  # 读取管理员回复的信息

        replycontent = request.POST.get("content")  # userorder表的ordercontent
        orderobj = models.Order.objects.get(id=oid)  # userorder表的orderid
        # userobj=models.User.objects.get(id=orderobj.orderuser)
        nid = orderobj.orderuser  # 这里的nid是一个user object
        # print(nid)
        # print(nid.username)
        # # userobj=models.User.objects.get(id=id)
        # print(replycontent)
        # print(orderobj.title)
        # print(userobj)
        # print(userobj.username)
        ourt = models.userorder.objects.create(ordercontent=replycontent, orderid=orderobj, userid=nid)  # 插到userorder
        ourt.save()

        nret = models.userorder.objects.filter(orderid=oid).order_by("id")  # 重新查找返回

        # 分页管理
        npage_number = request.GET.get('page', default='1')
        np = Paginator(nret, 8)
        npage = np.page(int(npage_number))

        return render(request, "userreplysuccess.html", {"page": npage, "p": np, "title": title, "replyinfo": "回复成功！"})
        # return render(request,"admintest.html")


#用户关闭工单的业务实现
def closeorder(request):

    orderid = request.GET.get("orderid")
    ret=models.Order.objects.get(id=orderid)
    ret.state=0
    print(models.Order.objects.get(id=orderid).state)

    ret.save()

    # return HttpResponse(orderid,models.Order.objects.get(id=orderid).state)
    return redirect('/userfinorder/')



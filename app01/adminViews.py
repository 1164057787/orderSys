from django.shortcuts import render
from django.shortcuts import HttpResponse,render,redirect
# from django.db import models
# Create your views here.
from tools import gettime

from django.core.paginator import Paginator #分页管理

from app01 import models

from tools import redisCache

#实现查看已完成工单
def finorder(request):

    ret=models.Order.objects.filter(state=0).order_by("id")

    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    return render(request,"finorder.html",{"order":ret,"page":page,"p":p})


#实现查看未完成工单
def unfinorder(request):

    ret=models.Order.objects.filter(state=1).order_by("id")

    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    return render(request,"unfinorder.html",{"unorder":ret,"page":page,"p":p})



#工单详情页

def odetail(request):
    oid=request.GET.get("orderid")
    # print(oid)  从链接里拿到工单的ID 再去查找该工单的具体内容
    title=models.Order.objects.get(id=oid).title   #如果这里做分页显示，用get 如果为空回报差，而filter拿到空不报错
    ret=models.userorder.objects.filter(orderid=oid).order_by("id")  #查找到该工单 返回queryset


    redisorder="order" + str(oid)
    print(redisorder)
    count=1
    if redisCache.exist(redisorder):
        cont=redisCache.getvalue(key=redisorder)
        # print(cont)
        for i in ret:
            if i.ordercontent in cont:
                count=count+1
                # print(i.ordercontent)

            else:
                # break
                # print(i.ordercontent)
                redisCache.lpush(key=redisorder, value=i.ordercontent)

    else:

        for i in ret:
            # print(i.ordercontent)
            # print(type(i.ordercontent))
            redisCache.lpush(redisorder,i.ordercontent)




    #分页管理
    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    # return render(request,"odetail.html",{"ouobj":ret,"page":page,"p":p,"title":title})
    return render(request,"odetail.html",{"odetail":ret,"page":page,"p":p,"title":title})



#工单回复
def oreply(request):

    oid = request.GET.get("orderid")
    title = models.Order.objects.get(id=oid).title
    ret = models.userorder.objects.filter(orderid=oid).order_by("id")  # 查找到该工单 返回queryset


    #分页管理
    page_number = request.GET.get('page', default='1')
    p = Paginator(ret, 8)
    page = p.page(int(page_number))

    if request.method=='GET': #返回到基本的渲染页面

        return render(request,"oreply.html",{"oreply":ret,"page":page,"p":p,"title":title})

    elif request.method == 'POST':  #读取管理员回复的信息

        replycontent=request.POST.get("content") #userorder表的ordercontent
        orderobj=models.Order.objects.get(id=oid)  #userorder表的orderid
        # userobj=models.User.objects.get(id=orderobj.orderuser)
        nid=orderobj.orderuser   #这里的nid是一个user object
        # print(nid)
        # print(nid.username)
        # # userobj=models.User.objects.get(id=id)
        # print(replycontent)
        # print(orderobj.title)
        # print(userobj)
        # print(userobj.username)
        ourt=models.userorder.objects.create(ordercontent=replycontent, orderid=orderobj, userid=nid)#插到userorder
        ourt.save()

        nret = models.userorder.objects.filter(orderid=oid).order_by("id") #重新查找返回


        # 分页管理
        npage_number = request.GET.get('page', default='1')
        np = Paginator(nret, 8)
        npage = np.page(int(npage_number))

        return render(request,"replysuccess.html",{"page":npage,"p":np,"title":title,"replyinfo":"回复成功！"})
        # return render(request,"admintest.html")


#查看未审核通过的用户
def usercheck(request):
    retuser=models.User.objects.filter(userstate=1).order_by("id")
    page_number = request.GET.get('page', default='1')
    p = Paginator(retuser, 8)
    page = p.page(int(page_number))

    return render(request, "checkuser.html", {"retuser": retuser, "page": page, "p": p})
    # return 0

# 用户的注册审核业务逻辑具体实现
def check(request):
    uid = request.GET.get("userid")
    ret=models.User.objects.get(id=uid)
    ret.userstate=0

    ret.save()

    return redirect('/usercheck/')

from tools.redis_pool import POOL
import redis
from django_redis import get_redis_connection
from django.shortcuts import render,HttpResponse

def test():

    coon=redis.Redis(connection_pool=POOL)
    coon.set("name","fuqc")
    coon.set("name1","吃了吗")

    str=coon.get("name")
    print(str)


    # print(coon.get("name"))
    # print(str(coon.get("name"),encoding='utf-8'))
    # print(str(coon.get("name1"),encoding='utf-8'))
    # print(str(coon.get("n"),encoding='utf-8'))

    return 0

# test()



def test2(request):
    # 从连接池中拿到连接
    rs = get_redis_connection()

    ss=rs.get("n")  #如果没查到 就会返回None
    print(ss)

    # rs.lpush("test1","怎么说死机了","不知道怎么处理，晚点去现场")
    s1=rs.lrange("test1",0,-1)
    print(s1)

    return HttpResponse(ss)


# saveinfo(3)

def exist(key):   #判断该工单是否已经存在与redis
    rs = get_redis_connection()
    if rs.exists(key):
        return True

    return False

def lpush(key,value):   #该方法将一个或多个值插入到列表头部
    rs = get_redis_connection()
    rs.lpush(key,value)
    # print(rs.lrange(key,0,-1))


    # print(rs.exists(key))
    return 0

def getvalue(key):    #该方法获取当前id下，redis工单中的所有内容
    rs = get_redis_connection()
    ll=rs.lrange(key,0,-1)

    return ll


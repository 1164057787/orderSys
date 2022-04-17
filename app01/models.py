from django.db import models

# Create your models here.

class Admin(models.Model):#管理员表，继承model类
    adminid=models.IntegerField()
    adminname=models.CharField(max_length=32)
    adminpwd=models.CharField(max_length=32)


class User(models.Model):#用户表
    # userid = models.IntegerField()
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)#用名字 密码
    userstate=models.IntegerField(default=1) #用户状态 用于管理员审核



class Order(models.Model):#工单表

    title=models.CharField(max_length=128)
    # contenr=models.CharField(max_length=256)
    ordertime=models.DateTimeField(auto_now_add=True)
    state=models.IntegerField()
    orderuser=models.ForeignKey("User",on_delete=models.CASCADE,default=1)
    orderadmin=models.CharField(max_length=32)


class userorder(models.Model):
    outime=models.DateTimeField(auto_now=True)
    orderid=models.ForeignKey("Order",on_delete=models.CASCADE)
    userid=models.ForeignKey("User",on_delete=models.CASCADE)
    ordercontent=models.CharField(max_length=256)






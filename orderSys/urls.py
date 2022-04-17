"""orderSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse, render
from django.urls import path, re_path

from app01 import views, adminViews,userView
from tools import redisCache

# def index(request):
#     # 业务逻辑
#
#
#     # 返回结果
#     # return HttpResponse('INDEX') #返回一个字符串
#     return render(request,'index.html')


urlpatterns = [
    # path('admin/', admin.site.urls),
    # 公共路由
    # path('index1/', views.index1),
    path('index/', views.index),

    path('usertest/', views.usertest),
    path('userlogin/', views.userlogin),

    path('admintest/', views.admintest),
    path('adminlogin/', views.adminlogin),

    path('about/', views.about),
    path('help/', views.help),

    path('register/', views.register),

    path('opage/', views.orderpage),

    # 管理员视图下的路由
    path('unfinorder/', adminViews.unfinorder),
    path('finorder/', adminViews.finorder),

    path('odetail/', adminViews.odetail),

    path('oreply/', adminViews.oreply),
    path('usercheck/', adminViews.usercheck),
    path('check/', adminViews.check),

    # 用户路由
    path('osubmit/', userView.ordersubmit),
    path('userfinorder/', userView.userfinorder),
    path('userodetail/', userView.userodetail),
    path('userunfinorder/', userView.userunfinorder),
    path('useroreply/', userView.userorply),
    path('closeorder/', userView.closeorder),



    path('test/', views.test),
    path('test2/', redisCache.test2),

    # 前后端分离的路由
    # re_path('admins/(?P<pk>\d+)',views.AdminView.as_view())
    # path('admins/',views.AdminView.as_view())
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

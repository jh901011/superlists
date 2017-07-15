"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
import lists.urls
#import lists.views   #需要先导入lists包和views文件，若未导入lists，会报lists未定义的错误，若未导入views，服务器会报没有views属性错误


urlpatterns = [
#     url(r'^admin/', admin.site.urls),  #由于版本问题，已经没有了include关键字，直接用调用就好了,不过需要import一次
    url(r'^$', lists.views.home_page, name='home'),
    url(r'^lists/', include('lists.urls')),   #啃官方文档。在引用其他的urlconf时，需要使用includ关键字，与配置URL的方式不一样
]

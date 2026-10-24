"""
URL configuration for Blockchain_Enabled_Chat_Application_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from Blockchain_Enabled_Chat_Application_System import views as mv
from Users import views as uv
from Admin import views as av

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mv.index,name='index'),
    path('userLoginForm',mv.userLoginForm,name='userLoginForm'),
    path('userRegisterForm',mv.userRegisterForm,name='userRegisterForm'),
    path('adminLoginForm',mv.adminLoginForm,name='adminLoginForm'),


    #AdminURLs

    path('adminLoginCheck',av.adminLoginCheck,name='adminLoginCheck'),
    path('adminHome',av.adminHome,name='adminHome'),
    path('userList',av.userList,name='userList'),
    path('activate_user',av.activate_user,name='activate_user'),
    path('deactivate_user',av.deactivate_user,name='deactivate_user'),
    path('delete_user',av.delete_user,name='delete_user'),
    
    path('log',av.log,name='log'),

    path('Ulog',uv.Ulog,name='Ulog'),

    #USERSURLS

    path('userRegisterCheck',uv.userRegisterCheck,name='userRegisterCheck'),
    path('userLoginCheck',uv.userLoginCheck,name='userLoginCheck'),
    path('userHome',uv.userHome,name='userHome'),
    path('search',uv.search,name='search'),
    path('start_chat',uv.start_chat,name='start_chat'),   
    path('clear_blocks',uv.clear_blocks,name='clear_blocks'),
    # path('chatHistory',uv.chatHistory,name='chatHistory'),




]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

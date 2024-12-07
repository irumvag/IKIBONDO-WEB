from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('',index,name=''),
    path('about/',about,name='about'),
    path('contactus/',contactus,name='contactus'),
    path('login/',login_view,name='login'),
    path('useradmin/',useradmin,name='useradmin'),
    path('logout',logout_view,name='logout'),
    path('adminfeedback',adminfeedback,name='adminfeedback'),
    path('chw',chw,name='chw'),
    path('addchw',addchw,name='addchw'),
    path('change_password',change_password,name='change_password'),
    path('userprofile',userprofile_view,name='userprofile'),
    path('setting',setting_view,name='setting'),
    path('notification',notification_view,name='notification'),
    path('parents',pandb_view,name='parents'),
    path('vaccine',vandm_view,name='vaccine'),
    path('reports',report_view,name='reports'),
    path('admins',admin_view,name='admins'),
    path('babies',babies,name='babies'),
    path('hospitals',hospital_view,name='hospitals'),
]

urlpatterns+= staticfiles_urlpatterns()

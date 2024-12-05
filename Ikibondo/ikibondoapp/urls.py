from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('',index,name=''),
    path('about/',about,name='about'),
    path('contactus/',contactus,name='contactus'),
    path('login/',login_view,name='login'),
    path('useradmin/',useradmin,name='useradmin'),
    path('signup/',signup,name="signup"),
    path('logout',logout_view,name='logout'),
    path('adminfeedback',adminfeedback,name='adminfeedback'),
    path('chw',chw_view,name='chw'),
    path('addchw',addchw,name='addchw'),
    path('change_password',change_password,name='change_password'),
]

urlpatterns+= staticfiles_urlpatterns()
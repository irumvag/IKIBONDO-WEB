from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

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
    path('babies/<str:phone>/',babies,name='babies'),
    path('babies/',babies_view,name='babies'),
    path('hospitals',hospital_view,name='hospitals'),
    #path(r'^(?P<phone_number>[\w])/$',userdetail),
    path('userdetail/<str:phone>/',userdetail,name='userdetail'),
    #reset password url
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #end reset
    path('approve/<str:phone>/<str:role>/',create_chw,name='approve'),
    path('add_vaccine/',add_vaccine,name='add_vaccine'),
    path('userparent/',parent_view,name='userparent'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
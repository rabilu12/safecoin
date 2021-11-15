from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path
from members import views
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # The user profile file
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),
    # Authentication files
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("agent/upgrade/", views.agent_register, name="agent_register"),
    path("verification/invoice/", views.invoice, name="invoice"),
    path("documents/upload/", views.idupload, name="idupload"),
    path('user/profile/', views.UserProfile.as_view(), name='userprofile'),
    path('agent/profile/', views.AProfile.as_view(), name='aprofile'),
    path("agt/profile/", views.agentprofile, name="agentprofile"),
    path("unit/topup/", views.topup, name="topup"),
    path("unit/topup60/", views.topup60, name="topup60"),
    path("unit/topup130/", views.topup130, name="topup130"),
    path("unit/topup270/", views.topup270, name="topup270"),
    path("unit/topup550/", views.topup550, name="topup550"),
    path("unit/usdttopup60/", views.usdttopup60, name="usdttopup60"),
    path("unit/usdttopup130/", views.usdttopup130, name="usdttopup130"),
    path("unit/usdttopup270/", views.usdttopup270, name="usdttopup270"),
    path("unit/usdttopup550/", views.usdttopup550, name="usdttopup550"),
    path("unit/bnbtopup60/", views.bnbtopup60, name="bnbtopup60"),
    path("unit/bnbtopup130/", views.bnbtopup130, name="bnbtopup130"),
    path("unit/bnbtopup270/", views.bnbtopup270, name="bnbtopup270"),
    path("unit/bnbtopup550/", views.bnbtopup550, name="bnbtopup550"),
    path("agent/feeverify/", views.feeverify, name="feeverify"),
    path("agent/give/", views.give, name="give"),
    path("agent/certification/vic", views.paywithvictor, name="paywithvictor"),
    path("agent/certification/ray", views.ray, name="ray"),
    path("agent/certification/qrb", views.qrb, name="qrb"),
    path("agent/certification/msn", views.msn, name="msn"),
    path("agent/certification/msa", views.msa, name="msa"),

    path("agent/certification/busy", views.busy, name="busy"),
    
    path("vppsubs/", views.vppsubs, name="vppsubs"),
    path("checkupload/", views.checkidupload, name="checkidupload"),
    path("documents/uploadsuccess", views.iduploadsuccess, name="iduploadsuccess"),
    path("agentoruser/", views.agentoruser, name="agentoruser"),



]

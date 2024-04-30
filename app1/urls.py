from django.urls import path
from .  import views

urlpatterns=[
    path("",views.login_page,name="login"),
    path("register/",views.register,name="register"),
    path("home/",views.home,name="home"),
    path("logout/",views.logout_page,name="logout"),
]
#pg_ctl start -D "C:\Program Files\PostgreSQL\16\data"
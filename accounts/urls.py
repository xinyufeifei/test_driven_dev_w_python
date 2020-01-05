from django.conf.urls import url
from accounts import views


urlpatterns = [
    url("^send_login_email$", views.send_login_mail, name="send_login_email"),
    url("^login$", views.login, name="login"),
]

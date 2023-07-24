from django.urls import path
from .views import RegisterAccount

urlpatterns = [
   path('register/', RegisterAccount.as_view()),
   ]
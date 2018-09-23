#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.DetailedUser.as_view(), name="details"),
    path('', views.UserList.as_view(), name="list"),
]
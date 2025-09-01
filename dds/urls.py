from django.urls import path

from . import views

app_name = "dds"

# регистрация путей
urlpatterns = [
    path("", views.record_list, name="record_list"),
    path("records/add/", views.record_add, name="record_add"),
    path("records/edit/<int:pk>/", views.record_edit, name="record_edit"),
    path("records/delete/<int:pk>/", views.record_delete, name="record_delete"),
]

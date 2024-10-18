from django.urls import path
from . import views
from .views import enter_new_order, select_sub_part

urlpatterns = [
    path('enter-new-order/<int:sub_part_id>/', views.enter_new_order, name='enter_new_order'),
    path('generate-reports/', views.generate_reports, name='generate_reports'),
    path('select-sub-part/', select_sub_part, name='select_sub_part'),
]

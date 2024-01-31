from django.urls import path
from .views import (
    CreateCompanyView,
    company_list,
    DeleteCompanyView,
    UpdateCompanyView
)

urlpatterns = [
    path('company/', company_list, name='company_list'),
    path('company/create/', CreateCompanyView.as_view(), name='create_company'),
    path('company/<int:company_id>/',
         UpdateCompanyView.as_view(), name='update_company'),
    path('company/delete/',
         DeleteCompanyView.as_view(), name='delete_company'),
]

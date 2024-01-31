from django.urls import path
from .views import (
    CreateIndustryView,
    UpdateIndustryView,
    DeleteIndustryView,
    industry_list,
    industry_feed,
)

urlpatterns = [
    path("industry/", industry_list, name="industry_list"),
    path("industry/create/", CreateIndustryView.as_view(), name="create_industry"),
    path(
        "industry/<int:industry_id>/",
        UpdateIndustryView.as_view(),
        name="update_industry",
    ),
    path("industry/<str:industry_name>/feed", industry_feed, name="industry_feed"),
    path("industry/delete/", DeleteIndustryView.as_view(), name="delete_industry"),
]

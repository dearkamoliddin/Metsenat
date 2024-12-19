from django.urls import path
from apps.common.views import (
    UserAPIView,
    SponsorView, SponsorCreateView, SponsorDetailView, SponsorUpdateView,
    StudentView, StudentCreateView, StudentDetailView, StudentUpdateView,
    StudentSponsorView, StudentSponsorCreateView, StudentSponsorDetailView, StudentSponsorUpdateView,
    DashboardListView, DashboardGraphAPIView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Users API
    path('users/', UserAPIView.as_view(), name='users'),

    # Dashboard API
    path('dashboard/', DashboardListView.as_view(), name='statistics'),
    path('dashboard/graph/', DashboardGraphAPIView.as_view(), name='sponsors_students_number'),


    # Sponsor urls
    path('sponsor/list/', SponsorView.as_view(), name='sponsor'),
    path('sponsor/create/', SponsorCreateView.as_view(), name='sponsor_create'),
    path('sponsor/<int:id>/detail/', SponsorDetailView.as_view(), name='sponsor_detail'),
    path('sponsor/<int:id>/edit/', SponsorUpdateView.as_view(), name='sponsor_update'),

    # Student urls
    path('student/list/', StudentView.as_view(), name='student'),
    path('student/create/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:id>/detail/', StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:id>/edit', StudentUpdateView.as_view(), name='student_update'),

    # StudentSponsor urls
    path('student_sponsor/list/', StudentSponsorView.as_view(), name='student_sponsor'),
    path('student_sponsor/create/', StudentSponsorCreateView.as_view(), name='student_sponsor_create'),
    path('student_sponsor/<int:id>/detail/', StudentSponsorDetailView.as_view(), name='student_sponsor_detail'),
    path('student_sponsor/<int:id>/edit/', StudentSponsorUpdateView.as_view(), name='student_sponsor_edit'),

    # JWTAuthentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

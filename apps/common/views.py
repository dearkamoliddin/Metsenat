from django.shortcuts import render
from rest_framework.response import Response

from django.db.models.functions import TruncMonth

from django.db.models import Sum, Avg, Count

from rest_framework.views import APIView

from rest_framework import generics, filters, status

from rest_framework.generics import (
    ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.common.models import Sponsor, Student, University, StudentSponsor

from collections import defaultdict

from apps.common.serializers import (
    SponsorSerializer, StudentSerializer, StudentSponsorSerializer, StudentSponsorUpdateSerializer,
    DashboardSerializer,
)

permissions = "" #[IsAuthenticated]
authentications = "" #[JWTAuthentication]


class UserAPIView(APIView):
    permission_classes = permissions
    authentication_classes = authentications

    def get(self, request):
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
        }
        return Response(data=user_data, status=status.HTTP_200_OK)


class SponsorView(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'amount', 'status']
    filterset_fields = ['amount', 'status', 'created_at']
    permission_classes = permissions
    authentication_classes = authentications


class SponsorCreateView(generics.CreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = permissions
    authentication_classes = authentications


class SponsorDetailView(RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    lookup_field = "id"
    permission_classes = permissions
    authentication_classes = authentications


class SponsorUpdateView(RetrieveUpdateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    lookup_field = "id"
    permission_classes = permissions
    authentication_classes = authentications


# Student List API (Filter, pagination, search)
class StudentView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name']
    filterset_fields = ['student_type', 'university']
    permission_classes = permissions
    authentication_classes = authentications


class StudentCreateView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = permissions
    authentication_classes = authentications


class StudentDetailView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"
    permission_classes = permissions
    authentication_classes = authentications


class StudentUpdateView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"
    permission_classes = permissions
    authentication_classes = authentications


# Student & Sponsor CRUD
class StudentSponsorView(ListAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['student', 'sponsor', 'allocated_money']
    search_fields = ['student__full_name', 'sponsor__full_name']
    permission_classes = permissions
    authentication_classes = authentications


class StudentSponsorCreateView(CreateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    permission_classes = permissions
    authentication_classes = authentications


class StudentSponsorDetailView(RetrieveAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    lookup_field = "id"
    permission_classes = permissions
    authentication_classes = authentications


class StudentSponsorUpdateView(RetrieveUpdateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorUpdateSerializer
    lookup_field = "id"
    permission_classes = permissions
    authentication_classes = authentications


class DashboardListView(APIView):
    def get(self, request):
        total_asked_sum = Student.objects.aggregate(total_amount=Sum('student_fee'))['total_amount'] or 0
        total_paid_sum = StudentSponsor.objects.aggregate(total_amount=Sum('allocated_money'))['total_amount'] or 0
        need_to_pay = total_asked_sum - total_paid_sum

        return Response({
            "total_requested_amount": total_asked_sum,
            "total_paid_amount": total_paid_sum,
            "total_need_to_be_paid": need_to_pay,
        })


class DashboardGraphAPIView(APIView):
    def get(self, request):
        sponsors = Sponsor.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(
            sponsor_count=Count('id')).values('month', 'sponsor_count')

        serializer_data = DashboardSerializer(sponsors, many=True)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)

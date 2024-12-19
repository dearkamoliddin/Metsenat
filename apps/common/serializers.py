from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.common.models import Sponsor, University, Student, StudentSponsor
from django.db.models import Sum
from django.contrib.auth.models import User


class SponsorSerializer(ModelSerializer):
    spent_money = serializers.CharField(source='amount', read_only=True)

    class Meta:
        model = Sponsor
        fields = '__all__'

    def validate(self, data):
        if data not in dict(Sponsor.SPONSOR_CHOICES):
            raise serializers.ValidationError(detail={'sponsor_type': "Invalid sponsor type"})

        if data not in dict(Sponsor.STATUS_CHOICES):
            raise serializers.ValidationError(detail={"status": "Invalid status"})

        if data['sponsor_type'] == 'legal_entity' and not data.get('organization'):
            raise serializers.ValidationError(
                detail={'organization_name': "Organization field must be provided for legal entities"},
                code=400)

        elif data['sponsor_type'] == 'natural_person' and data.get('organization'):
            raise serializers.ValidationError(detail={"organization": "No Organization for physical persons"})
        return data


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = ['name']


class StudentSponsor1Serializer(ModelSerializer):
    sponsor = serializers.CharField(source='sponsor.full_name', read_only=True)

    class Meta:
        model = StudentSponsor
        fields = ('id', 'sponsor', 'allocated_money')


class StudentSerializer(ModelSerializer):
    studentsponsor_set = StudentSponsor1Serializer(many=True)
    university = serializers.CharField(source='university.name', read_only=True)
    allocated_money = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_allocated_money(self, data):
        total_allocated = StudentSponsor.objects.filter(student=data).aggregate(
            total_allocated=Sum('allocated_money'))['total_allocated']
        return total_allocated or 0

    def validate_student_type(self, value):
        if value not in dict(Student.STUDENT_CHOICES):
            raise serializers.ValidationError(detail={"student type": "Invalid student type"})
        return value


class StudentSponsorSerializer(ModelSerializer):

    class Meta:
        model = StudentSponsor
        fields = ['sponsor', 'allocated_money']

    def validate(self, data):
        sponsor = attrs.get('sponsor')
        student = attrs.get('student')
        allocated_money = attrs.get('allocated_money', 0)

        sponsor_spent_money = sponsor.studentsponsor_set.aggregate(total_amount=Sum('allocated_money'))['total_amount'] or 0
        sponsor_remain_money = sponsor.amount - sponsor_spent_money
        if sponsor_remain_money < allocated_money:
            raise serializers.ValidationError(detail={'sponsor': "Not enough money"})

        total_allocated = StudentSponsor.objects.filter(student=student).aggregate(Sum('allocated_money'))[
                              'allocated_money__sum'] or 0
        total_allocated += allocated_money
        if total_allocated > student.student_fee:
            raise serializers.ValidationError(detail={'allocated_money': "Student contract is full"})

        if allocated_money > student.student_fee:
            raise serializers.ValidationError(detail={'student_fee': 'More than student fee'})

        sponsor_status = sponsor.status
        if sponsor_status != "confirmed":
            raise serializers.ValidationError(detail={"status": "Sponsor status is not confirmed!"})

        return data


class StudentSponsorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = ['id', 'sponsor', 'allocated_money']

    def update(self, instance, validated_data):
        new_sponsor = validated_data.get('sponsor', instance.sponsor)
        new_allocated_money = validated_data.get('allocated_money', instance.allocated_money)

        # Calculate the total allocated money for the new sponsor
        new_sponsor_allocated_money = new_sponsor.studentsponsor_set.aggregate(
            total_allocated_money=Sum('allocated_money')
        )['total_allocated_money'] or 0

        # Calculate the remaining money for the sponsor
        remaining_money = new_sponsor.amount - new_sponsor_allocated_money

        # Check if there is enough money to allocate
        if remaining_money < new_allocated_money:
            raise serializers.ValidationError("Not enough money in the sponsor's account.")

        # Proceed with the update if validation passes
        instance.sponsor = new_sponsor
        instance.allocated_money = new_allocated_money
        instance.save()

        return instance


class DashboardSerializer(serializers.Serializer):
    sponsor_count = serializers.IntegerField()
    month = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['student_count'] = Student.objects.filter(created_at__month=instance['month'].month).count()
        return data

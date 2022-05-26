# from pyexpat import model
from rest_framework import serializers

from courses.models import Course, CourseCategory


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "link",
            "password",
            "status",
            "price",
            "category",
        )


class CourseRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "link",
            "password",
            "status",
            "price",
        )
        # extra_kwargs = {'password':{
        #     'write_only': True
        # }}

        # def create(self, validated_data):
        #     course = Course.objects.create(**validated_data)
        #     course.save()
        #     return course


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "link",
            "password",
            "status",
            "price",
        )


class CourseDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "link",
            "password",
            "status",
            "price",
        )


class CourseCategoryCreateSerialilzer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )


class CourseCategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )


class CourseCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )


class CourseCategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
            "description",
        )

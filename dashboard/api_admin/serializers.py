from rest_framework import serializers


class DashboardOverviewSerializer(serializers.Serializer):
    revenue = serializers.DecimalField(max_digits=7, decimal_places=2)
    courses = serializers.IntegerField()
    exams = serializers.IntegerField()
    students = serializers.IntegerField()
    course_enrollment = serializers.IntegerField()
    users = serializers.IntegerField()


class DashboardRevenueSerializer(serializers.Serializer):
    revenue_overall = serializers.DecimalField(max_digits=7, decimal_places=2)
    revenue_month = serializers.DecimalField(max_digits=7, decimal_places=2)


# class DashboardRevenueGraphSerializer(serializers.Serializer):
#     created_at = serializers.SerializerMethodField(method_name="get_date")

#     class Meta:
#         model = Payment
#         fields = ("__all__")

#     def get_date(self, instance):
#         date = datetime.datetime.now()
#         return date.strftime("%m/%d/%Y")


class DashboardRevenueGraphSerializer(serializers.Serializer):
    January = serializers.DecimalField(max_digits=7, decimal_places=2)
    February = serializers.DecimalField(max_digits=7, decimal_places=2)
    March = serializers.DecimalField(max_digits=7, decimal_places=2)
    April = serializers.DecimalField(max_digits=7, decimal_places=2)
    May = serializers.DecimalField(max_digits=7, decimal_places=2)
    June = serializers.DecimalField(max_digits=7, decimal_places=2)
    July = serializers.DecimalField(max_digits=7, decimal_places=2)
    August = serializers.DecimalField(max_digits=7, decimal_places=2)
    September = serializers.DecimalField(max_digits=7, decimal_places=2)
    October = serializers.DecimalField(max_digits=7, decimal_places=2)
    November = serializers.DecimalField(max_digits=7, decimal_places=2)
    December = serializers.DecimalField(max_digits=7, decimal_places=2)


class DashboardRevenueCourseSerializer(serializers.Serializer):
    course = serializers.CharField(source="enrollment__courses__name")
    total = serializers.DecimalField(max_digits=7, decimal_places=2)

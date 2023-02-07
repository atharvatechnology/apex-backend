from django.contrib import admin
from common.admin import CreatorBaseModelAdmin
from discussion.models import Question 
# Register your models here.

@admin.register(Question)
class QuestionAdmin(CreatorBaseModelAdmin):
    list_display=[
        'id',
        'content',
        'question',
    ]

from rest_framework import serializers
from discussion.models import  Question 
from common.api.serializers import CreatorSerializer

"""Serializer to list all the questions"""
class QuestionListSerializer(serializers.ModelSerializer):
    replies =serializers.StringRelatedField(many=True, read_only =True)
    question =serializers.StringRelatedField(read_only =True)
    class Meta:
        ref_name = "Discussion Question"
        model=Question
        fields=['content','question','replies','created_by','created_at']

"""Serializer to retrieve a question"""
class QuestionRetrieveSerializer(serializers.ModelSerializer):
    replies =serializers.StringRelatedField(many=True, read_only =True)
    question =serializers.StringRelatedField(read_only =True)
    class Meta:
        ref_name = "Discussion Question"
        model=Question
        fields=['id','content','question','replies','created_by','updated_by','created_at','updated_at']

"""Serializer to create question"""
class QuestionCreateSerializer(CreatorSerializer):
    class Meta:
         ref_name = "Discussion Question"
         model=Question
         fields=['content','question']
    def create(self, validated_data):
        question= validated_data["question"]
        if (question is not None) and validated_data.get('question').is_question==False:
                raise serializers.ValidationError(
                    "Reply for Answer is not Possible",
                ) 
        else:
            return Question.objects.create(**validated_data) 

"""Serializer to update question"""
class QuestionUpdateSerializer(CreatorSerializer):
    class Meta:
         ref_name = "Discussion Question"
         model=Question
         fields=['content']
    def update(self, instance, validated_data):
        if (instance.question is not None) and instance.question.is_question==False:
                raise serializers.ValidationError(
                    "Reply for Answer is not Possible",
                )
        else:
            return super().update(instance, validated_data)

            


from rest_framework import serializers
from discussion.models import  Question 

class QuestionSerializer(serializers.ModelSerializer):
    replies =serializers.StringRelatedField(many=True, read_only =True)
    class Meta:
        ref_name = "Discussion Question"
        model=Question
        fields=['id','content','question','replies','created_by','updated_by']
    
    def create(self, validated_data):
        questions=Question.objects.filter(question=None)
        question= validated_data["question"]
        if (question is not None) and validated_data.get('question') not in questions:
                raise serializers.ValidationError(
                    "Reply for Answer is not Possible",
                ) 
        else:
            return Question.objects.create(**validated_data)   
    def update(self, instance, validated_data):
        questions=Question.objects.filter(question=None)
        instance.content=validated_data.get('content',instance.content)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.question =validated_data.get('question',instance.question)
        instance.updated_at =validated_data.get('updated_at',instance.updated_at)
        if (instance.question is not None) and instance.question not in questions:
                raise serializers.ValidationError(
                    "Reply for Answer is not Possible",
                )
        else:
            instance.save()     
        return instance
            

            


from django.db import models
from common.models import CreatorBaseModel
# Create your models here.

class Question(CreatorBaseModel):
    content=models.TextField()
    question = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE,related_name='replies')

    class Meta:
        ordering= ['-created_at']
    
    def __str__(self):
        return self.content
    
    @property
    def is_question(self):
        if self.question is None:
            return True
        return False
    # @property
    # def answers(self):
    #     return Question.objects.filter(question=self).reverse()


from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TaskList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=200)
    caption=models.TextField(null=True,blank=True)
    create_date=models.DateTimeField(auto_now_add=True)
    complete_status=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['complete_status']
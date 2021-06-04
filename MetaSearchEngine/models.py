from django.db import models

class Query(models.Model):
    query= models.CharField(max_length=200)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

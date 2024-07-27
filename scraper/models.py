from django.db import models


# Create your models here.
class TestDB(models.Model):
    test_id = models.IntegerField(primary_key=True)
    test_content = models.CharField(max_length=20)
    test_date = models.DateTimeField(auto_now=True)

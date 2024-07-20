from django.db import models

# Create your models here.
class Fighter(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True, default=0)
    height = models.CharField(max_length=100, null=True, blank=True)
    reach = models.CharField(max_length=100, null=True, blank=True)
    division = models.CharField(max_length=500, null=True, blank=True)
    style = models.CharField(max_length=300, null=True, blank=True)
    wins = models.IntegerField(null=True, blank=True, default=0)
    wins_by_knockout = models.IntegerField(null=True, blank=True, default=0)
    wins_by_submission = models.IntegerField(null=True, blank=True, default=0)
    wins_by_decision = models.IntegerField(null=True, blank=True, default=0)
    losses = models.IntegerField(null=True, blank=True, default=0)
    losses_by_knockout = models.IntegerField(null=True, blank=True, default=0)
    losses_by_submission = models.IntegerField(null=True, blank=True, default=0)
    losses_by_decision = models.IntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        return self.name
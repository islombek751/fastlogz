from django.db import models


class LogModel(models.Model):
    mychoices = (
        ("OFF","OFF"),
        ("ON","ON"),
        ("SB","SB"),
        ("D","D")
    )
    driver = models.ForeignKey('eld.DRIVERS', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('eld.Vehicle',  on_delete=models.CASCADE)
    distance = models.FloatField()
    untilbreak = models.TimeField()
    shift = models.TimeField()
    cycle = models.TimeField()
    worked_hours = models.TimeField()
    current_status = models.TimeField()
    errors = models.TextField()
    dvir = models.TextField()
    duty_status = models.CharField(max_length=50,choices=mychoices,null=True)
    driving  = models.BooleanField(blank=True,default=True)
    cycle_tomorrow = models.TimeField(blank=True)
    driving_in_violation = models.TimeField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    
    
    
    
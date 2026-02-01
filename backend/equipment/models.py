from django.db import models

class EquipmentBatch(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField() # Stores dict of {type: count}

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.file_name

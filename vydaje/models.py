from django.db import models


class EvidenceTable(models.Model):
    title = models.CharField(max_length=255,)
    evidence = models.FileField(upload_to='rates/%Y/%m/%d/')
    is_published = models.BooleanField(default=True)

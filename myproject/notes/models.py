from typing import Any, Mapping
from django.db import models

class Note(models.Model):
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


    def to_dict(self) -> Mapping[str, Any]:
        return {
            'body': self.body,
            'updated': self.updated,
            'created': self.created,
        }


    class Meta:
        ordering = ['-updated']

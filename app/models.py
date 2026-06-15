# app/models.py
from django.db import models

class Term(models.Model):
    
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название термина"
    )
    
    definition = models.TextField(
        verbose_name="Определение"
    )
    
    gost_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Название в соответствии с ГОСТ"
    )
    
    gost_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Термин"
        verbose_name_plural = "Термины"
        ordering = ['name']

from django.db import models

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()  # Quantity available in stock
    
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubPart(models.Model):
    name = models.CharField(max_length=100)
    raw_materials = models.ManyToManyField(RawMaterial, through='SubPartRawMaterial')
    colors = models.ManyToManyField(Color)  # New field to store colors
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    sub_parts = models.ManyToManyField(SubPart)
    
    def __str__(self):
        return self.name

class SubPartRawMaterial(models.Model):
    sub_part = models.ForeignKey(SubPart, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity_required = models.FloatField()  # Quantity required for this sub-part

    def __str__(self):
        return f"{self.sub_part.name} requires {self.quantity_required} of {self.raw_material.name}"
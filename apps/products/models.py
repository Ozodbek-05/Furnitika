from django.db import models
from apps.pages.models import BaseModel


class CategoryModel(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class ManufacturerModel(BaseModel):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"

    def __str__(self):
        return self.title


class ColorModel(BaseModel):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=7, help_text="HTML rang kodi (#RRGGBB)")

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.title


class TagModel(BaseModel):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.title


class ProductModel(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    stock = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name="products")
    manufacturer = models.ForeignKey(ManufacturerModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    colors = models.ManyToManyField(ColorModel, blank=True, related_name="products")
    tags = models.ManyToManyField(TagModel, blank=True, related_name="products")

    rating = models.FloatField(default=0) 
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

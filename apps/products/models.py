from django.db import models
from apps.pages.models import BaseModel


class ProductCategoryModel(BaseModel):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class ManufacturerModel(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'manufacturer'
        verbose_name_plural = 'manufacturers'


class ColorModel(BaseModel):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=7, help_text="HTML rang kodi (#RRGGBB)")

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colors'


class ProductTagModel(BaseModel):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class ProductModel(BaseModel):
    class ProductStatus(models.TextChoices):
        DRAFT = 'DRAFT'
        PUBLISHED = 'PUBLISHED'
        DELETED = 'DELETED'

    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(ProductCategoryModel, on_delete=models.CASCADE, related_name="products")
    manufacturer = models.ForeignKey(ManufacturerModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    colors = models.ManyToManyField(ColorModel, blank=True, related_name="products")
    tags = models.ManyToManyField(ProductTagModel, blank=True, related_name="products")

    rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class ProductImageModel(BaseModel):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.product.title} Image"


class DealOfTheDayModel(BaseModel):
    product = models.OneToOneField(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="deal_of_the_day"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deal_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="deals/", null=True, blank=True)

    def __str__(self):
        return f"Deal for {self.product.title}"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        first_image = self.product.images.first()
        return first_image.image.url if first_image else None

    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_time and self.end_time and self.start_time <= now <= self.end_time

    @property
    def time_left(self):
        from django.utils import timezone
        now = timezone.now()
        if self.end_time and now < self.end_time:
            return self.end_time - now
        return None

    class Meta:
        verbose_name = 'deal'
        verbose_name_plural = 'deals'







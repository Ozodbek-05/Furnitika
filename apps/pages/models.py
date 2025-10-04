from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class ContactModel(BaseModel):
    full_name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(
        max_length=255, null=True, blank=True
        )
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.full_name} - {self.email}"
    

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class BannerModel(BaseModel):
    image = models.ImageField(upload_to='banners/')
    title = RichTextUploadingField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = 'banners'


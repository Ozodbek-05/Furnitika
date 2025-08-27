from django.db import models
#
# class BaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now = True)
#
#     class Meta:
#         abstract = True
#
# class AuthorsModel(BaseModel):
#     full_name = models.CharField(max_length=128)
#     bio = models.TextField()
#     email = models.EmailField(unique=True)
#     image = models.ImageField(upload_to='author_images/')
#
#     def __str__(self):
#         return self.full_name
#
#     class Meta:
#         verbose_name = 'author'
#         verbose_name_plural = 'authors'
#
#
class ContactPagesModel(models.Model):
    full_name = models.CharField(max_length = 128)
    email = models.EmailField(unique = True)
    subject = models.CharField(max_length = 128, null=True, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} -> {self.email}"

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
#
#
#
# class CategoryModel(BaseModel):
#     name = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(unique=True, blank=True, null=True)
#
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#
# class Tag(BaseModel):
#     name = models.CharField(max_length=50, unique=True)
#
#     def __str__(self):
#         return self.name
#
#     class Mete:
#         verbose_name = 'tag'
#         verbose_name_plural = 'tags'
#
#
#
# class BlogPostModel(BaseModel):
#     author = models.ForeignKey(AuthorsModel, on_delete=models.CASCADE)
#     category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, blank=True)
#     tags = models.ManyToManyField(Tag, blank=True)
#
#     title = models.CharField(max_length=255,  blank=False, null=False)
#     image = models.ImageField(upload_to='blog_images/')
#     short_description = models.TextField()
#     content = models.TextField()
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'post'
#         verbose_name_plural = 'posts'
#
#
# class CommentsModel(BaseModel):
#     author = models.ForeignKey(AuthorsModel, on_delete=models.CASCADE, related_name="comments")
#     post = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE, related_name="comments")
#     website = models.URLField(max_length=200, unique=True)
#     message = models.TextField()
#
#     def __str__(self):
#         return self.website
#
#     class Meta:
#         verbose_name = 'comment'
#         verbose_name_plural = 'comments'

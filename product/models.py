from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
# Create your models here.
class Category (MPTTModel):
    STATUS = (

      ('True', 'Evet'),
      ('False', 'Hayır'),
    )

    title = models.CharField(max_length=100)
    keywords= models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image=models.ImageField(blank=True, upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug= models.SlugField(null=False,unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:

        order_insertion_by =['title']

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Product (models.Model):
   STATUS = (

      ('True', 'Evet'),
      ('False', 'Hayır'),
   )
   category = models.ForeignKey(Category, on_delete=models. CASCADE) #relation with Category table
   title = models.CharField(max_length=150)
   keywords = models.CharField(blank=True,max_length=255)
   description = models.CharField(blank=True,max_length=255)
   image=models.ImageField(blank=True, upload_to='images/')
   price = models. FloatField()
   amount=models.IntegerField()
   detail=RichTextUploadingField()
   slug = models.SlugField(null=False,unique=True)
   status=models.CharField(max_length=10 , choices = STATUS)
   create_at = models.DateTimeField(auto_now_add=True)
   update_at=models.DateTimeField(auto_now=True)

   def __str__(self):
       return self.title
   def image_tag(self):
       return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
   image_tag.short_description = 'Image'

   def catimg_tag(selfself):
       return mark_safe((Category.status))


   def get_absolute_url(self):
      return reverse('product_detail', kwargs={'slug': self.slug})

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
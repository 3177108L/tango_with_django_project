from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    max_length = 128

    name = models.CharField(max_length = max_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length = TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.title
    


    

# class Question(models.Model):
#     question_text = models.CharField(max_length = 200)
#     pub_date = models.DateTimeField('date published')

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete = models.CASCADE)
#     choice_text = models.CharField(max_length = 200)
#     votes = models.IntegerField(default = 0)
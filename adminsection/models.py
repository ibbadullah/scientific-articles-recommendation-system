from django.db import models
from django.contrib.auth.models import User

# Model for unapproved users
class UnApprovedUsersModel(models.Model):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    sign_up_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "unapprovedusersmodel"


# Model for categories
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=200,null=True,blank=True)
    category_description = models.CharField(max_length=500, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categorymodel"

# Model for articles
class ArticlesModel(models.Model):
    Category = models.ForeignKey(CategoryModel,verbose_name="category",on_delete=models.CASCADE)
    article_title = models.CharField(max_length=200,null=True,blank=True)
    article_keywords = models.TextField(max_length=1000, null=True, blank=True)
    article_author = models.CharField(max_length=100, null=True, blank=True)
    article_content = models.TextField(max_length=12500, null=True, blank=True)
    article_image = models.ImageField(upload_to="ArticlesImages",unique=True,null=True,blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "articlesmodel"


    
    def delete(self,*args,**kwargs):
        self.article_image.delete()
        return super().delete(*args,**kwargs)


# Model for notifications for both admin and users
class NotificationModel(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    message = models.TextField(max_length=1500,null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True,default="Unread")
    generated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notificationmodel"


# Views model for storing article views
class ViewsModel(models.Model):
    Article = models.ForeignKey(ArticlesModel,verbose_name="article view",on_delete=models.CASCADE)
    User = models.ForeignKey("usersection.SignUpModel",verbose_name="user view",on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "viewsmodel"

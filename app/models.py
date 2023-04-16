from django.db import models

# Model for contact us
class ContactUsModel(models.Model):
    full_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message = models.TextField(max_length=2000,null=True,blank=True)
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contactusmodel"


# Email verification model
class EmailVerificationModel(models.Model):
    verification_key = models.CharField(max_length=32,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    status = models.CharField(max_length=15,null=True,blank=True,default="Unverified")
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "emailverificationmodel"

    def __str__(self):
        return self.verification_key


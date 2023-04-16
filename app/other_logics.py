from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
import string
from usersection.models import *
from adminsection.models import *


# Login check (Allowing only registered users to use the system)
def loginCheck(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


# Generating random string for email verification
def generateRandStr(request):
    num = 32
    randString = ""
    for n in range(num):
        limit = random.randint(0,62)
        randString = randString + string.printable[limit]
    return randString



# Email sendings function
def EmailSender(request,to,title,message,template_location,link):

    html_content = render_to_string(template_location,{"Title": title, "Message": message,"Link":link})

    text_content = strip_tags(html_content)

    sendEmail = EmailMultiAlternatives(
        # Title of the message
        title,
        # Message body
        text_content,
        # From Email
        settings.EMAIL_HOST_USER,
        # To email
        [to]
    )

    sendEmail.attach_alternative(html_content, "text/html")
    sendEmail.send()


# Email duplicate checking function
def checkEmail(request,email):
    email = email.lower()
    if SignUpModel.objects.filter(email=email).exists():
        return True
    else:
        return False


# Checking admin (This function actually finding that the logged in user is admin or a general user)
def checkAdmin(request):
    if request.user.is_admin == True and request.user.is_staff == True and request.user.is_superuser == True:
        return True
    else:
        return False


# Admin Notification function
def notifyAdmin(request,title,message):
    query = NotificationModel(title=title,message=message)
    return query.save()


# store article view
def storeArticleView(request,uId,aId):
    # first checking if the view is already counted
    if ViewsModel.objects.filter(User_id=uId,Article_id=aId).exists():
        return ""
    else:
        query = ViewsModel(User_id=uId,Article_id=aId)
        return query.save()


from .models import *
from usersection.models import *
from app.models import *


# Total dictionary
def totalsDic(request):
    totalUsers = SignUpModel.objects.all().count()
    totalUnverifiedUsers = UnApprovedUsersModel.objects.all().count()
    totalArticles = ArticlesModel.objects.all().count()
    totalCategories = CategoryModel.objects.all().count()
    totalViews = ViewsModel.objects.all().count()
    unreadNotifications = NotificationModel.objects.filter(status="Unread").count()
    totalNotifications = NotificationModel.objects.all().count()
    return {"TotalUsers":totalUsers,"TotalUnVerifiedUsers":totalUnverifiedUsers,"TotalNotifications":totalNotifications,
            "TotalArticles":totalArticles,"TotalViews":totalViews,"UnreadNotifications":unreadNotifications,"TotalCategories":totalCategories}


# Data dictionary
def dataDic(request):
    users = SignUpModel.objects.all().order_by("-id")
    unverifiedUsers = UnApprovedUsersModel.objects.filter().order_by("-id")
    articles = ArticlesModel.objects.all().order_by("-id")
    views = ViewsModel.objects.all().order_by("-id")
    allNotifications = NotificationModel.objects.all().order_by("-id")
    allMessages = ContactUsModel.objects.all().order_by("-id")
    visitedArticles = Doc2VecModel.objects.filter(User_id=request.user.id).count()
    return {"Users": users, "UnverifiedUsers": unverifiedUsers,"VisitedArticles":visitedArticles,
            "Articles": articles, "Views": views,"AllNotifications":allNotifications,"AllMessages":allMessages}




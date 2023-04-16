from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # Admin dashboard related url
    path('', adminDashboardView, name="AdminDashboard"),

    # Admin account related urls
    path('180.1.1/',AdminLoginView.as_view(),name="AdminLoginView"),
    path('admin-logout/',adminLogout,name="AdminLogout"),
    path('profile/',showAdminProfile,name="AdminProfileInfo"),
    path('update-profile/',login_required(AdminProfileUpdateView.as_view()),name="AdminProfileUpdateView"),

    # Categories related urls
    path('add-category/',login_required(AddCategoryView.as_view()),name="AddCategory"),
    path('all-categories/',showCategoriesView,name="AllCategories"),
    path('del-category/<int:id>/',deleteCategoryView,name="DeleteCategory"),
    path('update-category/<int:id>/',login_required(CategoryUpdateView.as_view()),name="UpdateCategory"),

    # Articles related urls
    path('add-article/',login_required(AddArticleView.as_view()),name="AddArticle"),
    path('all-articles/',showArticlesView,name="AllArticles"),
    path('del-article/<int:id>/',deleteArticleView,name="DeleteArticle"),
    path('update-article/<int:id>/',ArticleUpdateView.as_view(),name="UpdateArticle"),

    # Unapproved users related urls
    path('unapproved-users/',showUnapprovedUsersView,name="UnApprovedUsers"),
    path('approve-user/<int:id>/',approveUserView,name="ApproveUser"),
    path('del-una-user/<int:id>/',deleteUnapprovedUser,name="DeleteUnApprovedUser"),

    # Approved users related urls
    path('approved-users/',showApprovedUsersView,name="ApprovedUsers"),
    path('del-ap-user/<int:id>/',deleteApprovedUser,name="DeleteApprovedUser"),
    path('user-update-admin/<int:id>/',login_required(UserProfileUpdateViewAdmin.as_view()),name="UserProfileUpdateViewAdmin"),

    # Notifications related urls
    path('all-notifications/',showAllNotificationsView,name="AllNotifications"),
    path('notification/<int:id>/',notificationDetailsView,name="SingleNotification"),
    path('del-notification/<int:id>/', delnotificationView, name="DeleteNotification"),

    # Views related urls
    path('all-messages/',showAllMessages,name="AllMessages"),
    path('del-m/<int:id>/', delMessage, name="DeleteMessage"),

    # Views related urls
    path('all-views/',showAllViews,name="AllViews"),
    path('del-view/<int:id>/', delArticleView, name="DeleteViewOfArticle"),


]

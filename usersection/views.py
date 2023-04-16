from django.shortcuts import render,redirect
from django.views import View
from .models import SignUpModel
from django.contrib import messages
from app.other_logics import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from usersection.Doc2Vec.doc2vec_logics import *


# Class base view for updating the user profile
class UserProfileUpdateView(View):
    def get(self,request):
        return render(request,"userssection/userprofile.html")

    def post(self,request):
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        email = request.POST["email"].lower()
        # Matching user db email and profile form email (If it matched then it means user is just changing their name)
        if request.user.email == email:
            # Getting logged in user record by id
            query = SignUpModel.objects.get(id=request.user.id)
            query.first_name = firstName
            query.last_name = lastName
            query.save()
            messages.info(request,"Account updated successfully.")
            return redirect("UserProfileUpdateView")
        # Checking user email for duplication
        elif SignUpModel.objects.filter(email=email).exists():
            m = "Sorry, an account is already created on the current email. Please use another one."
            messages.info(request,m)
            return redirect("UserProfileUpdateView")

        else:
            query = SignUpModel.objects.get(id=request.user.id)
            query.first_name = firstName
            query.last_name = lastName
            query.email = email
            query.save()
            messages.info(request, "Account updated successfully with new email.")
            return redirect("UserProfileUpdateView")


# view for single article showing
@login_required(login_url="UserLogin")
def showSingleArticle(request,id):
    try:
        # calling storing view function
        storeArticleView(request, request.user.id,id)
        # Now selecting the article
        query = ArticlesModel.objects.get(id=id)
        # Pushing article record to the doc2vec model in order to recommend articles to the user
        doc2vecQuery = Doc2VecModel(User_id=request.user.id,Article_id=id)
        doc2vecQuery.save()
        return render(request, "publicsection/article-details.html", {"Article": query})
    except:
        return render(request,"404.html")



# view for searhing the article
@login_required(login_url="UserLogin")
def articleSearchView(request):
    try:
        if request.method == "GET":
            query = request.GET['q']
            # getting data
            query = ArticlesModel.objects.filter(Q(article_title__icontains=query)|Q(article_content__icontains=query)|Q(article_keywords__icontains=query))
            if query:
                return render(request, "userssection/articles-search-page.html", {"SearchArticles": query})
            else:
                m = "Sorry, no results found for your query."
                return render(request, "userssection/articles-search-page.html", {"Message": m})
    except:
        return render(request,"404.html")


# view for displaying all articles
@login_required(login_url="UserLogin")
def userAllArticles(request):
    query = ArticlesModel.objects.all()
    paginator = Paginator(query,9)
    page = request.GET.get('page')
    query = paginator.get_page(page)
    return render(request,'publicsection/user-all-articles.html',{"ArticlesQuery":query})

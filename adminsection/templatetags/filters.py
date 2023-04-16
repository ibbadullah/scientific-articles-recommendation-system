from django import template
from adminsection.models import *
from usersection.models import *

register = template.Library()


# Writing custom filer for counting single article views
@register.filter(name="ArticleViews")
def countArticleViews(request,articleId):
    query = ViewsModel.objects.filter(Article_id=articleId).count()
    return query

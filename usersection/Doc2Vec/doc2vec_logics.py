from adminsection.models import ArticlesModel
from usersection.models import Doc2VecModel
from django.shortcuts import render, redirect
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from django.db.models import Q
import os
import nltk
nltk.download('punkt')


# Getting all the keywords from the db of articles and storing in a file
def storeKeywords(request):
    file = open('usersection/Doc2Vec/keywords.txt','w')
    allArticles = ArticlesModel.objects.all()
    for d in allArticles:
        keywords = file.write(d.article_keywords)
    file.close()


# Getting all the keywords from the keywords.txt file for model training
def getKeywords(request):
    file = open('usersection/Doc2Vec/keywords.txt','r')
    keywords = file.read()
    file.close()
    keywords = keywords.split(',')
    return keywords


# passing data through train model
def recomendArticles(request):
    allArticles = getKeywords(request)
    data = allArticles
    # Tokenizing data. It means removing commas etc and other special characters + converting to lowercase
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

    max_epochs = 100  # number of operations. Default is 10
    vec_size = 20  # vector size
    alpha = 0.025  # learning rate


    model = Doc2Vec(size = vec_size,
                    alpha = alpha,
                    min_alpha = 0.00025, #minimum learning rate
                    min_count = 1, # count similar words only once
                    dm = 1 # defines the training algorithm. 1 means distributed memory and 0 means distributed bags
                    )

    model.build_vocab(tagged_data) # building vocabulary

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fixing the learning rate, no decay
        model.min_alpha = model.alpha

    fileName = "usersection/Doc2Vec/doc2vec.model"

    model.save(fileName)

    # Reloading the model

    model = Doc2Vec.load(fileName)

    # Getting data of the latest visited article from the database
    recentVisitedArticle = Doc2VecModel.objects.all().order_by('-id')[0]
    singleArticleQ = ArticlesModel.objects.get(id=recentVisitedArticle.Article_id)

    print("Input keywords: ",singleArticleQ.article_keywords)
    input_data = word_tokenize(singleArticleQ.article_keywords.lower())
    v1 = model.infer_vector(input_data)
    print("Vectors", v1)

    # to find most similar doc using tags
    similar_doc = model.docvecs.most_similar('1')
    print("Similar doc:",similar_doc)

    # for loop for getting matching keywords
    articleIDS = []
    similarKwrds = []
    for s in similar_doc:
        r = s[0]
        k = data[int(r)]
        similarKwrds.append(k)

        # getting ids of the articles from db through keyword
        articlesQ = ArticlesModel.objects.filter(Q(article_keywords__icontains=k))
        for a in articlesQ:
            articleIDS.append(a.id)

    # removing the same ids of the article
    ids = list(dict.fromkeys(articleIDS))
    # now getting the related articles from the db based on the doc2vec model

    recomendedArticlesQ = ArticlesModel.objects.filter(id__in=ids).order_by('-id')
    return recomendedArticlesQ



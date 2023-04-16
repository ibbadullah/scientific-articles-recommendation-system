from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .other_logics import *
from .models import ContactUsModel, EmailVerificationModel
from django.contrib.auth import logout, login, authenticate
from adminsection.models import UnApprovedUsersModel
from usersection.Doc2Vec.doc2vec_logics import *
import os


# Home view
def HomeView(request):
    # Checking user if user is logged in then allowing to the home page
    if loginCheck(request) == True:
        storeKeywords(request)
        return render(request,'publicsection/index.html',{"RecomendedArticles":recomendArticles(request)})
    else:
        return redirect('UserLogin')


# Class based view for sign up
class SignUpView1(View):
    def get(self,request):
        if loginCheck(request) == True:
            return redirect("Home")
        else:
            return render(request,'publicsection/signup-1.html')

    def post(self,request):
        if request.method == "POST":
            email = request.POST['email'].lower()
            # first checking the email in database
            if checkEmail(request,email) == True:
                m = "Sorry, the email already exists in the system. Please use another one."
                return render(request, 'publicsection/signup-1.html',{"Message":m})
            elif UnApprovedUsersModel.objects.filter(email=email).exists():
                m = "Sorry, you have already applied for the account. Please wait, the admin will approve your account very soon. Thanks for your patience."
                return render(request, 'publicsection/signup-1.html', {"Message": m})
            else:
                # calling random string generating function
                key = generateRandStr(request)
                # inserting key & email into the database
                query = EmailVerificationModel(email=email, verification_key=key)
                query.save()
                # now calling the email sending function in order to send email to the user but first preparing the details
                v_link = "http://127.0.0.1:8000/signup-step-2/" + key
                title = "Email Verification"
                message = "We received your sign up request. Please click the link and verify your email. If the link doesn't open then copy the link & paste it into a new tab."
                e_template = "emailtemplates/verification-link.html"
                EmailSender(request, email, title, message, e_template, v_link)
                # Storing user email in cookies in order to check with key in the next step
                request.session['email'] = email
                return render(request,"publicsection/email-sent-message.html")


# Class based view for verifying user email & for creating account
class SignUpView2(View):
    def get(self,request,key):
        try:
            # taking user email from cookies & storing in a variable
            email = request.session['email'].lower()
            # selecting  the latest sent key from the database
            key_query = EmailVerificationModel.objects.filter(email=email).order_by("-id")[0]
            # checking db key with link key
            if str(key_query) == str(key):
                query = EmailVerificationModel.objects.get(verification_key=key, email=email)
                query.status = "Verified"
                query.save()
                return render(request, 'publicsection/signup-2.html', {"Email": email,"Key":key})
            else:
                m = "Sorry the link is not valid."
                return render(request, "publicsection/signup-1.html", {"Message": m})
        except:
            m = "Sorry, the link is not valid."
            return render(request, "publicsection/signup-1.html", {"Message": m})



    def post(self,request,key):
        if request.method == "POST":
            firstName = request.POST["first_name"]
            lastName = request.POST["last_name"]
            username = request.POST["username"].lower()
            email = request.POST["email"].lower()
            password = request.POST["password"]
            v_key = request.POST["key"]

            # checking username in both places
            if SignUpModel.objects.filter(username=username).exists():
                m = "Sorry, the username is already taken. Please use another one."
                return render(request,"publicsection/signup-2.html",{"Message":m,"Email":email,"Key":v_key})
            elif UnApprovedUsersModel.objects.filter(username=username).exists():
                m = "Sorry, the username is already taken. Please use another one."
                return render(request, "publicsection/signup-2.html", {"Message": m, "Email": email, "Key": v_key})
            else:
                # creating unverified account for user
                query = UnApprovedUsersModel(first_name=firstName,last_name=lastName,username=username,email=email,password=password)
                query.save()
                # Now deleting all the keys from the db for this user & also deleting user email from the cookies
                deleteKeys = EmailVerificationModel.objects.filter(email=email)
                deleteKeys.delete()
                del request.session['email']
                # calling notifyAdmin function in order to notify the admin about the new signup request
                title = "A New Signup Request Received"
                message = "A new signup request has been received from "+firstName+" "+lastName+". Please approve the user if doesn't violate the SARS policy."
                notifyAdmin(request,title,message)
                return render(request,"publicsection/account-created-message.html")





# Class based view for users login
class UsersLoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            return render(request,'publicsection/login.html')

    def post(self,request):
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('Home')
            else:
                m = "Sorry, your email or password is incorrect."
                return render(request,'publicsection/login.html',{"Message":m})


# Class based view for contact us
class ContactUsView(View):
    def get(self,request):
        return render(request,'publicsection/contact-us.html')

    def post(self,request):
        if request.method == "POST":
            fullName = request.POST['full_name']
            email = request.POST['email']
            message = request.POST['message']
            query = ContactUsModel(full_name=fullName,email=email,message=message)
            query.save()
            if query:
                # notifying admin about the message
                title = "A new message received"
                mText = "A new message has received from "+fullName+". Please read the message & give a response to the user."
                notifyAdmin(request,title,mText)
                m = "Thank you for your message. We received your message. We will respond to you as soon as possible."
                return render(request,"publicsection/contact-us.html",{"Message":m})
            else:
                m = "Sorry, something went wrong."
                return render(request, "publicsection/contact-us.html", {"Message": m})



# Function based view for about us
def aboutUs(request):
    return render(request,'publicsection/about-us.html')


# Function based view for privacy policy
def privacyPolicy(request):
    return render(request,'publicsection/privacy-policy.html')


# logout view
def logoutView(request):
    logout(request)
    return render(request,'publicsection/logout.html')

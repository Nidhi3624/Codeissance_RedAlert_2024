from django.shortcuts import render, get_object_or_404, reverse
from myapp.models import Contact, Dish, Team, Category, Profile, Order
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import requests
from django.http import JsonResponse

from .models import Category
from newsapi import NewsApiClient

from .chatbot import generate_api_response

# def index(request):
#     context ={}
#     cats = Category.objects.all().order_by('name')
#     context['categories'] = cats
#     # print()
#     dishes = []
#     for cat in cats:
#         dishes.append({
#             'cat_id':cat.id,
#             'cat_name':cat.name,
#             'cat_img':cat.image,
#             'items':list(cat.dish_set.all().values())
#         })
#     context['menu'] = dishes

#     return render(request,'index.html', context)




def index(request):
    context = {}
    cats = Category.objects.all().order_by('name')
    context['categories'] = cats
    
    dishes = []
    for cat in cats:
        dishes.append({
            'cat_id': cat.id,
            'cat_name': cat.name,
            'cat_img': cat.image,
            'items': list(cat.dish_set.all().values())
        })
    context['menu'] = dishes

    # Add news API functionality
    # newsapi = NewsApiClient(api_key='aa908021ff1c4dd4a032f3ecb4942bd3')
    # top_headlines = newsapi.get_top_headlines(country='us', language='en', page_size=5)
    # context['articles'] = top_headlines['articles']

    # # def get_faang_job_news():
    # #     newsapi = NewsApiClient(api_key='aa908021ff1c4dd4a032f3ecb4942bd3')
    
    # #     # Define keywords related to placements, jobs, and FAANG companies
    # #     keywords = 'jobs OR placements'
    
    # #     # Get news articles
    # #     all_articles = newsapi.get_everything(q=keywords,
    # #                                       language='en',
    # #                                       sort_by='publishedAt',
    # #                                       page_size=5)
    
    # #     return all_articles['articles']
    # # # Usage
    # # context = {}
    # # context['articles'] = get_faang_job_news()

    # return render(request, 'index.html', context)
    def get_placement_interview_news():
        newsapi = NewsApiClient(api_key='aa908021ff1c4dd4a032f3ecb4942bd3')
        
        # Define keywords related to placements and interviews
        keywords = 'engineering OR microsoft OR oracle  '
        
        # Get news articles
        all_articles = newsapi.get_everything(q=keywords,
                                              language='en',
                                              sort_by='publishedAt',
                                              page_size=10)  # Increased to 10 articles
        
        return all_articles['articles']

    # Fetch placement and interview news
    context['articles'] = get_placement_interview_news()

    return render(request, 'index.html', context)


def contact_us(request):
    context={}
    if request.method=="POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        msz = request.POST.get("message")
        
        obj = Contact(name=name, email=em, subject=sub, message=msz)
        obj.save()
        context['message']=f"Dear {name}, Thanks for your time!"

    return render(request,'contact.html', context)

def about(request):
    return render(request,'about.html')

def feature(request):
    return render(request, 'feature.html')

def team_members(request):
    context={}
    members = Team.objects.all().order_by('name')
    context['team_members'] = members
    return render(request,'team.html', context)

def all_dishes(request):
    context={}
    dishes = Dish.objects.all()
    if "q" in request.GET:
        id = request.GET.get("q")
        dishes = Dish.objects.filter(category__id=id)
        context['dish_category'] = Category.objects.get(id=id).name 

    context['dishes'] = dishes
    return render(request,'all_dishes.html', context)

def register(request):
    context={}
    if request.method=="POST":
        #fetch data from html form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        contact = request.POST.get('number')
        check = User.objects.filter(username=email)
        if len(check)==0:
            #Save data to both tables
            usr = User.objects.create_user(email, email, password)
            usr.first_name = name
            usr.save()

            profile = Profile(user=usr, contact_number = contact)
            profile.save()
            context['status'] = f"User {name} Registered Successfully!"
        else:
            context['error'] = f"A User with this email already exists"

    return render(request,'register.html', context)

def check_user_exists(request):
    email = request.GET.get('usern')
    check = User.objects.filter(username=email)
    if len(check)==0:
        return JsonResponse({'status':0,'message':'Not Exist'})
    else:
        return JsonResponse({'status':1,'message':'A user with this email already exists!'})

def signin(request):
    context={}
    if request.method=="POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        check_user = authenticate(username=email, password=passw)
        if check_user:
            login(request, check_user)
            if check_user.is_superuser or check_user.is_staff:
                return HttpResponseRedirect('/admin')
            return HttpResponseRedirect('/dashboard')
        else:
            context.update({'message':'Invalid Login Details!','class':'alert-danger'})

    return render(request,'login.html', context)

def dashboard(request):
    context={}
    login_user = get_object_or_404(User, id = request.user.id)
    #fetch login user's details
    profile = Profile.objects.get(user__id=request.user.id)
    context['profile'] = profile

    #update profile
    if "update_profile" in request.POST:
        print("file=",request.FILES)
        name = request.POST.get('name')
        contact = request.POST.get('contact_number')
        add = request.POST.get('address')
       

        profile.user.first_name = name 
        profile.user.save()
        profile.contact_number = contact 
        profile.address = add 

        if "profile_pic" in request.FILES:
            pic = request.FILES['profile_pic']
            profile.profile_pic = pic
        profile.save()
        context['status'] = 'Profile updated successfully!'
    
    #Change Password 
    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = login_user.check_password(c_password)
        if check==True:
            login_user.set_password(n_password)
            login_user.save()
            login(request, login_user)
            context['status'] = 'Password Updated Successfully!' 
        else:
            context['status'] = 'Current Password Incorrect!'

    #My Orders 
    orders = Order.objects.filter(customer__user__id=request.user.id).order_by('-id')
    context['orders']=orders    
    return render(request, 'dashboard.html', context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def single_dish(request, id):
    context={}
    dish = get_object_or_404(Dish, id=id)

    if request.user.is_authenticated:
        cust = get_object_or_404(Profile, user__id = request.user.id)
        order = Order(customer=cust, item=dish)
        order.save()
        inv = f'INV0000-{order.id}'

        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':dish.discounted_price,
            'item_name':dish.name,
            'user_id':request.user.id,
            'invoice':inv,
            'notify_url':'http://{}{}'.format(settings.HOST, reverse('paypal-ipn')),
            'return_url':'http://{}{}'.format(settings.HOST,reverse('payment_done')),
            'cancel_url':'http://{}{}'.format(settings.HOST,reverse('payment_cancel')),
        }

        order.invoice_id = inv 
        order.save()
        request.session['order_id'] = order.id

        form = PayPalPaymentsForm(initial=paypal_dict)
        context.update({'dish':dish, 'form':form})

    return render(request,'dish.html', context)

def payment_done(request):
    pid = request.GET.get('PayerID')
    order_id = request.session.get('order_id')
    order_obj = Order.objects.get(id=order_id)
    order_obj.status=True 
    order_obj.payer_id = pid
    order_obj.save()

    return render(request, 'payment_successfull.html') 

def payment_cancel(request):
    ## remove comment to delete cancelled order
    # order_id = request.session.get('order_id')
    # Order.objects.get(id=order_id).delete()

    return render(request, 'payment_failed.html') 




# def chatbot_response(request):
#     if request.method == 'POST':
#         query = request.POST.get('query', '')
#         response = generate_api_response(query)
#         return JsonResponse({'response': response})
#     return JsonResponse({'error': 'Invalid request method'})

def chatbot_response(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')  # Retrieve the user's query from the POST request
        response = generate_api_response(query)  # Generate a response using an API function
        return JsonResponse({'response': response})  # Return the response as JSON
    return JsonResponse({'error': 'Invalid request method'})  # Handle invalid request methods



def mentor_index(request):
    return render(request,'mentor_index.html')

def mentor_userProfile(request):
    return render(request,'mentor_userProfile.html')

def courses_index(request):
    return render(request,'courses_index.html')

def courses_list(request):
    return render(request,'courses_list.html')

def courses_quiz(request):
    return render(request,'courses_quiz.html')


from django.shortcuts import render,redirect
from .models import * 
from .forms import * 
# Create your views here.

def forum_index(request):
    forums=forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())

    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'forum_index.html',context)

def addInForum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request,'addInForum.html',context)

def addInDiscussion(request):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request,'addInDiscussion.html',context)
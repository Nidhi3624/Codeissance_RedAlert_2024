from django.contrib import admin
from django.urls import path, include
from myapp import views 
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('contact/',views.contact_us,name="contact"),
    path('about/',views.about,name="about"),
    path('team/',views.team_members,name="team"),
    path('dishes/',views.all_dishes,name="all_dishes"),
    path('register/',views.register,name="register"),
    path('check_user_exists/',views.check_user_exists,name="check_user_exist"),
    path('login/', views.signin, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('dish/<int:id>/', views.single_dish, name='dish'),

    path('paypal/',include('paypal.standard.ipn.urls')),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('feature/', views.feature, name="feature"),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path('mentor_index/', views.mentor_index, name='mentor_index'),
    path('mentor_userProfile/mentor_index/',views.mentor_index, name='mentor_index'),
    path('mentor_userProfile/', views.mentor_userProfile, name='mentor_userProfile'),
    path('mentor_index/mentor_userProfile/',views.mentor_userProfile, name='mentor_userProfile'),
    path('courses_index/', views.courses_index, name='courses_index'),
    path('courses_list/', views.courses_list, name='courses_list'),
    path('courses_quiz/', views.courses_quiz, name='courses_quiz'),
    path('forum_index',views.forum_index,name='forum_index'),
    path('addInForum/',views.addInForum,name='addInForum'),
    path('addInDiscussion/',views.addInDiscussion,name='addInDiscussion'),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [ 
    path('',login,name='login'),
    path('Dashboard/',Dashboard,name='Dashboard'),
    path('AddGuide/',AddGuide,name='AddGuide'),
    path('Guides/',Guides,name='Guides'),
    path('user/',user,name='user'),
    path('operator/',operator,name='operator'),
    path('updateGuide/<int:updateID>',updateGuide,name="updateGuide"),
    path('unpublish_guide/<int:UnpublishID>',unpublish_guide,name="unpublish_guide"),
    path('publish_guide/<int:publishID>',publish_guide,name="publish_guide"),
    path('full_description/<int:descID>',full_description,name="full_description"),
    path('full_message/<int:MsgID>',full_message,name="full_message"),
    path('delete_Guide/<int:guideID>',delete_Guide,name="delete_Guide"),
    path('Message/',Message,name='Message'),
    path('delete_msg/<int:msgID>',delete_msg,name="delete_msg"),
    path('delete_user/<int:userID>',delete_user,name="delete_user"),
    path('updateUser/<int:upID>',updateUser,name="updateUser"),
    path('logout/',logout,name='logout'),

    #API
    path('register/',register.as_view()),
    path('customer_login/',csrf_exempt(customer_login),name='customer_login'),
    path('Queries/',QueriesListView.as_view()),
    path('CreateQuery/',QueriesCreateView.as_view()),
    path('AllGuides/',GuideListView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('Updateuser/<id>/', UserUpdateView.as_view()),
    
   ]
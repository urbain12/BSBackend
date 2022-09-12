from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
from django.db.models import Q
# from .utils import cartData, check_transaction, check_instalment
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .models import *

# from dateutil.relativedelta import *
from django.contrib.auth import (
    authenticate,
    logout as django_logout,
    login as django_login,
)
from django.shortcuts import render, redirect
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core import serializers
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta
import json
from django.contrib import messages
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
import os
import csv


# Users
def operator(request):
    if request.method == "POST":
        try:
            user1 = User.objects.get(email=request.POST["email"])
            return render(
                request, "operator.html", {"error": "The Email  has already been taken"}
            )
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST["phonenumber"])
                return render(
                    request,
                    "operator.html",
                    {"error": "The phone number  has already been taken"},
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.POST["firstname"],
                    LastName=request.POST["lastname"],
                    MName=request.POST["MName"],
                    FName=request.POST["FName"],
                    Weight=request.POST["weight"],
                    Height=request.POST["weight"],
                    DOB=request.POST["DOB"],
                    email=request.POST["email"],
                    phone=request.POST["phonenumber"],
                    password=request.POST["password"],
                )
            return redirect("user")
    else:
        return render(request, "operator.html")


@login_required(login_url="/login")
def user(request):
    users = User.objects.all()
    search_query = request.GET.get("search", "")
    if search_query:
        users = User.objects.filter(Q(phone__icontains=search_query))
    paginator = Paginator(users, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "users.html", {"users": users, "page_obj": page_obj})


@login_required(login_url="/login")
def updateUser(request, upID):
    updateuser = User.objects.get(id=upID)
    if request.method == "POST":
        updateuser.FirstName = request.POST["firstname"]
        updateuser.LastName = request.POST["lastname"]
        updateuser.MName = request.POST["MName"]
        updateuser.FName = request.POST["FName"]
        updateuser.Weight = request.POST["weight"]
        updateuser.Height = request.POST["height"]
        updateuser.DOB = request.POST["dob"]
        updateuser.phone = request.POST["phonenumber"]
        updateuser.email = request.POST["email"]
        updateuser.save()
        # Addproduct = True
        return redirect("user")
    else:
        return render(request, "updatemembers.html", {"updateuser": updateuser})


def delete_user(request, userID):
    user = User.objects.get(id=userID)
    user.delete()
    return redirect("user")


def login(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST["email"], password=request.POST["password"]
        )
        if customer is not None:
            django_login(request, customer)
            return redirect("Dashboard")
        else:
            return render(
                request,
                "Login.html",
                {"error": "Your Email or Password are incorrect. "},
            )
    else:
        return render(request, "Login.html")


@login_required(login_url="/login")
def logout(request):
    django_logout(request)
    return redirect("login")


class register(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        print(request.data)
        try:
            user1 = User.objects.get(email=request.data["email"])
            response = {
                "status": "Failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "A user with that email already exists!",
                "data": [],
            }

            return Response(response)
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.data["phone"])
                response = {
                    "status": "Failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "A user with that phone number already exists!",
                    "data": [],
                }

                return Response(response)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.data["FirstName"],
                    LastName=request.data["LastName"],
                    MName=request.data["MName"],
                    FName=request.data["FName"],
                    Weight=request.data["Weight"],
                    Height=request.data["Height"],
                    DOB=request.data["DOB"],
                    email=request.data["email"],
                    phone=request.data["phone"],
                    password=request.data["password"],
                )
                response = {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Child Registered successfully!!!",
                    "data": [],
                }

                return Response(response)


def customer_login(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(phone=body["phone"])
            if user.check_password(body["password"]):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    "user_id": user.id,
                    "email": user.email,
                    "status": "success",
                    "token": str(token),
                    "code": status.HTTP_200_OK,
                    "message": "Login successfull",
                    "data": [],
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json")
            else:
                data = {
                    "status": "failure",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Phone or password incorrect!",
                    "data": [],
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type="application/json")
        except User.DoesNotExist:
            data = {
                "status": "failure",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Phone or password incorrect!",
                "data": [],
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type="application/json")


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.data["user_id"])
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password ChangePasswupdated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"


# CMS

# Dashboard


@login_required(login_url="/login")
def Dashboard(request):
    alllist = len(User.objects.all())
    return render(
        request,
        "dashboard.html",
        {
            "alllist": alllist,
        },
    )


# Guides


@login_required(login_url="/login")
def AddGuide(request):
    if request.method == "POST":

        Addguide = Guide()
        Addguide.Title = request.POST["title"]
        Addguide.SubTitle = request.POST["sTitle"]
        Addguide.Description = request.POST["description"]
        Addguide.save()
        return redirect("Guides")
    else:
        return render(request, "Addnewguide.html")


@login_required(login_url="/login")
def Guides(request):
    guides = Guide.objects.all()
    search_query = request.GET.get("search", "")
    if search_query:
        guides = Guide.objects.filter(Q(Title__icontains=search_query))
    paginator = Paginator(guides, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "Guides.html", {"guides": guides, "page_obj": page_obj})


@login_required(login_url="/login")
def updateGuide(request, updateID):
    updateguide = Guide.objects.get(id=updateID)
    if request.method == "POST":
        updateguide.Title = request.POST["title"]
        updateguide.Description = request.POST["description"]
        updateguide.SubTitle = request.POST["STitle"]
        updateguide.save()
        return redirect("Guides")
    else:
        return render(request, "updateguide.html", {"updateguide": updateguide})


def full_description(request, descID):
    desc = Guide.objects.get(id=descID)
    return render(request, "fullDesc.html", {"desc": desc})


@login_required(login_url="/login")
def unpublish_guide(request, UnpublishID):
    unpublish = Guide.objects.get(id=UnpublishID)
    unpublish.Publish = True
    unpublish.save()
    return redirect("Guides")


@login_required(login_url="/login")
def publish_guide(request, publishID):
    publish = Guide.objects.get(id=publishID)
    publish.Publish = False
    publish.save()
    return redirect("Guides")


def delete_Guide(request, guideID):
    Guides = Guide.objects.get(id=guideID)
    Guides.delete()
    return redirect("Guides")


# Queries


@login_required(login_url="/login")
def Message(request):
    querries = Queries.objects.all().order_by("-id")
    search_query = request.GET.get("search", "")
    if search_query:
        querries = Queries.objects.filter(Q(fullname__icontains=search_query))
    paginator = Paginator(querries, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "Message.html", {"querries": querries, "page_obj": page_obj})


def full_message(request, MsgID):
    Msg = Queries.objects.get(id=MsgID)
    return render(request, "fullMsg.html", {"Msg": Msg})


def delete_msg(request, msgID):
    Msg = Queries.objects.get(id=msgID)
    Msg.delete()
    return redirect("Message")


# API
class GuideListView(ListAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

class GetGuideListView(ListAPIView):
    serializer_class = GuideSerializer
    def get_queryset(self):
        return Guide.objects.filter(Title="Imirire")


class QueriesCreateView(CreateAPIView):
    queryset = Queries.objects.all()
    serializer_class = QueriesSerializer


class Querieslistbyid(ListAPIView):
    serializer_class = QueriesSerializer
    
    def get_queryset(self):
        return Queries.objects.filter(user=self.kwargs['user_id'])

class GetchildbyId(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['user_id'])


def reply(request, requestID):
    if request.method == 'POST':
        print('replyreply reply')
        req = Queries.objects.only('id').get(
            id=requestID)
        req.reply = request.POST['Msg']
        req.replied = True
        req.save()
        payload={'details':f'Dear {req.FirstName},\n we received your message, Here is our reply {req.reply}.','phone_number':'250787018287'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)
        return redirect('Message')
    else:
        message = Queries.objects.get(id=requestID)
        return render(request, 'reply.html', {'message': message})


def AddVaccine(request):
    if request.method == 'POST':
        print('working')
        AddVaccines = Vaccines()
        AddVaccines.Vaxtype = request.POST['vax']
        if request.POST['user'] != '':
            user = User.objects.get(
                id=int(request.POST['user']))
            AddVaccines.user = user
        AddVaccines.save()
        return redirect('Vaccination')
    else:
        vaccines_=Vaccines.objects.all()
        users_=[]
        for vax in vaccines_:
            users_.append(vax.user.id)
        users=User.objects.exclude(id__in=users_)
        vaccines=['Birth','SixWeeks','TenWeeks','FourteenWeeks','NineMonths','FifteenMonths']
        return render(request, 'AddnewVaccine.html', {'users': users,'vaccines':vaccines})


def add_vaccine(request,userID):
    user = User.objects.get(id=userID)
    if request.method == 'POST':
        print('working')
        AddVaccines = Vaccines()
        AddVaccines.Vaxtype = request.POST['vax']
        AddVaccines.user = user
        AddVaccines.save()
        return redirect('Vaccination')
    else:
        
        vaccines=user.remVax.split(", ")
        return render(request, 'add_vaccine.html', {'user': user,'vaccines':vaccines})


@login_required(login_url="/login")
def Vaccination(request):
    users = User.objects.all()
    search_query = request.GET.get("search", "")
    if search_query:
        users = User.objects.filter(
                Q(FirstName__icontains=search_query))
       
        
    paginator = Paginator(users, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "Vaccination.html", {"users": users, "page_obj": page_obj})


@login_required(login_url='/login')
def Reports(request, UserID):
    user = User.objects.get(id=UserID)
    vaccines = Vaccines.objects.filter(
        user=UserID)
    return render(request, 'ChildReport.html', {'user': user, 'vaccines': vaccines})


def export_report_csv(request, UserID):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    customer = User.objects.get(id=UserID)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{customer.FirstName} {customer.LastName} Vaccine Report - {ondate}.csv"'
    writer = csv.writer(response)
    writer.writerow([

        'Isaro App'
    ])
    writer.writerow([
    

                str(customer.FirstName) +' '+str(customer.LastName)+
                ' ' "Vaccination Report"

    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    
    writer.writerow(['Types',
                    'date' ])
                    
    customer = User.objects.filter(id=UserID)
    payments = Vaccines.objects.filter(
        user=UserID)
    instalments = []
    for sub in payments:

        transactions = [
            
            sub.Vaxtype,
            sub.added_at.strftime("%Y-%m-%d"),
        ]

        print(transactions)
        print(type(transactions))
        instalments.append(transactions)
    for user in instalments:
        writer.writerow(user)

    return response


class VaxlistbyID(ListAPIView):
    serializer_class = VaxSerializer
    
    def get_queryset(self):
        return Vaccines.objects.filter(user=self.kwargs['user_id'])
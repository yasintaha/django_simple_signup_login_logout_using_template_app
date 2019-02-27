from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import SignupSerializer

# pyrebase package for FCM configuration
import pyrebase

# your FCM credentials
config = {
    "apiKey" : "<your FCM API key>",
    "authDomain" : "<your FCM authdomain>",
    "databaseURL" : "<your FCM databseURL>",
    "projectId" : "<your FCM projectID>",
    "storageBucket" : "<your FCM storage bucket name>",
    "messagingSenderId" : "<your FCM message SenderID>"
  }

firebase = pyrebase.initialize_app(config)

# for login,signup into FCM, auth initialization
authe = firebase.auth()

# FCM database initialization
database = firebase.database()


class SignupView(APIView):
    serializer_class = SignupSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data['name']
            email = serializer.data['email']
            password = serializer.data['password']

            try:
                # creating user with respective email and password
                user = authe.create_user_with_email_and_password(email,password)
                uid = user['localId']
                data = {'name':name,'status':"1"}
                # creating a database for the users detail on FCM platform
                database.child("users").child(uid).child("details").set(data)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            except:
                message = {"message":"unable to create"}
                return Response(serializer.errors,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

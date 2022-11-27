from django.shortcuts import render
from rest_framework.views import APIView
from api.models import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from api.helpers.authenticate import generate, generate_temporary_password, decode_token, blackListToken, \
    validate_decoded_token
# Create your views here.

class RegisterViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def post(self, request, call_center_id=None):
        '''
        API Call to create users and save token.
        request: email, username, password
        request body: {
                        id: '',
                        firstName: '', - User
                        lastName: '', - User
                        role: '', - UserCallCenterRole
                        hasAccessAnywhere: false,
                        hasViewCallCenterTotalsOnDashboard: false,
                        title: '',
                        reportsTo: '',
                        userName: '', - User
                        email: '', - User
                        mobilePhone: '',
                        status: true,
                        team: '', - UserProfile team_id
                    }
        '''
        print("Create new user")

        request.data["password"] = request.data["password"]
        request.data["username"] = request.data["username"]

        if request.data.get("username") != "":
            users = User.objects.filter(username=request.data.get("username"))

            if users.exists():
                return Response({"status": "Failed", "message": "User with that username already exists."},
                                status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"status": "Failed", "message": "User creation unsuccessful."},
                            status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(serializer.validated_data)

        if user:
            serializer = UserSerializer(user, context={"request": request})
            token, created = Token.objects.get_or_create(user=user)
        
    
        return Response({"status": "Success", "message": "User Successfully created",
                        "data": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
    
        username = request.data["username"]
        password=request.data["password"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            return Response({"status": "Failed", "message": "Username not found.", "error_message": str(e)},status=status.HTTP_403_FORBIDDEN)


        if user:
           
       
            if not user.check_password(password):
                return Response({"status": "Failed", "message": "Password is incorrect."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            token = Token.objects.get(user=user)
            if token:
                access_token = generate(user, user.username, password)
        else:
            return Response({"status": "Failed", "message": "This user doesn't exists."})
        
        return Response({"status": "Success", "message": "Login Successful",
                        "token": access_token["access"],}, status=status.HTTP_202_ACCEPTED)
       

class TaskView(APIView):


    def get(self, request):
        isTokenValid, decoded_token = validate_decoded_token(request)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            todo=Todolist.objects.filter(user=current_agent)
            serializer=TodolistSerializer(todo,many=True)
            return Response({"status": "Success", "message": "your list my highness",
                        "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"status": "failed", "message": "Something went wrong. {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


      
    def post(self, request):
        isTokenValid, decoded_token = validate_decoded_token(request)
        agentId = decoded_token["user_id"]
        current_agent = User.objects.get(pk=agentId)
        if not isTokenValid:
            return Response({"status": "failed", "message": "You are not authorized to view this page. Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            if request.data["todo_id"]:
                todo=Todolist.objects.get(pk=request.data["todo_id"])
                tasks=Tasks.objects.filter(todo=todo).update(active=False)
                tasks=request.data["tasks"]
                print("taskss",tasks)
                i=1
                for g in tasks:
                
                    if g["id"]:
                        print("to change")
                        task=Tasks.objects.get(pk=g["id"])
                        task.active=True
                        task.name=g["name"]
                        task.priority=i
                        task.save()
                    else:
                        task=Tasks.objects.create(todo=todo,name=g["name"],priority=i,status=g["status"],active=True)
                    i+=1
            else:
                todo=Todolist.objects.create(name=request.data["todo_name"],user=current_agent)
                tasks=request.data["tasks"]
                i=1
                for g in tasks:
                    task=Tasks.objects.create(todo=todo,name=g["name"],priority=i,status=g["status"],active=True)
                    i+=1
            serializer= TodolistSerializer(todo)
            return Response({"status": "Success", "message": "Here is your new Todo",
                            "DATA":serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
                return Response({"status": "failed", "message": "Something went wrong. {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
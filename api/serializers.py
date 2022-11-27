
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "password"]

        extra_kwargs = {
            'password': {'write_only': True}
        }
          
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class TodolistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = "__all__"

          
    def to_representation(self, instance):
        Task = Tasks.objects.filter(todo=instance,active=True).order_by('priority')
        response = super().to_representation(instance)
        if Task.count()==1:
            print("here")
            print("task",Task)
            
            response["tasks"] = TaskSerializer(Task[0]).data
        else:
            response["tasks"] = TaskSerializer(Task,many=True).data

        return response


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"
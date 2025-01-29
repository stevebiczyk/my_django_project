# tasks/serializers.py
from rest_framework import serializers
from .models import Project, Task, Comment, TaskAttachment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']

class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.ReadOnlyField(source='uploaded_by.username')

    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'uploaded_by', 'uploaded_by_username', 'uploaded_at', 'description']
        read_only_fields = ['uploaded_by']

class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'assigned_to_username',
                 'created_by', 'created_by_username', 'priority', 'status', 'due_date',
                 'created_at', 'updated_at', 'completed_at', 'comments', 'attachments']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'completed_at']

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username')
    members_detail = UserSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 
                 'owner', 'owner_username', 'members', 'members_detail', 'tasks']
        read_only_fields = ['owner', 'created_at', 'updated_at']
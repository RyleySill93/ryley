from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Node, Account


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'left', 'right']


class AccountSerializer(serializers.ModelSerializer):
    tag = NodeSerializer()
    class Meta:
        model = Account
        fields = ['id', 'name', 'normal_balance', 'tag']


class AccountView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

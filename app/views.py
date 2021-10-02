# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .models import *

@api_view(['GET'])
def api_over_view(request):
    api_urls = {
        'login': '/api/v1/token/',
        'refresh': '/api/v1/token/refresh/',
        'register': '/api/v1/register/',

        'list snippet': '/api/v1/list/snippet/',
        'detail snippet': '/api/v1/detail/snippet/<id>/',
        'create snippet' : '/api/v1/create/snippet/',
        'delete snippet' : '/api/v1/delete/snippet/<id>/',
        'update snippet' : '/api/v1/update/snippet/<id>/',

        'list tag': '/api/v1/list/tag/',
        'detail tag': '/api/v1/detail/tag/<id>/',

        'list_users': '/api/v1/users/',
    }
    return  Response(api_urls, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        srzl = UserRegisterSerializer(data=request.data)
        
        if not srzl.is_valid():
            data = {'error': 'Something went wrong!'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        srzl.save()

        user = User.objects.get(username=srzl.data['username'])
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def snippet_list(request):
    try:
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        return Response(serializer.data, status=200)
    except:
        data = {'error': 'Something went wrong!'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def snippet_detail(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
        serializer = SnippetDetailSerializer(snippet, context={'request': request})
        return Response(serializer.data, status=200)
    except:
        data = {'error': 'Something went wrong!'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def create_snippet(request):
    if request.method == 'POST':
        tag = request.data['tag']
        user_name = request.data['user']
        title = request.data['title']
        snippet = request.data['snippet']

        if Tag.objects.filter(name=tag).exists():
            tag_id = Tag.objects.get(name=tag)
        else:
            tag_id = Tag.objects.create(name=tag)
        
        request.data['tag'] = tag_id

        try:
            user = User.objects.get(username=user_name)
            snippet = Snippet.objects.create(tag=tag, user=user, title=title, snippet=snippet)
        except User.DoesNotExist:
            data = {'error': 'Something went wrong!'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        data = {'success' : 'Snippet successfully added'}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def delete_snippet(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
        snippet.delete()
        data = {'deleted': 'Snippet successfully deleted'}
        return Response(data, status=200)
    except:
        data = {'error': 'Something went wrong!'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
def update_snippet(request, id):
    if request.method == 'GET':
        try:
            snippet = Snippet.objects.get(id=id)
            srzl = SnippetSerializer(snippet)
            return Response(srzl.data, status=200)
        except:
            return Response({'error' : 'Something went wrong'}, status=403)

    if request.method == 'POST':
        try:
            tag = Tag.objects.get(name=request.data['tag'])
            user = User.objects.get(username=request.data['user'])
            
            snippet = Snippet.objects.get(id=id)
            snippet.tag = tag
            snippet.user = user
            snippet.title = request.data['title']
            snippet.snippet = request.data['snippet']
            snippet.save()

            data = {'success': 'Snippet successfully updated'}
            return Response(data, status=200)
        except:
            data = {'error': ' Something went wrong'}
            return Response(data, status=200)

"""

{
    "username" : "athif",
    "email" : "athif@gmail.com",
    "password" : "xzaq1234",
    "confirm_password" : "xzaq1234"
}

{
    "tag" : "one",
    "user" : "shareef",
    "title" : "one",
    "snippet" : "good morning"
}

"""
@api_view(['GET'])
def tag_list(request):
    try:
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data, status=200)
    except:
        data = {'error': 'Something went wrong!'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
def tag_detail(request, id):
    try:
        tag = Tag.objects.get(id=id)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=200)
    except:
        data = {'error': 'Something went wrong!'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

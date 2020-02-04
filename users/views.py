import json

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegistration, UserLogin, UserEditProfile, UserChangePassword

def str_date(date):
    return str(date.replace(tzinfo=None, microsecond=0))

def user_model_to_json(user):
    return {
        'kind': 'user',
        'id': user.id,
        'username': user.username, 
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created': str_date(user.date_joined),
    }

@csrf_exempt
def all_users(request):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            response = {
                    'kind': 'error',
                    'errors': {
                        'request':[
                            {
                            'message': 'You are not logged in.',
                            'code': 'auth'
                            }
                        ]
                            
                    }
                }
            return HttpResponse(json.dumps(response) , content_type='application/json', status=401)
        
        user = User.objects.get(username=request.user)
        
        return JsonResponse(user_model_to_json(user))

    elif request.method == 'POST':

        #validate input
        user = UserRegistration(json.loads(request.body))
        if not user.is_valid():
            
            response = {
                'kind' : 'error',
                'errors' : json.loads(user.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        #create new object
        model = User(**user.cleaned_data)
        model.set_password(user.cleaned_data['password'])

        #save object to database
        model.save()
        
        return JsonResponse(user_model_to_json(model))

    elif request.method == 'PUT':

        if not request.user.is_authenticated:
            response = {
                    'kind': 'error',
                    'errors': {
                        'request':[
                            {
                            'message': 'You are not logged in.',
                            'code': 'auth'
                            }
                        ]
                            
                    }
                }
            return HttpResponse(json.dumps(response) , content_type='application/json', status=401)

        #validate input
        form = UserEditProfile(json.loads(request.body), instance=request.user)

        if not form.is_valid():
            response = {
                'kind': 'error',
                'errors' : json.loads(form.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        #Save to database
        form.save()

        model = User.objects.get(username=form.cleaned_data['username'])

        return JsonResponse(user_model_to_json(model))

    elif request.method == 'DELETE':

        if not request.user.is_authenticated:
            response = {
                    'kind': 'error',
                    'errors': {
                        'request':[
                            {
                            'message': 'You are not logged in.',
                            'code': 'auth'
                            }
                        ]
                            
                    }
                }
            return HttpResponse(json.dumps(response) , content_type='application/json', status=401)

        user = User.objects.get(username=request.user.get_username())
        logout(request)
        
        user.delete()

        return HttpResponse(status=204)
    
    else:
        return HttpResponseNotAllowed(['POST', 'GET', 'PUT', 'DELETE'])

@csrf_exempt
def login_user(request):

    if request.method == 'POST':

        form = UserLogin(json.loads(request.body))

        if not form.is_valid():
            response = {
                'kind' : 'error',
                'error' : json.loads(form.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        user = authenticate(request=request, username= form.cleaned_data['username'], password= form.cleaned_data['password'])
        
        if user is not None:
            login(request, user)
            return HttpResponse(status='204')
        else:
            response = {
                    'kind': 'error',
                    'errors': {
                        'request':[
                            {
                            'message': 'Username or password not correct.',
                            'code': 'invalid'
                            }
                        ]
                            
                    }
                }
            return HttpResponseBadRequest(json.dumps(response) , content_type='application/json')

    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def logout_user(request):

    if request.method == 'GET':
        logout(request)
        return HttpResponse(status='204')
    
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def change_password(request):

    if request.method == 'PUT':
        form = UserChangePassword(json.loads(request.body), instance=request.user)

        if not form.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(form.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')

        user = User.objects.get(username=form.cleaned_data['username'])
        print(form.cleaned_data['password'])
        user.set_password(form.cleaned_data['password'])
        user.save()

        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['PUT'])
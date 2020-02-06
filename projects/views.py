import datetime
import json

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseNotFound,
                         JsonResponse)
from django.views.decorators.csrf import csrf_exempt

from .forms import ProjectForm, TaskForm
from .models import Project, Task


def str_date(date):
    return str(date.replace(tzinfo=None, microsecond=0))

def list_ids_query_set(QuerySet):
    return [model.id for model in QuerySet]

def task_model_to_json(task):
    return {
        'kind': 'task',
        'id': task.id,
        'title': task.title, 
        'description': task.description,
        'created': str_date(task.created),
        'updated': str_date(task.updated),
        'project': task.project.id,
        'deadline': str_date(task.deadline),
        'resources': task.resources,
        'status': task.status,
    }

def task_list_query_set(QuerySet):
    return [task_model_to_json(model) for model in QuerySet]

def project_model_to_json(project, complete_tasks=False):
    return {
        'kind': 'project',
        'id': project.id,
        'title': project.title, 
        'description': project.description,
        'author': project.author.id,
        'created': str_date(project.created),
        'updated': str_date(project.updated),
        'public': project.public,
        'tasks': task_list_query_set(project.tasks.all()) if complete_tasks else list_ids_query_set(project.tasks.all()),
        'deadline': str_date(project.deadline),
        'status': project.status,
    }

def project_list_query_set(QuerySet):
    return [project_model_to_json(model) for model in QuerySet]

@csrf_exempt
def projects_view(request):

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
        return HttpResponse(content=json.dumps(response), content_type='application/json', status=401)

    if request.method == 'GET':
        response = { 
            'kind': 'projects',
            'projects': project_list_query_set(Project.objects.all()) 
        }
        return JsonResponse(response)

    elif request.method == 'POST':

        #validate input
        project = ProjectForm(json.loads(request.body))
        if not project.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(project.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')
        
        #creation of new object
        model = Project(author=request.user, **project.cleaned_data)
        
        #Save changes in database
        model.save()

        return JsonResponse(project_model_to_json(model), status=201)
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def project_view(request, projectId=None):

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
        return HttpResponse(content=json.dumps(response), content_type='application/json', status=401)

    if not Project.objects.filter(id=projectId).exists():
        response = {
                'kind': 'error',
                'errors': {
                    'request':[
                        {
                        'message': 'A project with that id does not exist.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')
    
    project = Project.objects.get(id=projectId)

    if  request.method == 'GET':
        return JsonResponse(project_model_to_json(project, complete_tasks=True))

    elif request.method == 'PUT':
    
        #validate input
        project_input = ProjectForm(json.loads(request.body), instance=project)
        if not project_input.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(project_input.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')
        
        #Save changes in database
        project.save()

        return JsonResponse(project_model_to_json(project))

    elif request.method == 'DELETE':
        project.delete()
        return HttpResponse(status=204)
    
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

@csrf_exempt
def tasks_view(request, projectId=None):

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
        return HttpResponse(content=json.dumps(response), content_type='application/json', status=401)

    if not Project.objects.filter(id=projectId).exists():
        response = {
                'kind': 'error',
                'errors': {
                    'request':[
                        {
                        'message': 'A project with that id does not exist.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')
    
    project = Project.objects.get(id=projectId)

    if  request.method == 'GET':
        response = {
            'kind': 'task_list',
            'tasks': task_list_query_set(project.tasks.all())
        }
        return JsonResponse(response)
        
    elif request.method == 'POST':
            
        #validate input
        task = TaskForm(json.loads(request.body))
        if not task.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(task.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response) , content_type='application/json')

        #creation of new object
        model = Task(project=project, **task.cleaned_data)
        
        #Save changes in database
        model.save()
        project.tasks.add(model)

        return JsonResponse(task_model_to_json(model), status=201)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def task_view(request, projectId=None, taskId=None):

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
        return HttpResponse(content=json.dumps(response), content_type='application/json', status=401)

    if not Project.objects.filter(id=projectId).exists():
        response = {
                'kind': 'error',
                'errors': {
                    'request':[
                        {
                        'message': 'A project with that id does not exist.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')
    
    project = Project.objects.get(id=projectId)

    if not project.tasks.filter(id=taskId).exists():
        response = {
                'kind': 'error',
                'errors': {
                    'request':[
                        {
                        'message': 'A task with that id does not exist or does not belong to this project.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')

    task = project.tasks.get(id=taskId)

    if request.method == 'GET': 
        return JsonResponse(task_model_to_json(task))

    elif request.method == 'PUT':
        #validate input
        task_input = TaskForm(json.loads(request.body), instance=task)
        if not task_input.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(task_input.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')
        
        #Save changes in database
        task.save()

        return JsonResponse(task_model_to_json(task))

    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .forms import NewProject, NewTask
import json, datetime, uuid

projects = {}

@csrf_exempt
def all_projects(request):

    if request.method == 'GET':#get all projects
        return JsonResponse({ 'projects': projects })

    elif request.method == 'POST':#create a new project

        #validate input
        np = NewProject(json.loads(request.body))
        if not np.is_valid():
            return HttpResponseBadRequest(np.errors.as_json(), content_type='text/json')
        
        #creation of new object
        body = np.cleaned_data
        id = str(uuid.uuid4())
        new_project = {
            'kind': 'project',
            'id': id,
            'title': body['title'], 
            'description': body['description'],
            'created': datetime.datetime.now(),
            'updated': datetime.datetime.now(),
            'canRead':[],
            'canEdit':[],
            'admins':[],
            'tasks': {},
            'deadline': body['deadline'],
            'status': 0,
        }

        #Save changes in database
        projects[id] = new_project

        return JsonResponse(new_project)
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def specific_project(request, projectId=None):

    #Validate that the project exists
    if not str(projectId) in projects:
            return HttpResponseNotFound('A project with that id does not exist.')

    if request.method == 'GET':#gets the specific project
        return JsonResponse(projects[str(projectId)])
        
    elif request.method == 'POST':#post a task to the project
        
        #validate input
        nt = NewTask(json.loads(request.body))
        if not nt.is_valid():
            return HttpResponseBadRequest(nt.errors.as_json(), content_type='text/json')

        #creation of new object
        body = nt.cleaned_data
        id = str(uuid.uuid4())
        new_task = {
            'kind': 'task',
            'id': id,
            'title': body['title'], 
            'description': body['description'],
            'deadline': body['deadline'],
            'startDate': body['startDate'],
            'inCharge':[],
            'resorces': body['resources'],
            'status': 0,
        }

        #Save changes in database
        projects[str(projectId)]['tasks'][id] = new_task

        return JsonResponse(new_task)

    elif request.method == 'PUT':#modify the entire project to these new values
        body = json.loads(request.body)

        if not 'title' in body:
            return HttpResponseBadRequest('A project cannot be updated without a "title" field.')
        if not 'description' in body:
            return HttpResponseBadRequest('A project cannot be updated without a "description" field.')
        if not 'canRead' in body:
            return HttpResponseBadRequest('A project cannot be updated without a "canRead" field.')
        if not 'canEdit' in body:
            return HttpResponseBadRequest('A project cannot be updated without a "canEdit" field.')
        if not 'admins' in body:
            return HttpResponseBadRequest('A project cannot be updated without an "admins" field.')
        if not 'deadline' in body:
            return HttpResponseBadRequest('A project cannot be updated without a "deadline" field.')
        if not 'status' in body:
            return HttpResponseBadRequest('A project cannot be updated without a "status" field.')

        modified_project = {
            'kind': 'project',
            'id': str(projectId),
            'title': body['title'], 
            'description': body['description'],
            'created': projects[str(projectId)]['created'],
            'updated': datetime.datetime.now(),
            'canRead': body['canRead'],
            'canEdit': body['canEdit'],
            'admins': body['admins'],
            'tasks': projects[str(projectId)]['tasks'],
            'deadline': body['deadline'],
            'status': body['status'],
        }
        
        return

    elif request.method == 'PATCH':#modify only the changes to the resource
        return
    elif request.method == 'DELETE':#deletes the project
        return
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json, datetime

projects = {
    '1':{
        'kind': 'project',
        'id': '1',
        'title': 'Dummy Project',
        'description': 'This is a project to test the feature that creates projects',
        'created': '2011-08-01T19:58:51.947',
        'updated': '2011-08-01T19:58:51.947',
        'canRead':[],
        'canEdit':[],
        'admins':[],
        'tasks': {},
        'deadline': '2020-08-01T19:58:51.947',
        'status': 0,
    }
}

@csrf_exempt
def all_projects(request):

    if request.method == 'GET':#get all projects
        return JsonResponse({ 'projects': projects })

    elif request.method == 'POST':#create a new project
        body = json.loads(request.body)

        #validate that the request has everything that has been asked for
        if not 'title' in body:
            return HttpResponseBadRequest('A project cannot be created without title')
        if not 'description' in body:
            return HttpResponseBadRequest('A project cannot be created without description')
        if not 'deadline' in body:
            return HttpResponseBadRequest('A project cannot be created without a deadline')
        
        #creation of new object
        id = str(len(projects) + 1)
        newProject = {
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
        projects[id] = newProject
        return JsonResponse(newProject)

@csrf_exempt
def specific_project(request, projectId=None):

    if request.method == 'GET':#gets the specific project

        if not str(projectId) in projects:
            return HttpResponseBadRequest('A project with that id does not exist.')
            
        return JsonResponse(projects[str(projectId)])
        
    elif request.method == 'POST':#post a task to the project
        return
    elif request.method == 'PUT':#modify the entire project to these new values
        return
    elif request.method == 'PATCH':#modify only the changes to the resource
        return
    elif request.method == 'DELETE':#deletes the project
        return
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .forms import ProjectForm, TaskForm
from .models import Project, Task
import json, datetime, uuid

projects = {}

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
        'created': str_date(project.created),
        'updated': str_date(project.updated),
        'tasks': task_list_query_set(project.tasks.all()) if complete_tasks else list_ids_query_set(project.tasks.all()),
        'deadline': str_date(project.deadline),
        'status': project.status,
    }

def project_list_query_set(QuerySet):
    return [project_model_to_json(model) for model in QuerySet]

@csrf_exempt
def all_projects(request):

    if request.method == 'GET':#get all projects
        response = { 
            'kind': 'projects',
            'projects': project_list_query_set(Project.objects.all()) 
        }
        return JsonResponse(response)

    elif request.method == 'POST':#create a new project

        #validate input
        project = ProjectForm(json.loads(request.body))
        if not project.is_valid():
            response = {
                'kind': 'error',
                'errors': json.loads(project.errors.as_json())
            }
            return HttpResponseBadRequest(json.dumps(response), content_type='application/json')
        
        #creation of new object
        model = Project(**project.cleaned_data)
        
        #Save changes in database
        model.save()

        return JsonResponse(project_model_to_json(model))
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def specific_project(request, projectId=None):

    #Validate that the project exists
    try:
        project = Project.objects.get(id=projectId)
    except:
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
    else:
        if  request.method == 'GET':#gets the specific project
            return JsonResponse(project_model_to_json(project, complete_tasks=True))
            
        elif request.method == 'POST':#post a task to the project
            
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

            return JsonResponse(task_model_to_json(model))

        elif request.method == 'PUT':#modify the entire project to these new values
            
            #validate input
            projectInput = ProjectForm(json.loads(request.body), instance=project)
            if not projectInput.is_valid():
                response = {
                    'kind': 'error',
                    'errors': json.loads(projectInput.errors.as_json())
                }
                return HttpResponseBadRequest(json.dumps(response), content_type='application/json')
            
            #Save changes in database
            project.save()

            return JsonResponse(project_model_to_json(project))

        elif request.method == 'DELETE':#deletes the project
            project.delete()
            return HttpResponse(status=204)

        else:
            return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])

def specific_task(request, projectId=None, taskId=None):

    #validate that the project and task both exist
    #the task must correspond with the project
    try:
        project = Project.objects.get(id=projectId)
        task = project.tasks.get(id=taskId)
    except:
        response = {
                'kind': 'error',
                'errors': {
                    'request':[
                        {
                        'message': 'A project or task with that id does not exist.',
                        'code': 'not found'
                        }
                    ]
                        
                }
            }
        return HttpResponseNotFound(json.dumps(response) , content_type='application/json')
    else:

        if request.method == 'GET': 
            return JsonResponse(task_model_to_json(task))

        else:
            return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
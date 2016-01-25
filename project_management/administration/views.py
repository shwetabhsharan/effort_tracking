from administration.models import (Sprint, Task, STORY_POINTS, SubTask, TEAM, 
                                   STATUSES, SUBTASK_SCOPE, EffortRecord, TASK_STATUS_LIST, 
                                   TEAM_LIST, EffortTracking, rca_type_choice, cr_status,
                                   review_type_choice, CodeReview)
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages

def login_page(request):
    """
        render login screen
    """
    logout(request)
    context = {}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

def authenticate_user(request):
    """
        authenticate user
    """
    context = {}

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if not username or not password:
        messages.add_message(request, messages.INFO, 'Please enter the required fields')
        return HttpResponseRedirect('/administration/login/')
    elif not user:
        messages.add_message(request, messages.INFO, 'Invalid Credentials')
        return HttpResponseRedirect('/administration/login/')
    else:
        login(request, user)

    return HttpResponseRedirect('/administration/main/')

def main(request):
    """
        render main page
    """
    context = {}
    return render_to_response('index.html', context)

def sprint(request):
    """
        render sprint page
    """
    context = {}
    sprint_objects = Sprint.objects.all()
    context['sprint_objects'] = sprint_objects
    return render_to_response('sprint.html', context, context_instance=RequestContext(request))

def add_sprint(request):
    """
        store sprint date
    """

    context = {}
    sprint_name = request.POST.get('sprint_name')
    sprint_start_date = request.POST.get('sprint_start_date')
    sprint_end_date = request.POST.get('sprint_end_date')
    velocity = request.POST.get('velocity')

    if not sprint_name or not velocity or not sprint_start_date or not sprint_end_date:
        messages.add_message(request, messages.INFO, 'Please enter the required fields')
        return HttpResponseRedirect('/administration/sprint/')


    sprint_start_date = datetime.strptime(sprint_start_date, '%m/%d/%Y')
    sprint_end_date = datetime.strptime(sprint_end_date, '%m/%d/%Y')

    sprint_obj = Sprint.objects.create(sprint_name=sprint_name, sprint_start_date=sprint_start_date,
                                       sprint_end_date=sprint_end_date, user=request.user, velocity=velocity)

    return HttpResponseRedirect('/administration/sprint/')

def task(request):
    """
        render task page
    """

    context = {}
    sprint_obj = None

    sprint_id = request.GET.get('id')

    if sprint_id:
        sprint_obj = Sprint.objects.get(id=sprint_id)

    sprint_objects = Sprint.objects.filter(status = False) # render all open sprints

    if sprint_obj:
        task_objects = Task.objects.filter(sprint=sprint_obj)
        context['sprint_obj'] = sprint_obj
    elif sprint_objects:
        task_objects = Task.objects.filter(sprint=sprint_objects[0])
        context['sprint_obj'] = sprint_objects[0]
    else:
        task_objects = []

    context['users'] = User.objects.all().values()
    context['sprint_objects'] = sprint_objects
    context['task_objects'] = task_objects
    context['story_points'] = STORY_POINTS

    return render_to_response('task.html', context, context_instance=RequestContext(request))

def add_task(request):
    """
        store sprint date
    """

    context = {}

    sprint_id = request.GET.get('id')

    task_id = request.POST.get('task_id')
    story_point = request.POST.get('story_point')
    user_id = request.POST.get('user')
    created_datetime = request.POST.get('created_datetime')

    if not task_id or not created_datetime:
        messages.add_message(request, messages.INFO, 'Please enter the required fields')
        return HttpResponseRedirect('/administration/task/?id=%s' % sprint_id)

    created_datetime = datetime.strptime(created_datetime, '%m/%d/%Y')

    sprint_obj = Sprint.objects.get(id=sprint_id)

    user_obj = User.objects.get(id=user_id)

    task_obj = Task()
    task_obj.sprint=sprint_obj
    task_obj.task_id=task_id.upper()
    task_obj.story_point=story_point
    task_obj.user=user_obj
    task_obj.created_datetime=created_datetime
    task_obj.save()

    return HttpResponseRedirect('/administration/task/?id=%s' % sprint_id)

def subtask(request):
    """
        render subtask page
    """

    context = {}

    task_obj = None

    task_id = request.GET.get('id')

    if task_id:
        task_obj = Task.objects.get(id=task_id)

    task_objects = Task.objects.filter(sprint__status = False) # render all open sprints

    if task_obj:
        subtask_objects = SubTask.objects.filter(task=task_obj)
        context['task_obj'] = task_obj
    elif task_objects:
        subtask_objects = SubTask.objects.filter(task=task_objects[0])
        context['task_obj'] = task_objects[0]
    else:
        subtask_objects = []

    task_objects = Task.objects.all()

    context['task_objects'] = task_objects
    context['subtask_objects'] = subtask_objects
    context['statuses'] = TASK_STATUS_LIST
    context['subtask_scope'] = SUBTASK_SCOPE
    context['team_list'] = TEAM
    context['users'] = User.objects.all()

    return render_to_response('subtask.html', context, context_instance=RequestContext(request))

def add_subtask(request):
    """
        store subtask
    """

    context = {}

    task_id = request.GET.get('id')

    subtask_id = request.POST.get('subtask_id')
    effort = request.POST.get('effort')
    scope = request.POST.get('scope')
    team = request.POST.get('team')
    status = request.POST.get('status')
    assigned_datetime = request.POST.get('assigned_datetime')

    if not subtask_id or not effort or not assigned_datetime:
        messages.add_message(request, messages.INFO, 'Please enter the required fields')
        return HttpResponseRedirect('/administration/subtask/?id=%s' % task_id)

    assigned_datetime = datetime.strptime(assigned_datetime, '%m/%d/%Y')
    user_id = request.POST.get('user')
    user_obj = User.objects.get(id=user_id)


    task_obj = Task.objects.get(id=task_id)

    subtask_obj = SubTask()
    subtask_obj.task=task_obj
    subtask_obj.subtask_id=subtask_id.upper()
    subtask_obj.effort=effort
    subtask_obj.remaining=effort
    subtask_obj.subtask_scope=scope
    subtask_obj.user=user_obj
    subtask_obj.team=team
    subtask_obj.status=status
    subtask_obj.assigned_datetime=assigned_datetime

    subtask_obj.save()

    ef_record_obj = EffortRecord()
    ef_record_obj.subtask = subtask_obj
    ef_record_obj.save()

    return HttpResponseRedirect('/administration/subtask/?id=%s' % task_id)

def effort_tracking(request):
    """
        render effort tracking sheet
    """

    context = {}
    effort_record_list = []

    sprint_id = request.GET.get('id')
    team = request.GET.get('team')

    if sprint_id and team:
        sprint_id = int(sprint_id)
        effort_record_list = EffortRecord.objects.filter(subtask__team=team, subtask__task__sprint__id = sprint_id)

    context['effort_record_list'] = effort_record_list
    context['sprint_objects'] = Sprint.objects.filter(status = False) # render all open sprints
    context['team_list'] = TEAM_LIST
    context['selected_sprint'] = sprint_id
    context['selected_team'] = team

    return render_to_response('effort_tracking.html', context, context_instance=RequestContext(request))

def track_effort(request):
    """
        render effort tracking sheet
    """

    context = {}
    effort_record_list = []

    sprint_id = request.GET.get('id')
    team = request.GET.get('team')
    consumed_efforts = request.GET.get('ce')
    effort_id = request.GET.get('eid')
    if effort_id and consumed_efforts:
        effort_rec_obj = EffortRecord.objects.get(id=effort_id)
        effort_rec_obj.subtask.remaining = int(effort_rec_obj.subtask.remaining) - int(consumed_efforts)
        effort_rec_obj.subtask.save()
        et_obj = EffortTracking.objects.create(effort_fk=effort_rec_obj, daily_effort=consumed_efforts, effort_date=datetime.now())

    if sprint_id and team:
        sprint_id = int(sprint_id)
        effort_record_list = EffortRecord.objects.filter(subtask__team=team, subtask__task__sprint__id = sprint_id)

    context['effort_record_list'] = effort_record_list
    context['sprint_objects'] = Sprint.objects.filter(status = False) # render all open sprints
    context['team_list'] = TEAM_LIST
    context['selected_sprint'] = sprint_id
    context['selected_team'] = team

    return render_to_response('track_effort.html', context, context_instance=RequestContext(request))

def edit_effort(request, id):
    """
        edit task details
    """

    context = {}

    effort_record_obj = EffortRecord.objects.get(id=id)

    context['effort_record_obj'] = effort_record_obj
    context['sprint_objects'] = Sprint.objects.filter(status = False) # render all open sprints
    context['team_list'] = TEAM
    context['users'] = User.objects.all()
    context['task_status_list'] = TASK_STATUS_LIST
    context['subtask_scope'] = SUBTASK_SCOPE

    return render_to_response('edit_effort_tracking.html', context, context_instance=RequestContext(request))

def save_effort(request, id):
    """
        
    """
    effort_record_obj = EffortRecord.objects.get(id=id)

    start_date = request.POST.get('start_date')
    if start_date:
        effort_record_obj.start_date = datetime.strptime(start_date, '%m/%d/%Y')

    peer_review_date = request.POST.get('peer_review_date')
    if peer_review_date:
        effort_record_obj.peer_review_date = datetime.strptime(peer_review_date, '%m/%d/%Y')

    internal_qa_date = request.POST.get('internal_qa_date')
    if internal_qa_date:
        effort_record_obj.internal_qa_date = datetime.strptime(internal_qa_date, '%m/%d/%Y')

    pr_date = request.POST.get('pr_date')
    if pr_date:
        effort_record_obj.pr_date = datetime.strptime(pr_date, '%m/%d/%Y')

    client_review_date = request.POST.get('client_review_date')
    if client_review_date:
        effort_record_obj.client_review_date = datetime.strptime(client_review_date, '%m/%d/%Y')

    code_merge_date = request.POST.get('code_merge_date')
    if code_merge_date:
        effort_record_obj.code_merge_date = datetime.strptime(code_merge_date, '%m/%d/%Y')

    qa_testing = request.POST.get('qa_testing')
    if qa_testing:
        effort_record_obj.qa_testing = datetime.strptime(qa_testing, '%m/%d/%Y')

    closed = request.POST.get('closed')
    if closed:
        effort_record_obj.closed = datetime.strptime(closed, '%m/%d/%Y')

    user_id = request.POST.get('developer')
    if user_id:
        user = User.objects.get(id=user_id)
        effort_record_obj.subtask.user = user

    team = request.POST.get('team')
    if team:
        effort_record_obj.subtask.team = team

    subtask_scope = request.POST.get('subtask_scope')
    if subtask_scope:
        effort_record_obj.subtask.subtask_scope = subtask_scope

    status = request.POST.get('status')
    if status:
        effort_record_obj.subtask.status = status

    effort_record_obj.subtask.save()
    effort_record_obj.save()


    return HttpResponseRedirect('/administration/effort/')

def review(request):
    """
        render code review sheet
    """
    context = {}
    task_objects = []
    subtask_objects = []
    user_subtask_objects = []

    sprints = Sprint.objects.filter(status = False)
    for obj in sprints:
        tasks = Task.objects.filter(sprint=obj)
        task_objects.extend(tasks)

    for obj in task_objects:
        subtasks = SubTask.objects.filter(task=obj)
        subtask_objects.extend(subtasks)

    for obj in subtask_objects:
        if obj.user.id == request.user.id:
            user_subtask_objects.append(obj)

    context['user_subtask_objects'] = user_subtask_objects
    context['users'] = User.objects.all()
    context['cr_status'] = cr_status
    context['rca_list'] = rca_type_choice
    context['review_type_choice'] = review_type_choice

    return render_to_response('review.html', context, context_instance=RequestContext(request))

def add_review(request):
    """
        Store code review data in the database
    """

    pull_request = request.POST.get('pull_request')
    filename = request.POST.get('filename')
    subtask_id = request.POST.get('subtask_id')
    reviewer = request.POST.get('reviewer')
    review_date = request.POST.get('review_date')
    fixed_date = request.POST.get('fixed_date')
    comment = request.POST.get('comment')
    status = request.POST.get('status')
    review_type = request.POST.get('review_type')
    rca = request.POST.get('rca')

    if not review_date or not pull_request or not filename or not comment:
        messages.add_message(request, messages.INFO, 'Please enter the required fields')
        return HttpResponseRedirect('/administration/review/')

    if fixed_date:
        fixed_date = datetime.strptime(fixed_date, '%m/%d/%Y')
    else:
        fixed_date = None

    review_date = datetime.strptime(review_date, '%m/%d/%Y')

    subtask_obj = SubTask.objects.get(id=subtask_id)

    reviewer_obj = User.objects.get(id=reviewer)

    code_review_obj = CodeReview.objects.create(
                                  subtask = subtask_obj,
                                  pull_request = pull_request,
                                  review_type = review_type,
                                  filename=filename,
                                  comment=comment,
                                  review_date = review_date,
                                  fix_date = fixed_date,
                                  status = status,
                                  rca = rca,
                                  developer = request.user,
                                  reviewer=reviewer_obj
                                  )
    return HttpResponseRedirect('/administration/review/')
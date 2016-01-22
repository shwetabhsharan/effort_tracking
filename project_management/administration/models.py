from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# key - story point value - efforts in hours
STORY_POINTS = [0, 1, 2, 3, 5, 8, 13, 21, 34]
EFFORT = [1,4,6,9,14,22,35,56,90]

SUBTASK_SCOPE = (
           ('Planned', 'Planned'),
           ('Unplanned', 'Unplanned'),
           )

TASK_STATUS_LIST = ['Not Started', 'Development', 'Unplanned', 'Internal QA', 'Pull Request', 
                    'Client Review', 'Review Fix', 'Merged', 'QA Testing', 'Closed', 'Blocked', 'Next Sprint', 
                    'Assigned to Client', 'Infra Process']

STATUSES = (
           ('Not Started', 'Not Started'),
           ('Development', 'Development'),
           ('Unplanned', 'Unplanned'),
           ('Internal QA', 'Internal QA'),
           ('Pull Request', 'Pull Request'),
           ('Client Review', 'Client Review'),
           ('Review Fix', 'Review Fix'),
           ('Merged', 'Merged'),
           ('QA Testing', 'QA Testing'),
           ('Closed', 'Closed'),
           ('Blocked', 'Blocked'),
           ('Next Sprint', 'Next Sprint'),
           ('Assigned to Client', 'Assigned to Client'),
           ('Infra Process', 'Infra Process'),
           )

TEAM_LIST = ['WETL', 'Matrix', 'Gambit', 'Goonies']

TEAM = (
        ('WETL', 'WETL'),
        ('Matrix', 'Matrix'),
        ('Gambit', 'Gambit'),
        ('Goonies', 'Goonies')
        )

review_type_choice = (
               ('Peer', 'Peer'),
               ('Client', 'Client'),
               ('QA', 'QA')
               )

cr_status = (
             ('Opem', 'Open'),
             ('In Progress', 'In Progress'),
             ('Fixed', 'Fixed'),
             ('Closed', 'Closed'),
             ('No Comments', 'No Comments')
             )

rca_type_choice = (
                   ('DOMO Standard', 'DOMO Standard'),
                   ('AngularJS Experience', 'AngularJS Experience'),
                   ('Client Code', 'Client Code'),
                   ('Enhancement', 'Enhancement'),
                   ('Code Optimization', 'Code Optimization'),
                   ('Requirement Conflict', 'Requirement Conflict'),
                   ('Reviewer Conflict', 'Reviewer Conflict'),
                   ('Appreciation', 'Appreciation')
                   )

class UserProfile(models.Model):
    role_type = (
                 ('developer', 'Developer'),
                 ('qa', 'QA')
                 )
    user = models.ForeignKey(User, unique=True)
    user_role = models.CharField(max_length=20, null=False, choices=role_type)
    team = models.CharField(max_length=20, null=True, choices=TEAM)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'

class Sprint(models.Model):
    """
        schema for sprint information
    """

    sprint_name = models.CharField(max_length=30)

    # metadata
    sprint_start_date = models.DateTimeField()
    sprint_end_date = models.DateTimeField()
    status = models.BooleanField(default=False)
    velocity = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.sprint_name

    class Meta:
        ordering = ['-sprint_start_date']
        verbose_name = 'Sprint'

class Task(models.Model):
    """
        schema for maintaining story/epic
    """

    sprint = models.ForeignKey(Sprint)
    task_id = models.CharField(max_length=10)
    story_point = models.IntegerField(max_length=2)

    # metadata
    created_datetime = models.DateTimeField()
    modified_datetime = models.DateTimeField()
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_datetime = datetime.now()
        self.modified_datetime = datetime.now()
        models.Model.save(self, *args, **kwargs )

    def __str__(self):
        return self.task_id

    class Meta:
        ordering = ['-task_id']
        verbose_name = 'Task'

class SubTask(models.Model):


    task = models.ForeignKey(Task)
    subtask_id = models.CharField(max_length=10)
    subtask_scope = models.CharField(max_length=20, null=False, choices=SUBTASK_SCOPE)
    status = models.CharField(max_length=20, null=False, choices=STATUSES)
    team = models.CharField(max_length=20, null=False, choices=TEAM)
    effort = models.IntegerField(max_length=2)
    remaining = models.IntegerField(max_length=2)

    # metadata
    assigned_datetime = models.DateTimeField()
    created_datetime = models.DateTimeField()
    modified_datetime = models.DateTimeField()
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_datetime = datetime.now()
        self.modified_datetime = datetime.now()
        models.Model.save(self, *args, **kwargs )

    def __str__(self):
        return self.subtask_id

    class Meta:
        ordering = ['-subtask_id']
        verbose_name = 'Sub Task'

class CodeReview(models.Model):
    """
        schema for maintaining code review comments
    """

    subtask = models.ForeignKey(SubTask)
    pull_request = models.IntegerField(max_length=5)
    review_type = models.CharField(max_length=30, null=False, choices=review_type_choice)
    filename = models.TextField()
    comment = models.TextField()

    review_date = models.DateTimeField()
    fix_date = models.DateTimeField()
    status = models.CharField(max_length=30, null=False, choices=cr_status)
    rca = models.CharField(max_length=30, null=False, choices=rca_type_choice)

    developer = models.ForeignKey(User, related_name='developer')
    reviewer = models.ForeignKey(User, related_name='reviewer')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_datetime = datetime.now()
        self.modified_datetime = datetime.now()
        models.Model.save(self, *args, **kwargs )

    class Meta:
        ordering = ['-developer']
        verbose_name = 'Code Review Record'


class EffortRecord(models.Model):
    """
        
    """

    subtask = models.ForeignKey(SubTask)
    start_date = models.DateTimeField(null=True)
    peer_review_date = models.DateTimeField(null=True)
    internal_qa_date = models.DateTimeField(null=True)
    pr_date = models.DateTimeField(null=True)
    client_review_date = models.DateTimeField(null=True)
    code_merge_date = models.DateTimeField(null=True)
    qa_testing = models.DateTimeField(null=True)
    closed = models.DateTimeField(null=True)

    def __str__(self):
        return self.subtask.subtask_id

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Effort Record'


class EffortTracking(models.Model):
    """
        
    """

    effort_fk = models.ForeignKey(EffortRecord)
    daily_effort = models.IntegerField(max_length=1)
    effort_date = models.DateField()

    class Meta:
        ordering = ['-effort_date']
        verbose_name = 'Effort Tracking'

from django.contrib import admin
from administration.models import UserProfile, Sprint, Task, SubTask, CodeReview, EffortRecord, EffortTracking

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_role', 'team')
    search_fields = ('user', 'user_role', 'team')
admin.site.register(UserProfile, UserProfileAdmin)

class SprintAdmin(admin.ModelAdmin):
    list_display = ('sprint_name', 'sprint_start_date', 'sprint_end_date')
    search_fields = ('sprint_name', 'sprint_start_date', 'sprint_end_date')
admin.site.register(Sprint, SprintAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('sprint', 'task_id', 'story_point', 'user')
    search_fields = ('sprint', 'task_id', 'story_point', 'user')
admin.site.register(Task, TaskAdmin)

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'subtask_id', 'subtask_scope', 'status', 'team', 'effort', 'user')
    search_fields = ('task', 'subtask_id', 'subtask_scope', 'status', 'team', 'effort', 'user')
admin.site.register(SubTask, SubTaskAdmin)

class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'pull_request', 'developer', 'reviewer', 'pull_request', 'status')
    search_fields = ('subtask', 'pull_request', 'developer', 'reviewer', 'pull_request', 'status')
admin.site.register(CodeReview, CodeReviewAdmin)

class EffortRecordAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'start_date', 'peer_review_date', 'internal_qa_date', 'pr_date', 'client_review_date', 'code_merge_date', 'qa_testing', 'closed')
    search_fields = ('subtask', 'start_date', 'peer_review_date', 'internal_qa_date', 'pr_date', 'client_review_date', 'code_merge_date', 'qa_testing', 'closed')
admin.site.register(EffortRecord, EffortRecordAdmin)

class EffortTrackingAdmin(admin.ModelAdmin):
    list_display = ('effort_fk', 'daily_effort', 'effort_date', 'user')
    search_fields = ('effort_fk', 'daily_effort', 'effort_date', 'user')
admin.site.register(EffortTracking, EffortTrackingAdmin)
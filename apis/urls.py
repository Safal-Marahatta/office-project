from app1.views import complete_task,postpone_task,repeat_task
from django.urls import path

urlpatterns=[
    path('complete/',complete_task,name="complete"),
    path('postpone/',postpone_task,name="postpone"),
    path('repeat/',repeat_task,name="repeat"),
]
from django.urls import path
from Student.views import courseTable  # 导入你的视图模块
from Student.views import courseSelection
from Student.views import courseSelected
from Student.views import addClass
from Student.views import deleteClass
from Student.views import scoreAnalysis
from Student.views import getSemester

urlpatterns = [
    path('student/courseTabel/', courseTable, name='courseTable'),  
    path('student/courseSelection/', courseSelection, name='courseSelection'),
    path('student/courseSelected/', courseSelected, name='courseSelected'),
    path('student/addClass/', addClass, name='addClass'),
    path('student/deleteClass/', deleteClass, name='deleteClass'),
    path('student/scoreAnalysis/', scoreAnalysis, name='scoreAnalysis'),
    path('student/getSemester/', getSemester, name='getSemester'),
]
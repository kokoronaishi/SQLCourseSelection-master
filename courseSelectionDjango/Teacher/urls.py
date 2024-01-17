from django.urls import path
from Teacher.views import TeacherTableInfo  # 导入你的视图模块
from Teacher.views import get_students
from Teacher.views import get_courses
from Teacher.views import get_course_id
from Teacher.views import add_score
from Teacher.views import get_score

urlpatterns = [
    path('teacher/TeacherTableInfo/', TeacherTableInfo, name='TeacherTableInfo'),
    path('teacher/get_students/', get_students, name='get_students'),
    path('teacher/get_courses/', get_courses, name='get_courses'),
    path('teacher/get_course_id/', get_course_id, name='get_course_id'),
    path('teacher/add_score/', add_score, name='add_score'),
    path('teacher/get_score/', get_score, name='get_score'),
    # 其他 URL 配置...
]
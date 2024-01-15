from django.urls import path
from Teacher.views import TeacherTableInfo  # 导入你的视图模块

urlpatterns = [
    path('teacher/TeacherTableInfo/', TeacherTableInfo, name='TeacherTableInfo'),  # 为 login 视图函数定义一个 URL
    # 其他 URL 配置...
]
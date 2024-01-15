from django.urls import path
from Student.views import courseTable  # 导入你的视图模块

urlpatterns = [
    path('student/courseTabel/', courseTable, name='courseTable'),  # 为 login 视图函数定义一个 URL
    # 其他 URL 配置...
]
from django.urls import path
from Login.views import login  # 导入你的视图模块

urlpatterns = [
    path('login/', login, name='login'),  # 为 login 视图函数定义一个 URL
    # 其他 URL 配置...
]
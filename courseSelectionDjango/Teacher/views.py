from django.shortcuts import render
from Model.models import CourseTable
from Model.models import TeacherTable
from Model.models import ClassTable
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.

@csrf_exempt
# 查找某位老师开设的所有课程，仅为post请求，以表格形式返回
def TeacherTableInfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_id = data.get('username')
        semester = data.get('semester')
        print(f"teacherID:{teacher_id}")
        try:
            # 获取教师的所有 ClassTable 记录
            teacher = TeacherTable.objects.get(teacher_id=teacher_id)
            classes = ClassTable.objects.filter(teacher_id=teacher.teacher_id, 
                                               semester=semester)

            # 预加载相关的 CourseTable 记录
            classes = classes.select_related('course')

            courseinfo_data = []
            # 遍历每个 ClassTable 记录，获取所需的信息
            for class_ in classes:
                course_name = class_.course.course_name
                class_time = class_.class_time
                class_place = class_.class_place

                if class_time[2] == "一":
                    DoW = "Mon"
                elif class_time[2] == "二":
                    DoW = "Tue"
                elif class_time[2] == "三":
                    DoW = "Wed"
                elif class_time[2] == "四":
                    DoW = "Thu"
                elif class_time[2] == "五":
                    DoW = "Fri"
                if class_time[3] =="1":
                    if class_time[4] == "-":
                        class_begin = 1
                        class_end = int(class_time[5])
                        class_len_1 = class_end - class_begin
                    else:
                        class_begin = int(class_time[3:5])
                        class_end = int(class_time[6:8])
                        class_len_1 = class_end - class_begin
                elif class_time[5] == "1":
                    class_begin = int(class_time[3])
                    class_end = int(class_time[5:7])
                    class_len_1 = class_end - class_begin
                    print(class_begin)
                    print(class_end)
                    print(class_len_1)
                else:
                    class_begin = int(class_time[3])
                    class_end = int(class_time[5])
                    class_len_1 = class_end - class_begin

                course_dict = {
                    'course_name': course_name,
                    'DayofWeek': DoW,
                    'class_begin': class_begin-1,
                    'class_len_1': class_len_1,
                    'class_place': class_place,

                }
                courseinfo_data.append(course_dict)

            print(courseinfo_data)
            return JsonResponse({'courseinfo_data': courseinfo_data}, status=200)
        except TeacherTable.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
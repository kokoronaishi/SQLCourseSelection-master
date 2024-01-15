from django.shortcuts import render
from Model.models import ScoreTable
from Model.models import StudentTable
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.

@csrf_exempt
def courseTable(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('username')
        semester = data.get('semester')
        print(f"studentID:{student_id}")
        try:
            # 获取学生的所有 ScoreTable 记录
            student = StudentTable.objects.get(student_id=student_id)
            scores = ScoreTable.objects.filter(student_id=student.student_id, 
                                               classNo__semester=semester)

            # 预加载相关的 ClassTable、CourseTable 和 TeacherTable 记录
            scores = scores.select_related('classNo', 'classNo__course', 'classNo__teacher')

            courseinfo_data = []
            # 遍历每个 ScoreTable 记录，获取所需的信息
            for score in scores:
                course_name = score.classNo.course.course_name
                class_time = score.classNo.class_time
                class_place = score.classNo.class_place
                teacher_name = score.classNo.teacher.teacher_name

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
                    'teacher_name': teacher_name,
                }
                courseinfo_data.append(course_dict)

            print(courseinfo_data)
            return JsonResponse({'courseinfo_data': courseinfo_data}, status=200)
        except ScoreTable.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        

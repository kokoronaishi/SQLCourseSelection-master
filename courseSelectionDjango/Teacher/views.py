from django.shortcuts import render
from Model.models import CourseTable
from Model.models import TeacherTable
from Model.models import ClassTable
from Model.models import StudentTable
from Model.models import ScoreTable
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
            
            if course_name == "":
                return JsonResponse({'error': 'No courses'}, status=400)
            print(courseinfo_data)
            return JsonResponse({'courseinfo_data': courseinfo_data}, status=200)
        except TeacherTable.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
# 查找某位老师在某学期开的某门课程的所有学生，仅为post请求，接收username，semester，course_name作为参数
def get_students(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_id = data.get('username')
        semester = data.get('semester')
        course_name = data.get('course_name')
#        teacher_id = data.get('username')
#        semester = data.get('semester')
#        course_name = data.get('course_name')
#        teacher_name = TeacherTable.objects.get(teacher_id=teacher_id)
        course_id = CourseTable.objects.get(course_name=course_name)
        try:
            class_id = ClassTable.objects.get(teacher_id=teacher_id, semester=semester, course_id=course_id)
        except ClassTable.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=400)
        student_ids = ScoreTable.objects.filter(classNo=class_id)
        student_names = []
        student_id = []
        count = 0
        for score in student_ids:
            count = count + 1
            try:
                student_name = StudentTable.objects.get(student_id=score.student_id).student_name
#                print(student_name)
                student_names.append(student_name)
#                print(student_names)
                student_id.append(score.student_id)
            except StudentTable.DoesNotExist:
                return JsonResponse({'error': 'Student not found'}, status=400)
        students = [{'student_name': name, 'student_id': id} for name, id in zip(student_names, student_id)]
        if students == []:
            return JsonResponse({'error': 'No students'}, status=400)
        return JsonResponse({'students': students, 'count': count}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt    
def get_courses(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_id = data.get('username')
        semester = data.get('semester')
        try:
            course_ids = ClassTable.objects.filter(teacher_id=teacher_id, semester=semester)
            course_names = []
            course_id_all = []
            for course in course_ids:
                course_name = course.course.course_name
                course_id = course.course_id
                course_names.append(course_name)
                course_id_all.append(course_id)
#                print(course_names)
#                print(course_id_all)

            return JsonResponse({'course_name': course_names, 'course_id': course_id_all}, status=200)
        except ClassTable.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
@csrf_exempt
def get_course_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_name = data.get('course_name')
        try:
            course_id = CourseTable.objects.get(course_name=course_name).course_id
            print(course_id)
            return JsonResponse({'course_id': course_id}, status=200)
        except CourseTable.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
@csrf_exempt
def add_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_id = data.get('username')
        semester = data.get('semester')
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        score = data.get('score')
        scores = []
        try:
            print(student_id)
            print(course_id)
            classNo_id = ClassTable.objects.get(teacher_id=teacher_id, semester=semester, course_id=course_id).id
            print(classNo_id)
            ScoreTable.objects.filter(student_id=student_id, classNo_id=classNo_id).update(score=score)
            for eachscore in ScoreTable.objects.filter(classNo_id=classNo_id):
                score = eachscore.score
                scores.append(score)
            return JsonResponse({'success': 'Score added', 'score': scores}, status=200)
        except ScoreTable.DoesNotExist:
            return JsonResponse({'error': 'Score not found'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
@csrf_exempt
def get_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_id = data.get('username')
        semester = data.get('semester')
        course_id = data.get('course_id')
        scores = []
        try:
            classNo_id = ClassTable.objects.get(teacher_id=teacher_id, semester=semester, course_id=course_id).id
            for eachscore in ScoreTable.objects.filter(classNo_id=classNo_id):
                score = eachscore.score
                scores.append(score)
            return JsonResponse({'score': scores}, status=200)
        except ScoreTable.DoesNotExist:
            return JsonResponse({'error': 'Score not found'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
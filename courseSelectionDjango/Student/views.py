from django.shortcuts import render
from Model.models import ScoreTable
from Model.models import StudentTable
from Model.models import ClassTable
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

# Create your views here.

@csrf_exempt
def getSemester(request):
    if request.method == 'POST':
        try:
            # 获取ClassTable中的属性semester的所有不重复的值
            semesters = list(ClassTable.objects.values_list('semester', flat=True).distinct())
            semesters.sort()
            return JsonResponse({'semesters': semesters}, status=200)
        except ClassTable.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        

@csrf_exempt
def courseTable(request):
    # 在后端写死我的课表的学期
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('username')
        semester = data.get('semester')
        print(semester)
        # print(f"studentID:{student_id}")
        try:
            # 获取指定学生的所有 ScoreTable 记录
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
                # 对class_time的数据格式进行处理
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
                    'course_name': course_name,     # 课程名
                    'DayofWeek': DoW,               # 星期几
                    'class_begin': class_begin-1,   # 开始序号 
                    'class_len_1': class_len_1,     # 节数
                    'class_place': class_place,     # 上课地点
                    'teacher_name': teacher_name,   # 教师名
                }
                courseinfo_data.append(course_dict)

            # print(courseinfo_data)
            return JsonResponse({'courseinfo_data': courseinfo_data}, status=200)
        except ScoreTable.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
@csrf_exempt
def courseSelection(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data.get('query')
        course_id = data.get('course_id')
        teacher_id = data.get('teacher_id')
        semester = data.get('semester')
        student_id = data.get('student_id')
        try:
            if (course_id != '' and teacher_id != ''):      # 课号和教师号都不为空
                class_objs = ClassTable.objects.filter(course__course_id=course_id, 
                            teacher__teacher_id=teacher_id, semester=semester)
            elif (course_id != '' and teacher_id == ''):    # 课号不为空，教师号为空
                class_objs = ClassTable.objects.filter(course__course_id=course_id, 
                            semester=semester)
            elif (course_id == '' and teacher_id != ''):    # 课号为空，教师号不为空
                class_objs = ClassTable.objects.filter(teacher__teacher_id=teacher_id, 
                            semester=semester)
            elif (course_id == '' and teacher_id == ''):    # 课号和教师号都为空
                class_objs = ClassTable.objects.filter(semester=semester)
            
            # print(class_objs)
            selected_courses = ScoreTable.objects.filter(student_id=student_id, # 已选课程 
                                            classNo__semester=semester)
            # 建立选课表ScoreTable中classNo和student_id数量的字典
            class_counts = ScoreTable.objects.values('classNo').annotate(student_count=Count('student_id'))
            classinfo_data = []
            for class_obj in class_objs:
                # 如果该课程已经被选，则跳过
                if class_obj.id in selected_courses.values_list('classNo', flat=True):
                    continue
                current_num = 0
                course_id = class_obj.course.course_id
                course_name = class_obj.course.course_name
                class_time = class_obj.class_time
                credit = class_obj.course.credit
                teacher_id = class_obj.teacher.teacher_id
                teacher_name = class_obj.teacher.teacher_name
                capacity = class_obj.capacity
                # print(f'select{class_obj.id}')
                # 匹配classNo，查询已选人数 ( student_id数量 )
                for class_count in class_counts:
                    if class_count['classNo'] == class_obj.id:
                        current_num = class_count['student_count']
                        break
                
                class_dict = {
                    'course_id': course_id,
                    'course_name': course_name,
                    'class_time': class_time,
                    'credit': credit,
                    'teacher_id': teacher_id,
                    'teacher_name': teacher_name,
                    'capacity': capacity,
                    'current_num' : current_num
                }
                classinfo_data.append(class_dict)
            # print(classinfo_data)
            return JsonResponse({'classinfo_data': classinfo_data}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No matching class found'}, status=400)

@csrf_exempt
def courseSelected(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data = data.get('query')
        # print(data)
        student_id = data.get('student_id')
        semester = data.get('semester')
        try:
            # 通过学号和学期查询已选课程
            class_objs = ScoreTable.objects.filter(student_id=student_id, 
                                               classNo__semester=semester)
            class_objs = class_objs.select_related('classNo', 'classNo__course', 'classNo__teacher')
            # 建立选课表ScoreTable中classNo和student_id数量的字典
            class_counts = ScoreTable.objects.values('classNo').annotate(student_count=Count('student_id'))
            classinfo_data = []
            for class_obj in class_objs:
                current_num = 0 
                course_id = class_obj.classNo.course.course_id
                course_name = class_obj.classNo.course.course_name
                class_time = class_obj.classNo.class_time
                credit = class_obj.classNo.course.credit
                teacher_id = class_obj.classNo.teacher.teacher_id
                teacher_name = class_obj.classNo.teacher.teacher_name
                capacity = class_obj.classNo.capacity
                # print(f'selected{class_obj.classNo.id}')
                # 匹配classNo，查询已选人数 ( student_id数量 )
                for class_count in class_counts:
                    if class_count['classNo'] == class_obj.classNo.id:
                        current_num = class_count['student_count']
                        break

                class_dict = {
                    'course_id': course_id,
                    'course_name': course_name,
                    'class_time': class_time,
                    'credit': credit,
                    'teacher_id': teacher_id,
                    'teacher_name': teacher_name,
                    'capacity': capacity,
                    'current_num' : current_num
                }
                classinfo_data.append(class_dict)
            #print(classinfo_data)
            return JsonResponse({'classinfo_data': classinfo_data}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No matching class found'}, status=400)
        
@csrf_exempt
def addClass(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        student_id = data.get('student_id')
        semester = data.get('semester')
        teacher_id = data.get('teacher_id')
        try:
            
            # 通过class_id查询ClassTable记录
            class_obj = ClassTable.objects.get(course_id=course_id, 
                                    teacher_id=teacher_id, semester=semester)
            
            # 通过student_id查询StudentTable记录
            student_obj = StudentTable.objects.get(student_id=student_id)

            # 通过student_id和semester查询学生在当前学期选择的课程记录
            class_selected = ScoreTable.objects.filter(student_id=student_id, 
                                               classNo__semester=semester)
            class1_time = []
            for class1 in class_selected:
                # 将class1所对应的class_time转换为列表
                class1_time.append(class1.classNo.class_time)
            # 生成一个字典class_selected_time, 其中key为DoW的值
            class_selected_time = {}
            for time in class1_time:
                class_selected_time[time[2]] = []
            for time in class1_time:
                if time[3] =="1":
                    if time[4] == "-":
                        class_begin = 1
                        class_end = int(time[5])
                    else:
                        class_begin = int(time[3:5])
                        class_end = int(time[6:8])
                elif time[5] == "1":
                    class_begin = int(time[3])
                    class_end = int(time[5:7])
                else:
                    class_begin = int(time[3])
                    class_end = int(time[5])
                class_selected_time[time[2]].extend(list(range(class_begin, class_end + 1)))
            
            print(class_selected_time)
            selecting_class_time = class_obj.class_time
            try:
                period = class_selected_time[selecting_class_time[2]]
                if selecting_class_time[3] =="1":
                    if selecting_class_time[4] == "-":
                        class_begin = 1
                        class_end = int(selecting_class_time[5])
                    else:
                        class_begin = int(selecting_class_time[3:5])
                        class_end = int(selecting_class_time[6:8])
                elif selecting_class_time[5] == "1":
                    class_begin = int(selecting_class_time[3])
                    class_end = int(selecting_class_time[5:7])
                else:
                    class_begin = int(selecting_class_time[3])
                    class_end = int(selecting_class_time[5])
                for i in range(class_begin, class_end + 1):
                    if i in period:
                        return JsonResponse({'error': 'Time conflict'}, status=400)
            except KeyError:
                pass

            # 通过class_id和student_id在ScoreTable中添加记录
            ScoreTable.objects.create(student=student_obj, classNo=class_obj)
            
            return JsonResponse({'message': 'Add class successfully'}, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No matching class found'}, status=400)
        
@csrf_exempt
def deleteClass(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        student_id = data.get('student_id')
        semester = data.get('semester')
        teacher_id = data.get('teacher_id')
        try:
            # 通过class_id查询ClassTable记录
            class_obj = ClassTable.objects.get(course_id=course_id, 
                                    teacher_id=teacher_id, semester=semester)
            
            # 通过student_id查询StudentTable记录
            student_obj = StudentTable.objects.get(student_id=student_id)

            # 通过class_id和student_id在ScoreTable中删除记录
            ScoreTable.objects.filter(student=student_obj, classNo=class_obj).delete()

            return JsonResponse({'message': 'Delete class successfully'}, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No matching class found'}, status=400)
        
@csrf_exempt
def scoreAnalysis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        try:
            # 通过student_id在ScoreTable中查询记录, 通过classNo和classNo.course预加载相关记录
            scores = ScoreTable.objects.filter(student_id=student_id).select_related('classNo', 'classNo__course')
            # 计算每个semester的平均成绩
            semester_score = {}
            for score in scores:
                semester = score.classNo.semester
                if semester in semester_score:
                    semester_score[semester].append({score.score:score.classNo.course.credit})
                else:
                    semester_score[semester] = [{score.score:score.classNo.course.credit}]
            print(semester_score)
            for key in semester_score:
                sum_score = 0
                sum_credit = 0
                for score in semester_score[key]:
                    sum_score += list(score.keys())[0] * list(score.values())[0]
                    sum_credit += list(score.values())[0]
                semester_score[key] = round(sum_score / sum_credit,2)
            print(semester_score)
            semester_score = {key: semester_score[key] for key in sorted(semester_score)}
            keys = list(semester_score.keys())
            values = list(semester_score.values())
            avg_score = []
            avg_score.append(keys)
            avg_score.append(values)
            
            return JsonResponse({'avg_score': avg_score}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No matching class found'}, status=400)
        
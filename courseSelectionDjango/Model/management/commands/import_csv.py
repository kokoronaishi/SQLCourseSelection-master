from django.core.management.base import BaseCommand
from Model.models import DeptTable
from Model.models import StudentTable
from Model.models import ScoreTable
from Model.models import TeacherTable
from Model.models import User
from Model.models import ClassTable
from Model.models import CourseTable
from django.contrib.auth.hashers import make_password
import csv

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def handle(self, *args, **options):
        with open('../course_selection_csv/dept.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                dept = DeptTable(dept_id=row[0], dept_name=row[1])
                dept.save()

        with open('../course_selection_csv/student.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                dept = DeptTable.objects.get(dept_id=row[1])
                student = StudentTable(student_id=row[0], dept_id=dept.dept_id,
                                       student_name=row[2])
                student.save()

        with open('../course_selection_csv/teacher.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                dept = DeptTable.objects.get(dept_id=row[3])
                teacher = TeacherTable(teacher_id=row[0], level=row[1],
                                       dept_id=dept.dept_id, teacher_name=row[2])
                teacher.save()
        
        with open('../course_selection_csv/course.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                dept = DeptTable.objects.get(dept_id=row[3])
                course = CourseTable(course_id=row[0], course_name=row[1],
                                     credit=row[2], dept_id=dept.dept_id)
                course.save()

        with open('../course_selection_csv/class.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                course = CourseTable.objects.get(course_id=row[2])
                teacher = TeacherTable.objects.get(teacher_id=row[3])
                class1 = ClassTable(semester=row[0], class_time=row[1],
                                    course_id=course.course_id,
                                    teacher_id=teacher.teacher_id,
                                    class_place=row[4], capacity=row[5])
                class1.save()

        with open('../course_selection_csv/score.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                student = StudentTable.objects.get(student_id=row[2])
                class1 = ClassTable.objects.get(id=row[1])
                score = ScoreTable(score=row[0], classNo_id=class1.id,
                                    student_id=student.student_id)
                score.save()

        with open('../course_selection_csv/user.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                password = make_password(row[0])
                user = User(user_id=row[1], password=password, user_type=row[2])
                user.save()
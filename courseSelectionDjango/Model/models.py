from django.db import models

# Create your models here.


# 数据库同步命令

# 1.python manage.py makemigrations
# 2.python manage.py migrate


class DeptTable(models.Model):  # 院系表
    dept_id = models.CharField(max_length=10, primary_key=True)  # 院系号
    dept_name = models.CharField(max_length=20)  # 名称
    class Meta:
        db_table="DeptTable"


class User(models.Model):
    password = models.CharField(max_length=128)
    user_id = models.CharField(max_length=10, primary_key=True)  # 学号/工号
    user_type = models.CharField(max_length=2,default='S') # 用户类型
    class Meta:
        db_table="User"


class StudentTable(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)  # 学号
    student_name = models.CharField(max_length=20)  # 姓名
    dept = models.ForeignKey(
        DeptTable, on_delete=models.CASCADE)  # 院系号
    class Meta:
        db_table="StudentTable"
    


class TeacherTable(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True)  # 工号
    teacher_name = models.CharField(max_length=20)  # 姓名
    level = models.CharField( max_length=10)  # 职位
    dept = models.ForeignKey(
        DeptTable, on_delete=models.CASCADE)  # 院系号
    class Meta:
        db_table="TeacherTable"


class CourseTable(models.Model):  # 课程表(默认学分4)
    course_id = models.CharField(max_length=10, primary_key=True)  # 课号
    course_name = models.CharField(max_length=20)  # 课名
    credit = models.IntegerField(default=4)  # 学分
    dept = models.ForeignKey(
        DeptTable, on_delete=models.CASCADE)  # 院系号
    class Meta:
        db_table="CourseTable"


class ClassTable(models.Model):  # 开课表
    course = models.ForeignKey(CourseTable, on_delete=models.CASCADE)  # 课号
    teacher = models.ForeignKey(
        TeacherTable, on_delete=models.CASCADE)  # 工号
    semester = models.CharField(max_length=20)  # 学期
    class_time = models.CharField(max_length=20)  # 上课时间
    class_place = models.CharField(max_length=20)  # 上课地点
    capacity = models.IntegerField(default=10)  # 容量
    class Meta:
        unique_together=("course","teacher","semester")
        db_table="ClassTable"


class ScoreTable(models.Model):  # 班级表
    student = models.ForeignKey(
        StudentTable, on_delete=models.CASCADE)  # 学号
    classNo = models.ForeignKey(
        ClassTable, on_delete=models.CASCADE)  # 开课标识号
    score = models.FloatField(default=0)  # 最终成绩
    class Meta:
        unique_together=("student","classNo")
        db_table="ScoreTable"

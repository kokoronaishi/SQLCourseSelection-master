# Generated by Django 4.2.9 on 2024-01-15 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DeptTable",
            fields=[
                (
                    "dept_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("dept_name", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "DeptTable",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128)),
                (
                    "user_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("user_type", models.CharField(default="S", max_length=2)),
            ],
            options={
                "db_table": "User",
            },
        ),
        migrations.CreateModel(
            name="TeacherTable",
            fields=[
                (
                    "teacher_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("teacher_name", models.CharField(max_length=20)),
                ("level", models.CharField(max_length=10)),
                (
                    "dept",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.depttable",
                    ),
                ),
            ],
            options={
                "db_table": "TeacherTable",
            },
        ),
        migrations.CreateModel(
            name="StudentTable",
            fields=[
                (
                    "student_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("student_name", models.CharField(max_length=20)),
                (
                    "dept",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.depttable",
                    ),
                ),
            ],
            options={
                "db_table": "StudentTable",
            },
        ),
        migrations.CreateModel(
            name="CourseTable",
            fields=[
                (
                    "course_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("course_name", models.CharField(max_length=20)),
                ("credit", models.IntegerField(default=4)),
                (
                    "dept",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.depttable",
                    ),
                ),
            ],
            options={
                "db_table": "CourseTable",
            },
        ),
        migrations.CreateModel(
            name="ClassTable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("semester", models.CharField(max_length=20)),
                ("class_time", models.CharField(max_length=20)),
                ("class_place", models.CharField(max_length=20)),
                ("capacity", models.IntegerField(default=10)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.coursetable",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.teachertable",
                    ),
                ),
            ],
            options={
                "db_table": "ClassTable",
                "unique_together": {("course", "teacher", "semester")},
            },
        ),
        migrations.CreateModel(
            name="ScoreTable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.FloatField(default=0)),
                (
                    "classNo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.classtable",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Model.studenttable",
                    ),
                ),
            ],
            options={
                "db_table": "ScoreTable",
                "unique_together": {("student", "classNo")},
            },
        ),
    ]

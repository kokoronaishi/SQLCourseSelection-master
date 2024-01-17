<template>
  <div style="display: flex; justify-content: center; align-items: center; margin-top: 50px;">
    <el-select v-model="semester" placeholder="请选择学期" style="margin-right: 30px; width:150px;">
      <el-option
        v-for="item in ['202301', '202302', '202303', '202304']"
        :key="item"
        :label="item"
        :value="item">
      </el-option>
    </el-select>

    <el-select v-model="course_name" placeholder="请选择课程" style="margin-right: 30px; width:150px;">
      <el-option
        v-for="item in courses"
        :key="item"
        :label="item"
        :value="item">
      </el-option>
    </el-select>

    <el-button type="primary" @click="fetchData">查询</el-button>
  </div>

  <el-table :data="students" style="width: 100%; margin-top: 50px;">
    <el-table-column prop="student_id" label="学号"></el-table-column>
    <el-table-column prop="student_name" label="姓名"></el-table-column>
  </el-table>
</template>

<script>
import { ref,onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessageBox } from 'element-plus';

export default {
  setup() {

    const route = useRoute();
    const username = route.params.username;
    const semester = ref([]);
    const course_name = ref([]);
    const students = ref([]);
    const courses = ref([]);
    const fetchData = async () => {
      students.value = [];
      console.log(semester.value);
      console.log('fetchData start');
      const response = await fetch('http://localhost:8000/teacher/get_students/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          semester: semester.value,
          course_name: course_name.value,
        }),
      }); 
      console.log('fetchData end');

      if (response.status === 400) {
          ElMessageBox.alert('找不到符合条件的学生！', '警告', {
          confirmButtonText: '确定',
          type: 'warning'
          })
      } else {
          const data = await response.json()
          students.value = data.students
      }
/*      console.log(data.students.student_names[0]);
      console.log(data.students.student_id[0]);
      console.log(data.count);*/
    };

    const fetchCourses = async () => {
      const response = await fetch('http://localhost:8000/teacher/get_courses/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          semester: semester.value,
        }),
      });

      if (response.ok) {
        const course_data = await response.json();
        console.log(course_data.course_name);
        courses.value = course_data.course_name;
      }
    };

    onMounted(() => {
      fetchData();
      fetchCourses();
    });

    watch(semester, () => {
      fetchCourses();
    });

    return {
      fetchData,
      fetchCourses,
      students,
      semester,
      courses,
      course_name,
    };
  },
};
</script>

<style>
</style>
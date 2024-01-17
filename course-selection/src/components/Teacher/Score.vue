<template>
  <div style="display: flex; justify-content: center; align-items: center; margin-top: 50px;">
    <el-select v-model="semester" placeholder="请选择学期" style="margin-right: 30px; width:150px; margin-bottom: 30px;">
      <el-option
        v-for="item in semesters"
        :key="item"
        :label="item"
        :value="item">
      </el-option>
    </el-select>
    <el-select v-model="course_name" placeholder="请选择课程" style="margin-right: 30px; width:150px; margin-bottom: 30px;">
      <el-option
        v-for="item in course_names"
        :key="item"
        :label="item"
        :value="item">
      </el-option>
    </el-select>

    <el-button style="margin-bottom: 30px;" type="primary" @click="fetchStudentData">查询</el-button>
  </div>
  <!--<el-table :data="students" style="width: 100%; margin-top: 50px;">
    <el-table-column prop="student_id" label="学号"></el-table-column>
    <el-table-column prop="student_name" label="姓名"></el-table-column>
  </el-table>-->
  <div style="display: flex; justify-content: center; align-items: center; width:100%">
    <el-table :data="tableData" border stripe>
      <el-table-column type="index" align="center" class="first-column"></el-table-column>
      <el-table-column
        label="学号"
        prop="student_id"
        width="120px"
        align="center"
      ></el-table-column>
      <el-table-column
        label="姓名"
        prop="student_name"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column
        label="课程号"
        prop="course_id"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column
        label="课程名"
        prop="course_name"
        width="150px"
        align="center"
      ></el-table-column>
      <el-table-column
        label="学期"
        prop="semester"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column
        label="分数"
        prop="score"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column label="录入成绩" align="center" >
        <template v-slot="{row}">
          <el-button
            type="primary"
            class="center-text"               
            @click="showAddScoreDialog(row)"
            >录入成绩</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref,onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessageBox } from 'element-plus';

export default {
  setup() {

    const route = useRoute();
    const username = route.params.username;
    const semester = ref(['202301', '202302', '202303', '202304']);
    const course_name = ref([]);
    const students = ref([]);
    const course_names = ref([]);
    const course_ids = ref([]);
    const course_id = ref([]);
    const score = ref([]);
    const forceUpdate = ref(0);
    const addForm = {
      semester: '',
      student_id: '',
      student_name: '',
      course_id: '', 
      course_name: '',
      score: '',
    }
    const addFormRules = {
      score: [
        { required: true, message: '请输入成绩', trigger: 'blur' },
        { type: 'number', message: '成绩必须为数字值' },
      ],
    }
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
//        console.log(course_data.course_names[0]);
        course_names.value = course_data.course_name;
        course_ids.value = course_data.course_id;
      }
    };

    const fetchCourseId = async () => {
      console.log('fetchCourseId start')
      const response = await fetch('http://localhost:8000/teacher/get_course_id/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          course_name: course_name.value,
        }),
      });
      console.log('fetchCourseId end')
      if (response.ok) {
        const course_id_data = await response.json();
//        console.log(course_id_data)
        course_id.value = course_id_data.course_id;
        addForm.course_id = course_id_data.course_id;
      }
    };

    const fetchStudentData = async () => {
      students.value = [];
//      console.log(semester.value);
      console.log('fetchStudentData start');
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
      console.log('fetchStudentData end');

      if (response.status === 400) {
          ElMessageBox.alert('找不到符合条件的学生！', '警告', {
          confirmButtonText: '确定',
          type: 'warning'
          })
      } else {
          const student_data = await response.json()
          students.value = student_data.students
          addForm.student_id = student_data.students[0].student_id;
          addForm.student_name = student_data.students[0].student_name;
//          console.log(students.value);
      }
    };

    const showAddScoreDialog = async (row) => {
      const { value: form } = await ElMessageBox.confirm(`
        <div style="font-size: 16px;">
          <div style="display: flex; justify-content: space-between;">
            <span>学号: <b>${row.student_id}</b></span>
            <span>姓名: <b>${row.student_name}</b></span>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span>课程号: <b>${row.course_id}</b></span>
            <span>课程名: <b>${row.course_name}</b></span>
          </div>
          <div style="font-size: 20px; margin-top: 10px;">
            请输入成绩: <input type="number" id="score-input" style="width: 100px; height: 30px; font-size: 20px; border: 1px solid #000;" />
          </div>
        </div>
      `, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        dangerouslyUseHTMLString: true,
      });

      row.score = document.getElementById('score-input').value;
//      console.log(addForm.score);
//      console.log(tableData.score);
      if (form === null) {
        return;
      }
      const response = await fetch('http://localhost:8000/teacher/add_score/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          semester: semester.value,
          student_id: row.student_id,
          student_name: row.student_name,
          course_id: row.course_id,
          course_name: row.course_name,
          score: row.score,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        row.score = data.score;
        if (response.status === 200) {
          ElMessageBox.alert('录入成功！', '提示', {
            confirmButtonText: '确定',
            type: 'success',
          });
        await getScore();
        } else {
          ElMessageBox.alert('录入失败！', '提示', {
            confirmButtonText: '确定',
            type: 'error',
          });
        }
      }
    }

    const getScore = async () => {
      console.log('getScore start');
      const response = await fetch('http://localhost:8000/teacher/get_score/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          semester: semester.value,
          course_id: addForm.course_id,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        if (response.status === 200) {
          score.value = data.score;
        } else {
          ElMessageBox.alert('获取成绩失败！', '提示', {
            confirmButtonText: '确定',
            type: 'error',
          });
        }
      }
      console.log('getScore end');
    }

    watch(semester, async () => {
      await fetchCourses();
    });

    watch(course_name, async () => {
      addForm.course_name = course_name.value;
      await fetchCourseId();
      await fetchStudentData();
      getScore();
      forceUpdate.value += 1;
    });

    const tableData = computed(() => {
      console.log(forceUpdate.value)
      return students.value.map((students, index) => {
        const studentScore = score.value[index];
//        console.log(studentScore);
        return {
          student_id: students.student_id,
          student_name: students.student_name,
          course_id: course_id,
          course_name: course_name,
          semester: semester,
          score: studentScore,
        };
      
      });
    });

    onMounted(() => {
      fetchCourses();
    });

    return {
      username,
      semester,
      semesters: ['202301', '202302', '202303', '202304'],
      course_name,
      students,
      course_names,
      course_ids,
      course_id,
      score,
      fetchStudentData,
      fetchCourseId,
      fetchCourses,
      showAddScoreDialog,
      getScore,
      tableData,
      addForm,
      addFormRules,
    };
  },
};
</script>

<style>
.first-column .cell {
  margin-left: 200px;
}
</style>
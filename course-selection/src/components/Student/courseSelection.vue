<template>
      <div>
      <!-- 查询开课 -->
      <el-card class="box-card">
        <!-- 查询区域 -->
        <el-form :inline="true">
          <el-form-item label="课程号">
            <el-input
              placeholder="请输入课程号"
              v-model="searchQuery.course_id"
            ></el-input>
          </el-form-item> 
          <el-form-item label="教师号">
            <el-input
              placeholder="请输入教师号"
              v-model="searchQuery.teacher_id"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="getClassList()">
              <el-icon><Search/></el-icon>查询课程
            </el-button>
          </el-form-item>
        </el-form>
        <!-- 列表区域 -->
        <el-table :data="ClassListShow" border stripe>
          <!-- 自定义索引 -->
          <el-table-column type="index"> </el-table-column>
          <el-table-column prop="course_id" label="课程号"></el-table-column>
          <el-table-column prop="course_name" label="课程名"></el-table-column>
          <el-table-column prop="class_time" label="上课时间"></el-table-column>
          <el-table-column prop="credit" label="学分"></el-table-column>
          <el-table-column prop="teacher_id" label="教师号"></el-table-column>
          <el-table-column prop="teacher_name" label="教师名"></el-table-column>
          <el-table-column prop="capacity" label="容量"></el-table-column>
          <el-table-column prop="current_num" label="人数"></el-table-column>
          <el-table-column label="操作">
            <template v-slot:default="scope">
              <el-button
                type="primary"
                size="small"
                @click="addClass(scope.row)"
              >
              <el-icon><Plus/></el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页栏 -->
        <el-pagination
          class="pagination"
          :current-page="currentPage"
          :page-sizes="[5, 10, 15]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @current-change="currentPage = $event"
          @size-change="pageSize = $event"
        >
        </el-pagination>
      </el-card>
      <!-- 已选选列表 -->
      <el-card class="box-card">
        <div><h1>已选课程</h1></div>
        <!-- 列表区域 -->
        <el-table :data="SelectListShow" border stripe>
          <!-- 自定义索引 -->
          <el-table-column type="index"> </el-table-column>
          <el-table-column prop="course_id" label="课程号"></el-table-column>
          <el-table-column prop="course_name" label="课程名"></el-table-column>
          <el-table-column prop="class_time" label="上课时间"></el-table-column>
          <el-table-column prop="credit" label="学分"></el-table-column>
          <el-table-column prop="teacher_id" label="教师号"></el-table-column>
          <el-table-column prop="teacher_name" label="教师名"></el-table-column>
          <el-table-column prop="capacity" label="容量"></el-table-column>
          <el-table-column prop="current_num" label="人数"></el-table-column>
          <el-table-column label="操作">
            <template v-slot:default="scope">
              <el-button
                type="danger"
                size="small"
                @click="deleteClass(scope.row)"
              >
              <el-icon><Delete/></el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

</template>
<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router';
import { ElMessageBox } from 'element-plus'
export default {

  setup() {
    const searchQuery = reactive({
      course_id: '',
      teacher_id: '',
    })    
    const ClassListShow = ref([]) // 展示的选课列表
    const route = useRoute();
    const total = ref(0) // 选课列表总数
    const currentPage = ref(1) // 当前页面
    const pageSize = ref(5) // 每页展示列表数

    const SelectListShow = ref([]) // 已选课程

    const getClassList = async () => {
      ClassListShow.value = [];
      console.log("getClassList start")
      var query = {}
      query.teacher_id = ''
      query.course_id = ''
      if (searchQuery.course_id != '') {
        query.course_id = searchQuery.course_id
      }
      if (searchQuery.teacher_id != '') {
        query.teacher_id = searchQuery.teacher_id
      }
      query.semester = "202303"
      
      query.student_id = route.params.username
      const res = await fetch('http://localhost:8000/student/courseSelection/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {query:query}
          )
      })
      if (res.status !== 200) {
        console.error('获取开课列表失败')
        return
      }

      const data = await res.json()
      console.log(data)
      let classinfo_data = data.classinfo_data
      // console.log(classinfo_data.length)
      total.value = classinfo_data.length // set total value
      console.log(currentPage.value)
      let start = (currentPage.value - 1) * pageSize.value
      let end = start + pageSize.value
      console.log(start)
      console.log(end)
      ClassListShow.value = classinfo_data.slice(start, end)
      console.log("getClassList end")
    }

    watch([currentPage, pageSize], () => {
      getClassList();
    });

    const getSelectCourseList = async () => {
      SelectListShow.value = [];
      var query = {}
      query.semester = "202303"
      
      query.student_id = route.params.username
      const res = await fetch('http://localhost:8000/student/courseSelected/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {query:query}
        )
      })
      if (res.status !== 200) {
        console.error('获取选课列表失败')
        return
      }
      const data = await res.json()
      console.log(data)
      let classinfo_data = data.classinfo_data
      for (let data of classinfo_data){
        SelectListShow.value.push(data)
    }
  }
    const addClass = async (row) => {
      let course_id = row.course_id
      let semester = "202303"
      let teacher_id = row.teacher_id
      
      let student_id = route.params.username
      const res = await fetch('http://localhost:8000/student/addClass/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {course_id:course_id,semester:semester,student_id:student_id,
            teacher_id:teacher_id}
        )
      })

      if (res.status !== 200) {
        const data = await res.json()
        if (res.status === 400 && data.error === 'Time conflict') {
          ElMessageBox.alert('添加课程失败：时间冲突', '警告', {
            confirmButtonText: '确定',
            type: 'warning'
          })
        } else {
          console.error('添加课程失败')
        }
        return
      }

      const data = await res.json()
      console.log(data)
      await getSelectCourseList()
      await getClassList()
    }

    const deleteClass = async (row) => {
      let course_id = row.course_id
      let semester = "202303"
      let teacher_id = row.teacher_id
      
      let student_id = route.params.username
      const res = await fetch('http://127.0.0.1:8000/student/deleteClass/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {
            course_id:course_id,
            semester:semester,
            student_id:student_id,
            teacher_id:teacher_id
          }
        )
      })

      if (res.status !== 200) {
        console.error('删除课程失败')
        return
      }

      const data = await res.json()
      console.log(data)
      await getSelectCourseList()
      await getClassList()
    }

    onMounted(() => {
      getClassList()
      getSelectCourseList()
    })

    return {
      searchQuery,
      ClassListShow,
      total,
      currentPage,
      pageSize,
      SelectListShow,
      getClassList,
      addClass,
      deleteClass,
    }
  },
  
}
</script>
<style  scoped>



.box-card {
  margin-top: 10px;
}
.select {
  width: 120px;
}
.pagination {
  margin-top: 15px;
}
</style>
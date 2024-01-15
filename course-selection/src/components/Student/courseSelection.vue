<template>


      <div>
      <!-- 查询开课 -->
      <el-card class="box-card">
        <!-- 查询区域 -->
        <el-form :inline="true">
          <el-form-item label="课程号">
            <el-input
              placeholder="请输入课程号"
              v-model="searchQuery.course"
            ></el-input>
          </el-form-item>
          <el-form-item label="教师号">
            <el-input
              placeholder="请输入教师号"
              v-model="searchQuery.teacher"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search"  >查询课程</el-button>
          </el-form-item>
        </el-form>
        <!-- 列表区域 -->
        <el-table :data="OpenListShow" border stripe>
          <!-- 自定义索引 -->
          <el-table-column type="index"> </el-table-column>
          <el-table-column
            prop="course.course_id"
            label="课程号"
          ></el-table-column>
          <el-table-column
            prop="course.course_name"
            label="课程名"
          ></el-table-column>
          <el-table-column prop="course.credit" label="学分"></el-table-column>
          <el-table-column
            prop="teacher.user.user_id"
            label="教师号"
          ></el-table-column>
          <el-table-column
            prop="teacher.user.user_name"
            label="教师名"
          ></el-table-column>
          <el-table-column prop="semester" label="学期"></el-table-column>
          <el-table-column prop="course_time" label="上课时间"></el-table-column>
          <el-table-column label="操作">
            <template v-slot:default="scope">
              <el-button
                type="primary"
                icon="el-icon-circle-plus-outline"
                size="mini"
                
              >
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
          <el-table-column prop="open.id" label="开课号"></el-table-column>
          <el-table-column
            prop="open.course.course_id"
            label="课程号"
          ></el-table-column>
          <el-table-column
            prop="open.course.course_name"
            label="课程名"
          ></el-table-column>
          <el-table-column
            prop="open.course_time"
            label="上课时间"
          ></el-table-column>
          <el-table-column
            prop="open.course.credit"
            label="学分"
          ></el-table-column>
          <el-table-column
            prop="open.teacher.user.user_id"
            label="教师号"
          ></el-table-column>
          <el-table-column
            prop="open.teacher.user.user_name"
            label="教师名"
          ></el-table-column>
          <el-table-column label="操作">
            <template v-slot:default="scope">
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
        
              >
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

</template>
<script>
import { ref, reactive, onMounted } from 'vue'

export default {

  setup() {
    const semesterMap = ref([
      { value: '01', label: '春季' },
      { value: '02', label: '夏季' },
      { value: '03', label: '秋季' },
      { value: '04', label: '冬季' },
    ])
    const searchQuery = reactive({
      semester_year: '2021',
      semester_season: '01',
      course: '',
      teacher: '',
    })
    const OpenList = ref([]) // 选课列表
    const OpenListShow = ref([]) // 展示的选课列表
    const total = ref(0) // 选课列表总数
    const currentPage = ref(1) // 当前页面
    const pageSize = ref(5) // 每页展示列表数

    const SelectListShow = ref([]) // 已选课程

    onMounted(() => {
      getOpenList()
      getSelectCourseList()
    })

    return {
      semesterMap,
      searchQuery,
      OpenList,
      OpenListShow,
      total,
      currentPage,
      pageSize,
      SelectListShow,
    
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
<template>
      <el-form :inline="true">
        <el-form-item label="学期">
          <el-select
            v-model="selectedSemester"
            placeholder="请选择学期"
          >
          <!-- todo -->
            <el-option
              v-for="(item, index) in semester_list" 
              :key="index"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

    <el-table :data="times" style="width: 100%">
      <el-table-column prop="index" label="序号"></el-table-column>
      <el-table-column prop="time" label="上课时间"></el-table-column>
      <el-table-column prop="Mon" label="一"></el-table-column>
      <el-table-column prop="Tue" label="二"></el-table-column>
      <el-table-column prop="Wed" label="三"></el-table-column>
      <el-table-column prop="Thu" label="四"></el-table-column>
      <el-table-column prop="Fri" label="五"></el-table-column>
    </el-table>

</template>

<script>
import { ref,onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

export default {

  setup() {
    const times = ref([]);
    const selectedSemester = ref(null)
    const semester_list = ref([])

    const route = useRoute();

    const fetchSemester = async (selectedSemester) => {
      const response = await fetch('http://localhost:8000/student/getSemester/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        })
      });

      const data = await response.json();
      if (response.ok) {
        semester_list.value = data.semesters
        console.log(data.semesters)
        selectedSemester.value = data.semesters[data.semesters.length - 1]
        console.log(selectedSemester.value)
        console.log(semester_list.value)
      }
    }

    const fetchData = async (selectedSemester) => {
        times.value = [
        { index: 1, time: '8:00-8:45' },
        { index: 2, time: '8:55-9:40' },
        { index: 3, time: '10:00-10:45' },
        { index: 4, time: '10:55-11:40' },
        { index: 5, time: '13:00-13:45' },
        { index: 6, time: '13:55-14:40' },
        { index: 7, time: '15:00-15:45' },
        { index: 8, time: '15:55-16:40' },
        { index: 9, time: '18:00-18:45' },
        { index: 10, time: '18:55-19:40' },
        { index: 11, time: '20:00-20:45' },
        { index: 12, time: '20:55-21:40' },
      ];
      console.log('fetchData start');
      const username = route.params.username;
      const semester = selectedSemester.value;
      console.log(username);
      const response = await fetch('http://localhost:8000/student/courseTabel/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          semester: semester
        })
      });
      console.log('fetchData end');

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        let courseinfo_data = data.courseinfo_data;
        for (let i = 0; i < courseinfo_data.length; i++) {
        console.log(i);
        let course_name = courseinfo_data[i].course_name;
        let DoW = courseinfo_data[i].DayofWeek;
        let class_begin = courseinfo_data[i].class_begin;
        let class_len_1 = courseinfo_data[i].class_len_1;
        let class_place = courseinfo_data[i].class_place;
        let teacher_name = courseinfo_data[i].teacher_name;
        let class_info = course_name + '\n'+ teacher_name + '\n' 
          + class_place + '\n';
        console.log(DoW);
        console.log(class_info);
        console.log(class_begin);
        console.log(class_len_1);
        for (let j = class_begin; j <= class_begin + class_len_1; j++) {
          times.value[j][DoW] = class_info;
          console.log(times.value[j][DoW]);
        }
      }
      } else {
        console.error(data.error);
        alert('获取课表失败');
      }
    };

    watch(selectedSemester, () => {
      fetchData(selectedSemester);
    });

    onMounted(() => {
      fetchSemester(selectedSemester);
      fetchData(selectedSemester);
    });

    return {
      times,
      semester_list,
      selectedSemester,
    };
  },
};
</script>

<style>
.el-table .cell {
  white-space: pre-wrap;
}
</style>
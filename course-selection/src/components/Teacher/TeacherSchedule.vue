<template>
  <div>
    <div class="flex items-center justify-center mt-10">
      <span class="text-lg font-medium leading-6 text-gray-900">选择学期</span>
      <Listbox as="div" v-model="selectedSemester">
        <div class="relative mx-2">
          <ListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 sm:text-sm sm:leading-6">
            <span class="flex items-center">
              <span class="ml-3 block truncate">{{ selectedSemester }}</span>
            </span>
            <span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
            </span>
          </ListboxButton>

          <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
            <ListboxOptions class="absolute z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
              <ListboxOption v-for="semester in ['202301', '202302', '202303', '202304']" :key="semester" :value="semester" v-slot="{ active, selected }">
                <li :class="[active ? 'bg-indigo-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                  <div class="flex items-center">
                    <span :class="[selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate']">{{ semester }}</span>
                  </div>

                  <span v-if="selected" :class="[active ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                  </span>
                </li>
              </ListboxOption>
            </ListboxOptions>
          </transition>
        </div>
      </Listbox>
      <button 
        class="mt-0 px-6 py-2 bg-blue-500 text-white rounded" 
        @click="fetchData(selectedSemester)"
      >
        查询
      </button>
    </div>
    <el-table :data="times" style="width: 100%; margin-top: 30px;">
      <el-table-column prop="index" label="序号"></el-table-column>
      <el-table-column prop="time" label="上课时间"></el-table-column>
      <el-table-column prop="Mon" label="一"></el-table-column>
      <el-table-column prop="Tue" label="二"></el-table-column>
      <el-table-column prop="Wed" label="三"></el-table-column>
      <el-table-column prop="Thu" label="四"></el-table-column>
      <el-table-column prop="Fri" label="五"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref,onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Listbox, ListboxButton, ListboxLabel, ListboxOption, ListboxOptions } from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import { ElMessageBox } from 'element-plus';

export default {
  components:{
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
    CheckIcon,
    ChevronUpDownIcon
  },
  setup() {

    const selectedSemester = ref('202301');
    const times = ref([
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
    ]);
    const route = useRoute();
    const fetchData = async () => {
      console.log('fetchData start');
      for (let time of times.value) {
        time.Mon = undefined;
        time.Tue = undefined;
        time.Wed = undefined;
        time.Thu = undefined;
        time.Fri = undefined;
      }
//      times.value = [];
      const username = route.params.username;
      console.log(username);
      const semester = selectedSemester.value;
      console.log(semester);
      const response = await fetch('http://localhost:8000/teacher/TeacherTableInfo/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          semester: semester
        })
      }      
      );
      console.log('fetchData end');
      if (response.status === 500) {
          ElMessageBox.alert('该学期没有课程！', '警告', {
          confirmButtonText: '确定',
          type: 'warning'
          })
      }
      if (response.ok) {      
        const data = await response.json();
        console.log(data.courseinfo_data[0].course_name)
        let courseinfo_data = data.courseinfo_data;
        for (let i = 0; i < courseinfo_data.length; i++) {
          console.log(i);
          let course_name = courseinfo_data[i].course_name;
          let DoW = courseinfo_data[i].DayofWeek;
          let class_begin = courseinfo_data[i].class_begin;
          let class_len_1 = courseinfo_data[i].class_len_1;
          let class_place = courseinfo_data[i].class_place;
          let class_info = course_name + '\n'
                        + class_place + '\n';
/*        console.log(DoW);
          console.log(class_info);
          console.log(class_begin);
          console.log(class_len_1);
*/
          for (let j = class_begin; j <= class_begin + class_len_1; j++) {
            if (!times.value[j]) {
              times.value[j] = {};
            }  
            times.value[j][DoW] = class_info;
            console.log(times.value[j][DoW]);
          }
        }
      } else {
        console.error(data.error);
        ElMessageBox.alert('找不到符合条件的学生！', '警告', {
          confirmButtonText: '确定',
          type: 'warning'
        })
      }
    };

    onMounted(fetchData)

    return {
      times,
      selectedSemester,
      fetchData
    };
  },
};
</script>

<style>
.el-table .cell {
  white-space: pre-wrap;
}
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.input-group {
  margin-right: 10px;
}

.btn {
  background-color: #271ed3;
  border: none;
  color: white;
  padding: 12px 24px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

select {
  width: 200px;
  height: 35px;
  border-radius: 5px;
  border: 1px solid #ccc;
  padding: 5px;
  font-size: 16px;
}
</style>
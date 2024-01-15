import { createRouter, createWebHistory } from 'vue-router'
import myStudent from './components/Student/myStudent.vue'
import myLogin from './components/myLogin.vue'
import courseInfo from './components/Student/courseInfo.vue'
import courseSelection from './components/Student/courseSelection.vue'
import myTeacher from './components/Teacher/myTeacher.vue'
import TeacherSchedule from './components/Teacher/TeacherSchedule.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: myLogin },
  { path: '/student/:username',
    name: 'myStudent',
    component: myStudent,
    children: [
      { path: 'courseInfo', name: 'courseInfo', component: courseInfo },
      { path: 'courseSelection', name: 'courseSelection', component: courseSelection }
    ]
  },
  { path: '/teacher/:username',
    name: 'myTeacher',
    component: myTeacher,
    children: [
      { path: 'TeacherSchedule', name: 'TeacherSchedule/s', component: TeacherSchedule }
    ]
  },
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
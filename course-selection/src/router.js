import { createRouter, createWebHistory } from 'vue-router'
import myStudent from './components/Student/myStudent.vue'
import myLogin from './components/myLogin.vue'
import courseInfo from './components/Student/courseInfo.vue'
import courseSelection from './components/Student/courseSelection.vue'
import myTeacher from './components/Teacher/myTeacher.vue'
import TeacherSchedule from './components/Teacher/TeacherSchedule.vue'
import MyClass from './components/Teacher/MyClass.vue'
import Score from './components/Teacher/Score.vue'
import scoreAnalysis from './components/Student/scoreAnalysis.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: myLogin, name:'myLogin'},
  { path: '/student/:username',
    name: 'myStudent',
    component: myStudent,
    children: [
      { path: 'courseInfo', name: 'courseInfo', component: courseInfo },
      { path: 'courseSelection', name: 'courseSelection', component: courseSelection },
      { path: 'scoreAnalysis', name: 'scoreAnalysis', component: scoreAnalysis }
    ]
  },
  { path: '/teacher/:username',
    name: 'myTeacher',
    component: myTeacher,
    children: [
      { path: 'TeacherSchedule', name: 'TeacherSchedule', component: TeacherSchedule },
      { path: 'MyClass', name: 'MyClass', component: MyClass },
      { path: 'Score', name: 'Score', component: Score }
    ]
  },
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
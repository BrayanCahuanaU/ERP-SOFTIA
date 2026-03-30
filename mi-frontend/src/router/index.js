import { createRouter, createWebHistory } from 'vue-router'
import Dhb1140 from '@/views/Dhb1140.vue'
import Tes1010 from '@/views/Tes1010.vue'
import Tes1200 from '@/views/Tes1200.vue'



const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: { template: '<div>LOGIN</div>' } },
  { path: '/mnu1001', name: 'Mnu1001', component: { template: '<div>MENÚ</div>' } },
  { path: '/dhb1140', name: 'Dhb1140', component: Dhb1140 },
  { path: '/tes1010', name: 'Tes1010', component: Tes1010 },
  { path: '/tes1200', name: 'Tes1200', component: Tes1200 }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
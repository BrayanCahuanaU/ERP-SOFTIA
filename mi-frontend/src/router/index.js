import { createRouter, createWebHistory } from 'vue-router'
import Login         from '@/views/Login.vue'
import Mnu1001       from '@/views/Mnu1001.vue'
import Dhb1140       from '@/views/Dhb1140.vue'
import Tes1010       from '@/views/Tes1010.vue'
import Tes1200       from '@/views/Tes1200.vue'
import NotFound      from '@/views/NotFound.vue'
import AccessDenied  from '@/views/AccessDenied.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login',   name: 'Login',   component: Login },
  { path: '/mnu1001', name: 'Mnu1001', component: Mnu1001, meta: { requiresAuth: true } },
  { path: '/dhb1140', name: 'Dhb1140', component: Dhb1140, meta: { requiresAuth: true } },
  { path: '/tes1010', name: 'Tes1010', component: Tes1010, meta: { requiresAuth: true } },
  { path: '/tes1200', name: 'Tes1200', component: Tes1200, meta: { requiresAuth: true } },
  { path: '/403', name: 'AccessDenied', component: AccessDenied },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ── Router Guard ──────────────────────────────────────────────
router.beforeEach((to, from, next) => {
  const userType = sessionStorage.getItem('USER_TYPE')
  const isAuthenticated = !!userType

  // Si la ruta requiere autenticación
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // No está autenticado, redirigir a login
      sessionStorage.clear()
      next('/login')
    } else {
      // Está autenticado, permitir acceso
      next()
    }
  } else {
    // Rutas públicas (login, 403, 404)
    if (to.path === '/login' && isAuthenticated) {
      // Si ya está autenticado y va a login, redirigir a menú principal
      next('/mnu1001')
    } else {
      next()
    }
  }
})

export default router
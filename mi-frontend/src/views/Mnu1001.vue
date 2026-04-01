<template>
  <div class="mnu-container">
    <div class="mnu-header">
      <div class="header-left">
        <span class="logo-mark">●</span>
        <span class="logo-text">SISTEMA ERP — TESIS</span>
      </div>
      <div class="header-right">
        <span class="user-name">{{ pcNombre }}</span>
        <button class="btn-salir" @click="f_Salir">SALIR</button>
      </div>
    </div>

    <div class="mnu-body">
      <h2 class="mnu-titulo">MENÚ DE OPCIONES</h2>
      <div class="mnu-grid">

        <div v-if="pcTipo === 'ESTUDIANTE'" class="mnu-item" @click="f_Ir('/tes1010')">
          <div class="mnu-icon">📄</div>
          <div class="mnu-label">REGISTRAR PLAN DE TESIS</div>
        </div>

        <div v-if="pcTipo === 'ESTUDIANTE'" class="mnu-item mnu-item-disabled">
          <div class="mnu-icon">🔍</div>
          <div class="mnu-label">VER MIS TESIS</div>
          <div class="mnu-badge">PRÓXIMAMENTE</div>
        </div>

        <div v-if="pcTipo === 'ADMINISTRATIVO'" class="mnu-item" @click="f_Ir('/tes1200')">
          <div class="mnu-icon">👨‍⚖️</div>
          <div class="mnu-label">ASIGNAR DICTAMINADORES</div>
        </div>

        <div v-if="pcTipo === 'ADMINISTRATIVO'" class="mnu-item mnu-item-disabled">
          <div class="mnu-icon">🔍</div>
          <div class="mnu-label">VER TESIS REGISTRADAS</div>
          <div class="mnu-badge">PRÓXIMAMENTE</div>
        </div>

      </div>
    </div>

    <div class="mnu-footer">UCSM · Sistema de Gestión de Tesis · {{ new Date().getFullYear() }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router   = useRouter()
const pcNombre = ref('')
const pcTipo   = ref('')

onMounted(() => {
  pcNombre.value = sessionStorage.getItem('CNOMBRE') || 'USUARIO'
  pcTipo.value   = sessionStorage.getItem('USER_TYPE') || ''
})

function f_Ir(ruta) {
  router.push(ruta)
}

function f_Salir() {
  sessionStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
@import url('/src/styles/Mnu1001.css');
</style>

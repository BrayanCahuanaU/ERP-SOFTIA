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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

.mnu-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f0f4f8;
  font-family: 'DM Sans', sans-serif;
}

.mnu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-mark { font-size: 10px; color: #2563eb; }

.logo-text {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #1e293b;
  text-transform: uppercase;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.btn-salir {
  padding: 8px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-salir:hover { background: #dc2626; }

.mnu-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 24px;
}

.mnu-titulo {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #1e293b;
  text-transform: uppercase;
  margin-bottom: 36px;
}

.mnu-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: center;
  max-width: 900px;
}

.mnu-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  width: 200px;
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.mnu-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(37,99,235,0.15);
  border-color: #2563eb;
}

.mnu-icon { font-size: 40px; }

.mnu-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #1e293b;
  text-transform: uppercase;
  text-align: center;
  padding: 0 12px;
}

.mnu-item-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.mnu-badge {
  font-size: 10px;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: 0.08em;
  background: #eff6ff;
  padding: 3px 8px;
  border-radius: 20px;
}

.mnu-footer {
  text-align: center;
  padding: 16px;
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 0.06em;
}
</style>
<template>
  <div class="login-container">
    <!-- Header bar -->
    <div class="login-header">
      <span class="logo-mark">●</span>
      <span class="logo-text">SISTEMA ERP — TESIS</span>
    </div>

    <!-- Main card split in two -->
    <div class="login-card">

      <!-- LEFT: Administrativo -->
      <div class="panel panel-admin">
        <div class="panel-label">ACCESO ADMINISTRATIVO</div>
        <p class="panel-sub">Para personal docente y de gestión</p>

        <form @submit.prevent="loginAdministrativo" class="login-form">
          <div class="form-group">
            <label>CÓDIGO DE USUARIO</label>
            <input
              v-model="pcCodigoUsuario"
              type="text"
              placeholder="Ej: 1221"
              maxlength="4"
              @keyup.enter="loginAdministrativo"
            />
          </div>

          <div class="form-group">
            <label>CONTRASEÑA</label>
            <input
              v-model="pcPassword"
              type="password"
              placeholder="Ingrese contraseña"
              @keyup.enter="loginAdministrativo"
            />
          </div>

          <div class="error-message" v-if="pcErrorAdmin">{{ pcErrorAdmin }}</div>

          <button type="submit" class="btn-submit btn-admin" :disabled="plLoadingAdmin">
            <span class="btn-icon">→</span>
            {{ plLoadingAdmin ? 'INGRESANDO...' : 'INGRESAR' }}
          </button>
        </form>
      </div>

      <!-- Divider -->
      <div class="divider">
        <div class="divider-line"></div>
        <div class="divider-circle">ó</div>
        <div class="divider-line"></div>
      </div>

      <!-- RIGHT: Estudiante -->
      <div class="panel panel-estudiante">
        <div class="panel-label">ESTUDIANTE / EGRESADO</div>
        <p class="panel-sub">Para alumnos regulares y egresados</p>

        <form @submit.prevent="loginEstudiante" class="login-form">
          <div class="form-group">
            <label>DNI</label>
            <input
              v-model="pcDniEstudiante"
              type="text"
              placeholder="Ej: 73343342"
              maxlength="8"
              @keyup.enter="loginEstudiante"
            />
          </div>

          <div class="form-group">
            <label>CONTRASEÑA</label>
            <input
              v-model="pcPasswordEstudiante"
              type="password"
              placeholder="Ingrese contraseña"
            />
          </div>

          <div class="error-message" v-if="pcErrorEst">{{ pcErrorEst }}</div>

          <button type="submit" class="btn-submit btn-estudiante" :disabled="plLoadingEst">
            <span class="btn-icon">→</span>
            {{ plLoadingEst ? 'INGRESANDO...' : 'INGRESAR' }}
          </button>
        </form>
      </div>

    </div>

    <!-- Footer -->
    <div class="login-footer">UCSM · Sistema de Gestión de Tesis · {{ new Date().getFullYear() }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Administrativo
const pcCodigoUsuario  = ref('')
const pcPassword       = ref('')
const plLoadingAdmin   = ref(false)
const pcErrorAdmin     = ref('')

// Estudiante
const pcDniEstudiante      = ref('')
const pcPasswordEstudiante = ref('')
const plLoadingEst         = ref(false)
const pcErrorEst           = ref('')

// ── Login Administrativo ──────────────────────────────────────
async function loginAdministrativo() {
  pcErrorAdmin.value = ''

  if (!pcCodigoUsuario.value) { pcErrorAdmin.value = 'INGRESE SU CÓDIGO DE USUARIO'; return }
  if (!pcPassword.value)      { pcErrorAdmin.value = 'INGRESE SU CONTRASEÑA'; return }
  if (!/^[0-9A-Z\-]{4}$/.test(pcCodigoUsuario.value)) {
    pcErrorAdmin.value = 'CÓDIGO INVÁLIDO (4 caracteres)'; return
  }

  try {
    plLoadingAdmin.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'LOGIN_ADMINISTRATIVO', CCODUSU: pcCodigoUsuario.value, CPASSWORD: pcPassword.value })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { pcErrorAdmin.value = laData.ERROR; return }

    sessionStorage.setItem('CCODUSU',    pcCodigoUsuario.value)
    sessionStorage.setItem('CNOMBRE',    laData.CNOMBRE || '')
    sessionStorage.setItem('USER_TYPE',  'ADMINISTRATIVO')
    router.push('/mnu1001')
  } catch {
    pcErrorAdmin.value = 'ERROR AL CONECTAR CON EL SERVIDOR'
  } finally {
    plLoadingAdmin.value = false
  }
}

// ── Login Estudiante ──────────────────────────────────────────
async function loginEstudiante() {
  pcErrorEst.value = ''

  if (!pcDniEstudiante.value)          { pcErrorEst.value = 'INGRESE SU DNI'; return }
  if (!/^\d{8}$/.test(pcDniEstudiante.value)) { pcErrorEst.value = 'EL DNI DEBE TENER 8 DÍGITOS'; return }
  if (!pcPasswordEstudiante.value)     { pcErrorEst.value = 'INGRESE SU CONTRASEÑA'; return }

  try {
    plLoadingEst.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ID: 'LOGIN_ESTUDIANTE',
        CNRODNI:   pcDniEstudiante.value,
        CPASSWORD: pcPasswordEstudiante.value
      })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { pcErrorEst.value = laData.ERROR; return }

    // Validar que el backend retorne CUNIACA
    if (!laData.CUNIACA) { pcErrorEst.value = 'UNIDAD ACADÉMICA NO DEFINIDA O INVÁLIDA'; return }

    sessionStorage.setItem('CCODUSU',   laData.CCODEST || '')
    sessionStorage.setItem('CCODEST',   laData.CCODEST || '')
    sessionStorage.setItem('CNRODNI',   pcDniEstudiante.value)
    sessionStorage.setItem('CNOMBRE',   laData.CNOMBRE || '')
    sessionStorage.setItem('CUNIACA',   laData.CUNIACA || '')
    sessionStorage.setItem('USER_TYPE', 'ESTUDIANTE')
    router.push('/mnu1001')
  } catch {
    pcErrorEst.value = 'ERROR AL CONECTAR CON EL SERVIDOR'
  } finally {
    plLoadingEst.value = false
  }
}
</script>

<style scoped>
@import url('/src/styles/Login.css');
</style>
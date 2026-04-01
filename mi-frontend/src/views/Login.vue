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

    sessionStorage.setItem('CCODUSU',   laData.CCODEST || '')
    sessionStorage.setItem('CCODEST',   laData.CCODEST || '')
    sessionStorage.setItem('CNRODNI',   pcDniEstudiante.value)
    sessionStorage.setItem('CNOMBRE',   laData.CNOMBRE || '')
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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Root ──────────────────────────────────────────────────── */
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f0f4f8;
  font-family: 'DM Sans', sans-serif;
  gap: 0;
}

/* ── Header ────────────────────────────────────────────────── */
.login-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 28px;
}

.logo-mark {
  font-size: 10px;
  color: #2563eb;
}

.logo-text {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: #1e293b;
  text-transform: uppercase;
}

/* ── Card ──────────────────────────────────────────────────── */
.login-card {
  display: flex;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08), 0 1px 4px rgba(0,0,0,0.04);
  overflow: hidden;
  width: 100%;
  max-width: 820px;
  border: 1px solid #e2e8f0;
}

/* ── Panels ────────────────────────────────────────────────── */
.panel {
  flex: 1;
  padding: 40px 36px 44px;
  display: flex;
  flex-direction: column;
}

/* Admin panel: white */
.panel-admin {
  background: #ffffff;
}

/* Estudiante panel: light blue tonal (like Category 4 in the image) */
.panel-estudiante {
  background: #eff6ff;
}

.panel-label {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #2563eb;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.panel-sub {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 28px 0;
  font-weight: 400;
}

/* ── Divider ───────────────────────────────────────────────── */
.divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 2px;
  gap: 8px;
}

.divider-line {
  flex: 1;
  width: 1px;
  background: #e2e8f0;
}

.divider-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 11px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  flex-shrink: 0;
}

/* ── Form ──────────────────────────────────────────────────── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #475569;
  text-transform: uppercase;
}

.form-group input,
.form-group select {
  padding: 11px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 6px;
  font-size: 15px;
  font-family: 'DM Sans', sans-serif;
  color: #1e293b;
  background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.panel-estudiante .form-group input,
.panel-estudiante .form-group select {
  background: #ffffff;
  border-color: #bfdbfe;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-group input::placeholder {
  color: #cbd5e1;
}

/* ── Error ─────────────────────────────────────────────────── */
.error-message {
  background: #fef2f2;
  color: #b91c1c;
  padding: 10px 13px;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 600;
  border-left: 3px solid #ef4444;
  letter-spacing: 0.02em;
}

/* ── Buttons ───────────────────────────────────────────────── */
.btn-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  margin-top: auto;
}

.btn-admin {
  background: #1e293b;
  color: #ffffff;
}

.btn-admin:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.btn-estudiante {
  background: #2563eb;
  color: #ffffff;
}

.btn-estudiante:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 14px;
  line-height: 1;
}

/* ── Footer ────────────────────────────────────────────────── */
.login-footer {
  margin-top: 20px;
  font-size: 12.5px;
  color: #94a3b8;
  letter-spacing: 0.06em;
}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 640px) {
  .login-card {
    flex-direction: column;
    max-width: 400px;
  }

  .divider {
    flex-direction: row;
    padding: 2px 0;
  }

  .divider-line {
    flex: 1;
    height: 1px;
    width: auto;
  }

  .panel {
    padding: 32px 24px;
  }
}
</style>
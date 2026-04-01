<template>
  <div class="tes-container">
    <!-- Header -->
    <div class="tes-header">
      <span class="logo-mark">●</span>
      <span class="logo-text">REGISTRAR PLAN DE TESIS</span>

      <!-- Nombre usuario -->
      <div class="user-info">
        {{ pcNombre }}
      </div>
    </div>

    <!-- Main content -->
    <div class="tes-content">

      <!-- PANTALLA 1.1 - Selección de carrera -->
      <div v-if="pcScreen === '1'" class="screen screen-1">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">SELECCIONE LA CARRERA</h2>
            <p class="card-sub">Elija la carrera académica para registrar el plan de tesis</p>
          </div>

          <div class="form-group">
            <label class="form-label">CARRERA</label>
            <select v-model="pcCodest" class="form-input">
              <option value="">— Seleccione —</option>
              <option v-for="item in paDatos" :key="item.CCODEST" :value="item.CCODEST">
                {{ item.CNOMUNI }}
              </option>
            </select>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Salir">SALIR</button>
            <button class="btn btn-primary" @click="f_Aplicar">APLICAR</button>
          </div>
        </div>
      </div>

      <!-- PANTALLA 1.2 - Búsqueda de egresados -->
      <div v-if="pcScreen === '2'" class="screen screen-2">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">AGREGAR EGRESADOS</h2>
            <p class="card-sub">Carrera: <strong>{{ pcNomUni }}</strong></p>
          </div>

          <!-- Egresados agregados -->
          <div class="section">
            <h3 class="section-title">EGRESADOS SELECCIONADOS</h3>
            <div class="table-wrapper">
              <table class="table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>DNI</th>
                    <th>NOMBRE</th>
                    <th>CÓDIGO</th>
                    <th style="width:50px;"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in paEgresados" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.CNRODNI }}</td>
                    <td>{{ item.CNOMBRE }}</td>
                    <td>{{ item.CCODEST }}</td>
                    <td style="text-align:center; cursor:pointer; color:#ef4444;" @click="f_EliminarEgresado(index)">✕</td>
                  </tr>
                  <tr v-if="!paEgresados.length" class="empty-row">
                    <td colspan="5">NO HAY EGRESADOS AGREGADOS</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Búsqueda de egresado -->
          <div v-if="paEgresados.length < 2" class="section">
            <h3 class="section-title">BUSCAR EGRESADO</h3>
            <div class="form-group">
              <label class="form-label">DNI DEL EGRESADO</label>
              <div style="display:flex; gap:10px;">
                <input v-model="pcDniBuscar" maxlength="8" placeholder="Ej: 73343342"
                  class="form-input" style="flex:1;"
                  @input="pcDniBuscar = pcDniBuscar.replace(/[^0-9A-Z]/g, '')"/>
                <button class="btn btn-secondary" @click="f_BuscarEgresado" style="flex-shrink:0;">BUSCAR</button>
              </div>
            </div>
            <div v-if="plLoadingBuscar" style="text-align:center; padding:20px;">
              <Spinner/>
            </div>
            <div v-if="poEgresadoBuscado && poEgresadoBuscado.CNRODNI" class="result-card">
              <div class="result-info">
                <div class="result-dni">{{ poEgresadoBuscado.CNRODNI }}</div>
                <div class="result-name">{{ poEgresadoBuscado.CNOMBRE }}</div>
                <div class="result-code">{{ poEgresadoBuscado.CCODEST }}</div>
              </div>
              <button class="btn btn-primary" @click="f_AgregarEgresado">AGREGAR</button>
            </div>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Volver1">VOLVER</button>
            <button class="btn btn-primary" @click="f_Continuar">CONTINUAR</button>
          </div>
        </div>
      </div>

      <!-- PANTALLA 1.3 - Grabar plan de tesis -->
      <div v-if="pcScreen === '3'" class="screen screen-3">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">REGISTRAR PLAN DE TESIS</h2>
            <p class="card-sub">Complete los datos del plan antes de grabar</p>
          </div>

          <!-- Datos del estudiante -->
          <div class="info-panel">
            <div class="info-item">
              <span class="info-label">CARRERA</span>
              <span class="info-value">{{ pcNomUni }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">EGRESADO(S)</span>
              <span class="info-value">
                <span v-for="(item, index) in paEgresados" :key="index">
                  {{ item.CNOMBRE }}<span v-if="index < paEgresados.length - 1">, </span>
                </span>
              </span>
            </div>
          </div>

          <!-- Línea -->
          <div class="form-group">
            <label class="form-label">LÍNEA DE INVESTIGACIÓN</label>
            <select v-model="pcLinea" class="form-input">
              <option value="">— Seleccione —</option>
              <option v-for="item in paLineas" :key="item.CLINEA" :value="item.CLINEA">
                {{ item.CLINEA }} - {{ item.CDESCRI }}
              </option>
            </select>
          </div>

          <!-- Título -->
          <div class="form-group">
            <label class="form-label">TÍTULO DEL PLAN</label>
            <textarea v-model="pcTitulo" rows="4" placeholder="Ingrese el título del plan de tesis"
              class="form-input" style="resize:vertical;"></textarea>
          </div>

          <!-- PDF -->
          <div class="form-group">
            <label class="form-label">DOCUMENTO PDF</label>
            <div class="file-input-wrapper">
              <input type="file" accept=".pdf" @change="f_SeleccionarPDF" class="file-input"/>
              <span class="file-input-text">{{ pcNombrePDF || 'Seleccione un archivo PDF' }}</span>
            </div>
            <div v-if="pcNombrePDF" class="file-success">
              ✓ {{ pcNombrePDF }}
            </div>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Volver2">VOLVER</button>
            <button class="btn btn-primary" @click="f_Grabar">GRABAR</button>
          </div>
        </div>
      </div>

    </div>

    <!-- Footer -->
    <div class="tes-footer">UCSM · Sistema de Gestión de Tesis · {{ new Date().getFullYear() }}</div>
  </div>
</template>

<script setup>
import Spinner   from '@/components/Spinner.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router          = useRouter()
const pcScreen        = ref('1')
const plLoading       = ref(false)
const plLoadingBuscar = ref(false)
const plWorking       = ref(false)

// Datos sessionStorage
const pcNrodni = ref('')
const pcNombre = ref('')
const paDatos  = ref([])   // carreras

// Pantalla 1.1
const pcCodest = ref('')
const pcNomUni = ref('')
const pcUniAca = ref('')

// Pantalla 1.2
const paEgresados      = ref([])
const pcDniBuscar      = ref('')
const poEgresadoBuscado = ref(null)

// Pantalla 1.3
const paLineas   = ref([])
const pcLinea    = ref('')
const pcTitulo   = ref('')
const pcNombrePDF = ref('')
const poPDFFile  = ref(null)

onMounted(() => {
  pcNrodni.value = sessionStorage.getItem('CNRODNI') || '76574307'
  pcNombre.value = sessionStorage.getItem('CNOMBRE') || 'ABARCA ARTEAGA XIMENA FERNANDA'
  const lcDatos  = sessionStorage.getItem('DATOS')
  paDatos.value  = lcDatos ? JSON.parse(lcDatos) : [
    { CCODEST: '00412X', CUNIACA: '0005', CNOMUNI: 'CENTRO DE IDIOMAS' },
    { CCODEST: '004VUQ', CUNIACA: '0006', CNOMUNI: 'INSTITUTO DE INFORMATICA' },
    { CCODEST: '003WOQ', CUNIACA: '0049', CNOMUNI: 'INGENIERIA DE SISTEMAS' }
  ]
})

// 1.1 APLICAR
async function f_Aplicar() {
  if (!pcCodest.value) { alert('DEBE SELECCIONAR UNA CARRERA'); return }
  try {
    plLoading.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1010i', CCODEST: pcCodest.value })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    // Guardar datos retornados
    pcUniAca.value = laData.CUNIACA
    pcNomUni.value = laData.CNOMUNI
    paLineas.value = laData.DATOS
    // Agregar estudiante principal a la lista
    paEgresados.value = [{
      CNRODNI: pcNrodni.value,
      CNOMBRE: pcNombre.value,
      CCODEST: pcCodest.value
    }]
    pcScreen.value = '2'
  } catch (e) {
    alert('ERROR AL CONECTAR CON EL SERVIDOR')
  } finally {
    plLoading.value = false
  }
}

// 1.2 BUSCAR EGRESADO
async function f_BuscarEgresado() {
  if (!pcDniBuscar.value) { alert('INGRESE UN DNI'); return }
  poEgresadoBuscado.value = {}
  try {
    plLoadingBuscar.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1010b', CNRODNI: pcDniBuscar.value, CUNIACA: pcUniAca.value })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    // Verificar que no esté ya en la lista
    const lbYaExiste = paEgresados.value.some(x => x.CCODEST === laData.CCODEST)
    if (lbYaExiste) { alert('ESE EGRESADO YA ESTÁ EN LA LISTA'); return }
    poEgresadoBuscado.value = laData
  } catch (e) {
    alert('ERROR AL BUSCAR EGRESADO')
  } finally {
    plLoadingBuscar.value = false
  }
}

// 1.2 AGREGAR EGRESADO A LA LISTA
function f_AgregarEgresado() {
  if (paEgresados.value.length >= 2) {
    alert('MÁXIMO 2 EGRESADOS POR TESIS')
    return
  }
  paEgresados.value.push(poEgresadoBuscado.value)
  poEgresadoBuscado.value = {}
  pcDniBuscar.value = ''
}

// 1.2 ELIMINAR EGRESADO DE LA LISTA
function f_EliminarEgresado(index) {
  if (paEgresados.value.length === 1) {
    alert('DEBE HABER AL MENOS UN EGRESADO')
    return
  }
  paEgresados.value.splice(index, 1)
}

// 1.2 CONTINUAR A PANTALLA 3
function f_Continuar() {
  if (paEgresados.value.length === 0) {
    alert('DEBE HABER AL MENOS UN EGRESADO')
    return
  }
  pcScreen.value = '3'
}

// 1.3 SELECCIONAR PDF
function f_SeleccionarPDF(event) {
  const file = event.target.files[0]
  if (file) {
    poPDFFile.value  = file
    pcNombrePDF.value = file.name
  }
}

// 1.3 GRABAR
async function f_Grabar() {
  if (plWorking.value) return
  if (!pcLinea.value)  { alert('DEBE SELECCIONAR UNA LÍNEA'); return }
  if (!pcTitulo.value) { alert('DEBE INGRESAR EL TÍTULO');    return }
  plWorking.value = true
  try {
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ID:      'TES1010g',
        CLINEA:  pcLinea.value,
        CUNIACA: pcUniAca.value,
        MTITULO: pcTitulo.value.toUpperCase(),
        ACODEST: paEgresados.value.map(x => x.CCODEST).filter(x => x != null && x !== '')
      })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    alert('PLAN DE TESIS GRABADO CORRECTAMENTE')
    router.push('/mnu1001')
  } catch (e) {
    alert('ERROR AL GRABAR')
  } finally {
    plWorking.value = false
  }
}

function f_Volver1() { pcScreen.value = '1' }
function f_Volver2() { pcScreen.value = '2' }
function f_Salir()   { router.push('/mnu1001') }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Root ──────────────────────────────────────────────────── */
.tes-header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Logo izquierda, usuario derecha */
  padding: 16px 24px;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #e2e8f0;
  font-family: 'DM Sans', sans-serif;
  z-index: 10;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 8px; /* espacio entre el punto y el texto */
  justify-content: flex-start; /* fuerza que el logo quede a la izquierda */
}

.logo-mark {
  font-size: 12px;
  color: #2563eb;
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #1e293b;
  text-transform: uppercase;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.user-info:hover {
  color: #2563eb;
  cursor: pointer;
}

.user-info::before {
  content: '';
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #2563eb;
  display: inline-block;
}

.tes-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f4f8 0%, #f8fafc 100%);
  font-family: 'DM Sans', sans-serif;
  padding: 20px;
  gap: 20px;
}

/* ── Header ────────────────────────────────────────────────── */
.tes-header {
  display: flex;
  align-items: center;
  gap: 10px;
  position: absolute;
  top: 20px;
  left: 20px;
}

.logo-mark {
  font-size: 10px;
  color: #2563eb;
}

.logo-text {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #1e293b;
  text-transform: uppercase;
}

/* ── Content ───────────────────────────────────────────────── */
.tes-content {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.screen {
  width: 100%;
  max-width: 720px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ── Card ──────────────────────────────────────────────────── */
.card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08), 0 1px 4px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  padding: 40px 40px;
  width: 100%;
}

.card-header {
  margin-bottom: 32px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #1e293b;
  text-transform: uppercase;
  margin: 0;
  margin-bottom: 6px;
}

.card-sub {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  font-weight: 400;
}

/* ── Sections ──────────────────────────────────────────────── */
.section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #475569;
  text-transform: uppercase;
  margin: 0 0 14px 0;
}

/* ── Form ──────────────────────────────────────────────────── */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #475569;
  text-transform: uppercase;
}

.form-input {
  padding: 11px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
  color: #1e293b;
  background: #ffffff;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.form-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-input::placeholder {
  color: #cbd5e1;
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

/* ── File Input ────────────────────────────────────────────── */
.file-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  border: 1.5px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  background: #ffffff;
  transition: border-color 0.2s;
}

.file-input-wrapper:hover {
  border-color: #cbd5e1;
}

.file-input {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-input-text {
  padding: 11px 14px;
  color: #64748b;
  font-size: 14px;
  flex: 1;
  pointer-events: none;
}

.file-success {
  margin-top: 8px;
  color: #16a34a;
  font-size: 13px;
  font-weight: 600;
}

/* ── Table ─────────────────────────────────────────────────── */
.table-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  max-height: 400px;
  overflow-y: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table thead {
  background: #f8fafc;
  position: sticky;
  top: 0;
}

.table th {
  padding: 12px 14px;
  text-align: left;
  font-weight: 700;
  color: #475569;
  font-size: 12px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-bottom: 1px solid #e2e8f0;
}

.table td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
}

.table tbody tr:hover {
  background: #f8fafc;
}

.empty-row td {
  text-align: center;
  color: #94a3b8;
  font-weight: 500;
  padding: 20px 14px;
}

/* ── Info Panel ────────────────────────────────────────────── */
.info-panel {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 16px 18px;
  margin-bottom: 28px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #64748b;
  text-transform: uppercase;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

/* ── Result Card ───────────────────────────────────────────── */
.result-card {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  padding: 16px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.result-info {
  flex: 1;
}

.result-dni {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.result-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 2px;
}

.result-code {
  font-size: 12px;
  color: #64748b;
}

/* ── Buttons ───────────────────────────────────────────────── */
.button-group {
  display: flex;
  gap: 10px;
  margin-top: 32px;
}

.button-group-end {
  justify-content: flex-end;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 11px 20px;
  border: none;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  outline: none;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: #2563eb;
  color: #ffffff;
}

.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}

.btn-secondary {
  background: #e2e8f0;
  color: #1e293b;
}

.btn-secondary:hover {
  background: #cbd5e1;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* ── Footer ────────────────────────────────────────────────── */
.tes-footer {
  position: absolute;
  bottom: 20px;
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 640px) {
  .tes-container {
    padding: 20px 16px;
  }

  .tes-header {
    position: static;
    margin-bottom: 20px;
  }

  .card {
    padding: 28px 20px;
  }

  .info-panel {
    grid-template-columns: 1fr;
  }

  .button-group {
    flex-direction: column-reverse;
  }

  .result-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
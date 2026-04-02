<template>
  <div class="tes-container">
    <!-- Header -->
    <div class="tes-header">
      <span class="logo-mark">●</span>
      <span class="logo-text">REGISTRAR PLAN DE TESIS</span>
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

          <div v-if="plLoading" style="text-align:center; padding:40px;">
            <Spinner/>
          </div>

          <div v-else class="form-group">
            <label class="form-label">CARRERA</label>
            <div class="career-options">
              <div v-for="item in paDatos" :key="item.CUNIACA" 
                   @click="pcCodest = item.CUNIACA"
                   :class="['career-option', { 'career-assigned': item.CUNIACA === pcUniAcaAsignada, 'career-selected': item.CUNIACA === pcCodest }]">
                <div class="career-label">{{ item.CNOMUNI }}</div>
                <div v-if="item.CUNIACA === pcUniAcaAsignada" class="career-badge">TU CARRERA</div>
              </div>
            </div>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Salir">SALIR</button>
            <button class="btn btn-primary" @click="f_Aplicar" v-if="!plLoading">APLICAR</button>
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
            <button class="btn btn-secondary" @click="f_Volver('1')">VOLVER</button>
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

          <!-- PDF del plan -->
          <div class="form-group">
            <label class="form-label">ARCHIVO PDF DEL PLAN</label>
            <div class="pdf-upload-container">
              <input 
                ref="inputFile"
                type="file" 
                accept=".pdf" 
                style="display:none;"
                @change="f_SeleccionarPDF"
              />
              <button type="button" class="btn btn-secondary" @click="$refs.inputFile.click()">
                📎 SELECCIONAR PDF
              </button>
              <div v-if="pcNombrePDF" class="pdf-selected">
                <span class="pdf-icon">✓</span>
                <span class="pdf-name">{{ pcNombrePDF }}</span>
                <span class="pdf-remove" @click="f_LimpiarPDF">✕</span>
              </div>
            </div>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Volver('2')">VOLVER</button>
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

// Datos del login (sessionStorage)
const pcCodEst = sessionStorage.getItem('CCODEST') || sessionStorage.getItem('CCODUSU') || ''
const pcNrodni = sessionStorage.getItem('CNRODNI') || ''
const pcNombre = sessionStorage.getItem('CNOMBRE') || ''
const pcUniAca = ref(sessionStorage.getItem('CUNIACA') || '')

// Pantalla 1.1
const pcCodest = ref('')
const paDatos  = ref([])
const pcNomUni = ref('')
const pcUniAcaAsignada = ref('')  // Carrera asignada del estudiante

// Pantalla 1.2
const paEgresados       = ref([])
const pcDniBuscar       = ref('')
const poEgresadoBuscado = ref(null)

// Pantalla 1.3
const paLineas   = ref([])
const pcLinea    = ref('')
const pcTitulo   = ref('')
const pcNombrePDF = ref('')
const poPDFFile  = ref(null)

onMounted(async () => {
  if (!pcCodEst) {
    alert('DATOS DE SESIÓN INVÁLIDOS. POR FAVOR INICIE SESIÓN')
    return
  }
  try {
    plLoading.value = true
    // Cargar todas las carreras disponibles
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1010c', CCODEST: pcCodEst })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) {
      alert(laData.ERROR)
      return
    }
    // Guardar carreras disponibles
    paDatos.value = laData.DATOS || []
    pcUniAcaAsignada.value = laData.CUNIACA_ESTUDIANTE || ''
    // Preseleccionar la carrera asignada
    pcCodest.value = pcUniAcaAsignada.value
  } catch (e) {
    console.error('Error al cargar carreras:', e)
    alert(`ERROR AL CARGAR CARRERAS: ${e.message}`)
  } finally {
    plLoading.value = false
  }
})

// 1.1 APLICAR
async function f_Aplicar() {
  if (!pcCodest.value) { alert('DEBE SELECCIONAR UNA CARRERA'); return }
  try {
    plLoading.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1010i', CCODEST: pcCodEst, CUNIACA: pcCodest.value })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    // Guardar datos retornados
    pcUniAca.value = laData.CUNIACA
    pcNomUni.value = laData.CNOMUNI
    paLineas.value = laData.DATOS || []
    // Agregar estudiante principal a la lista
    paEgresados.value = [{
      CNRODNI: pcNrodni,
      CNOMBRE: pcNombre,
      CCODEST: pcCodEst
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
  try {
    plLoadingBuscar.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1010b', CNRODNI: pcDniBuscar.value, CUNIACA: pcUniAca.value })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
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
  poEgresadoBuscado.value = null
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

// 1.3 GRABAR
async function f_Grabar() {
  if (plWorking.value) return
  if (!pcLinea.value)  { alert('DEBE SELECCIONAR UNA LÍNEA'); return }
  if (!pcTitulo.value) { alert('DEBE INGRESAR EL TÍTULO');    return }
  if (!poPDFFile.value) { alert('DEBE SELECCIONAR UN ARCHIVO PDF'); return }
  
  plWorking.value = true
  try {
    const formData = new FormData()
    formData.append('ID', 'TES1010g')
    formData.append('CLINEA', pcLinea.value)
    formData.append('CUNIACA', pcUniAca.value)
    formData.append('MTITULO', pcTitulo.value.toUpperCase())
    formData.append('ACODEST', JSON.stringify(paEgresados.value.map(x => x.CCODEST).filter(x => x != null && x !== '')))
    formData.append('file', poPDFFile.value)
    
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      body: formData
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

// 1.3 SELECCIONAR PDF
function f_SeleccionarPDF(event) {
  const file = event.target.files?.[0]
  if (!file) return
  
  // Validar que sea PDF
  if (file.type !== 'application/pdf') {
    alert('SOLO SE PERMITEN ARCHIVOS PDF')
    event.target.value = ''
    return
  }
  
  // Validar tamaño máximo (10MB)
  if (file.size > 10 * 1024 * 1024) {
    alert('EL ARCHIVO NO DEBE SUPERAR 10MB')
    event.target.value = ''
    return
  }
  
  pcNombrePDF.value = file.name
  poPDFFile.value = file
}

// 1.3 LIMPIAR PDF
function f_LimpiarPDF() {
  pcNombrePDF.value = ''
  poPDFFile.value = null
}

function f_Volver(screen) {
  pcScreen.value = screen
}

function f_Salir() {
  router.push('/mnu1001')
}
</script>

<style scoped>
@import url('/src/styles/Tes1010.css');
</style>

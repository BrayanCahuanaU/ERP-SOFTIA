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
@import url('/src/styles/Tes1010.css');
</style>

<template>
  <div>
    <LayoutBar pcTitulo="REGISTRAR PLAN DE TESIS"/>
    <div style="padding:20px; width:100%; box-sizing:border-box;">

      <!-- PANTALLA 1.1 - Selección de carrera -->
      <div v-if="pcScreen === '1'" style="width:50%; margin:0 auto;">
        <div style="margin-bottom:15px;">
          <label style="font-weight:bold; display:block; margin-bottom:8px;">SELECCIONE LA CARRERA:</label>
          <select v-model="pcCodest" style="width:100%; padding:8px; font-size:14px;">
            <option value="">-- SELECCIONE --</option>
            <option v-for="item in paDatos" :key="item.CCODEST" :value="item.CCODEST">
              {{ item.CNOMUNI }}
            </option>
          </select>
        </div>
        <div style="margin-top:20px; display:flex; gap:10px; justify-content:flex-end;">
          <Boton3D texto="APLICAR" color="azul" style="width:20%;" @click="f_Aplicar"/>
          <Boton3D texto="SALIR"   color="rojo" style="width:20%;" @click="f_Salir"/>
        </div>
      </div>

      <!-- PANTALLA 1.2 - Búsqueda de egresados -->
      <div v-if="pcScreen === '2'" style="width:60%; margin:0 auto;">
        <div style="margin-bottom:15px; padding:10px; background:#f2f2f2; border-radius:6px;">
          <span style="font-weight:bold;">CARRERA:</span> {{ pcNomUni }}
        </div>

        <!-- Lista de egresados agregados -->
        <div style="margin-bottom:15px;">
          <label style="font-weight:bold; display:block; margin-bottom:8px;">EGRESADOS:</label>
          <table border="1" style="width:100%; border-collapse:collapse; font-size:14px;">
            <thead>
              <tr style="background:#f2f2f2;">
                <th style="padding:6px;">#</th>
                <th style="padding:6px;">DNI</th>
                <th style="padding:6px; text-align:left;">NOMBRE</th>
                <th style="padding:6px;">CÓDIGO</th>
                <th style="padding:6px;">❌</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in paEgresados" :key="index">
                <td style="padding:6px; text-align:center;">{{ index + 1 }}</td>
                <td style="padding:6px; text-align:center;">{{ item.CNRODNI }}</td>
                <td style="padding:6px;">{{ item.CNOMBRE }}</td>
                <td style="padding:6px; text-align:center;">{{ item.CCODEST }}</td>
                <td style="padding:6px; text-align:center; cursor:pointer;" @click="f_EliminarEgresado(index)">❌</td>
              </tr>
              <tr v-if="!paEgresados.length">
                <td colspan="5" style="padding:10px; text-align:center;">NO HAY EGRESADOS AGREGADOS</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Buscar otro egresado -->
        <div v-if="paEgresados.length < 2" style="margin-bottom:15px; padding:10px; border:1px solid #ccc; border-radius:6px;">
          <label style="font-weight:bold; display:block; margin-bottom:8px;">BUSCAR EGRESADO POR DNI:</label>
          <div style="display:flex; gap:10px; align-items:center;">
            <input v-model="pcDniBuscar" maxlength="8" placeholder="Ingrese DNI"
              style="padding:8px; font-size:14px; width:200px;"
              @input="pcDniBuscar = pcDniBuscar.replace(/[^0-9A-Z]/g, '')"/>
            <Boton3D texto="BUSCAR" color="azul" style="width:20%;" @click="f_BuscarEgresado"/>
          </div>
          <div v-if="plLoadingBuscar" style="margin-top:10px; text-align:center;">
            <Spinner/>
          </div>
          <div v-if="poEgresadoBuscado && poEgresadoBuscado.CNRODNI" 
              style="margin-top:10px; padding:8px; background:#e8f5e9; border-radius:4px;
                      display:flex; justify-content:space-between; align-items:center;">
            <span>{{ poEgresadoBuscado.CNRODNI }} — {{ poEgresadoBuscado.CCODEST }} — {{ poEgresadoBuscado.CNOMBRE }}</span>
            <Boton3D texto="AGREGAR" color="azul" style="width:25%;" @click="f_AgregarEgresado"/>
          </div>
        </div>

        <div style="margin-top:20px; display:flex; gap:10px; justify-content:flex-end;">
          <Boton3D texto="CONTINUAR" color="azul" style="width:25%;" @click="f_Continuar"/>
          <Boton3D texto="VOLVER"    color="rojo" style="width:20%;" @click="f_Volver1"/>
        </div>
      </div>

      <!-- PANTALLA 1.3 - Grabar plan de tesis -->
      <div v-if="pcScreen === '3'" style="width:60%; margin:0 auto;">

        <!-- Datos del estudiante -->
        <div style="margin-bottom:10px; padding:10px; background:#f2f2f2; border-radius:6px;">
          <div><span style="font-weight:bold;">CARRERA:</span> {{ pcNomUni }}</div>
          <div style="margin-top:5px;">
            <span style="font-weight:bold;">EGRESADO(S):</span>
            <span v-for="(item, index) in paEgresados" :key="index">
              {{ item.CNOMBRE }}<span v-if="index < paEgresados.length - 1">, </span>
            </span>
          </div>
        </div>

        <!-- Línea -->
        <div style="margin-bottom:10px;">
          <label style="font-weight:bold; display:block; margin-bottom:5px;">LÍNEA:</label>
          <select v-model="pcLinea" style="width:100%; padding:8px; font-size:14px;">
            <option value="">-- SELECCIONE --</option>
            <option v-for="item in paLineas" :key="item.CLINEA" :value="item.CLINEA">
              {{ item.CLINEA }} - {{ item.CDESCRI }}
            </option>
          </select>
        </div>

        <!-- Título -->
        <div style="margin-bottom:10px;">
          <label style="font-weight:bold; display:block; margin-bottom:5px;">TÍTULO:</label>
          <textarea v-model="pcTitulo" rows="4"
            style="width:100%; padding:8px; font-size:14px; box-sizing:border-box; resize:vertical;">
          </textarea>
        </div>

        <!-- PDF -->
        <div style="margin-bottom:10px;">
          <label style="font-weight:bold; display:block; margin-bottom:5px;">PDF DEL PLAN DE TESIS:</label>
          <input type="file" accept=".pdf" @change="f_SeleccionarPDF"
            style="padding:6px; font-size:14px;"/>
          <div v-if="pcNombrePDF" style="margin-top:5px; color:green; font-size:13px;">
            ✅ {{ pcNombrePDF }}
          </div>
        </div>

        <div style="margin-top:20px; display:flex; gap:10px; justify-content:flex-end;">
          <Boton3D texto="GRABAR" color="azul" style="width:20%;" @click="f_Grabar"/>
          <Boton3D texto="VOLVER" color="rojo" style="width:20%;" @click="f_Volver2"/>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import LayoutBar from '@/components/LayoutBar.vue'
import Boton3D   from '@/components/Boton3D.vue'
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
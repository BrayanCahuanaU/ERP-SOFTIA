<template>
  <div class="tes-container">
    <!-- Header: Muestra logo, título y nombre del usuario autenticado -->
    <div class="tes-header">
      <span class="logo-mark">●</span>
      <span class="logo-text">ASIGNACIÓN DE DICTAMINADORES</span>
      
      <!-- Nombre de usuario obtenido de sessionStorage (del login) -->
      <div class="user-info">
        {{ getNombre }}
      </div>
    </div>

    <!-- Contenedor de pantallas: Alternancia entre screen 1 y 2 mediante v-if -->
    <div class="tes-content">

      <!-- PANTALLA 1 - Lista de tesis pendientes de asignación de dictaminadores -->
      <div v-if="pcScreen === '1'" class="screen screen-1">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">ASIGNAR DICTAMINADORES</h2>
            <p class="card-sub">Seleccione una tesis de la lista</p>
          </div>

          <!-- Banner: Muestra la unidad académica actual -->
          <div class="info-banner">
            <span class="info-banner-label">CARRERA</span>
            <!-- pcNomUni viene del backend en f_Init() -->
            <span class="info-banner-value">{{ pcNomUni }}</span>
          </div>

          <!-- Spinner mientras carga datos del servidor -->
          <div v-if="plLoading" style="text-align:center; padding:40px;">
            <Spinner/>
          </div>

          <!-- Lista de tesis: Cada elemento es clickeable y llama a f_Detalle() -->
          <div v-else class="section">
            <h3 class="section-title">TESIS DISPONIBLES</h3>
            <div class="tesis-list">
              <!-- Bucle: Itera sobre paTesis (Array de objetos tesis) -->
              <div 
                v-for="(item, index) in paTesis" 
                :key="index"
                class="tesis-card"
                @click="f_Detalle(item)"
              >
                <!-- Encabezado: ID y fecha de presentación -->
                <div class="tesis-header">
                  <span class="tesis-id">TESIS {{ item.CIDTESI }}</span>
                  <span class="tesis-fecha">{{ item.TPRESEN }}</span>
                </div>

                <!-- Cuerpo: Información de la tesis -->
                <div class="tesis-body">
                  <div class="tesis-egresado">
                    {{ item.CNOMEST }}{{ item.NFLAG > 1 ? ' (+' + (item.NFLAG - 1) + ')' : '' }}
                  </div>

                  <div class="tesis-titulo">
                    {{ item.MTITULO }}
                  </div>

                  <div class="tesis-linea">
                    {{ item.CDESLIN }}
                  </div>
                </div>

                <div class="tesis-footer">
                  <span class="tesis-action">VER DETALLE →</span>
                </div>
              </div>

              <div v-if="!paTesis.length" class="empty-row">
                NO SE ENCONTRARON REGISTROS
              </div>
            </div>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Salir">SALIR</button>
          </div>
        </div>
      </div>

      <!-- PANTALLA 2 - Asignar dictaminadores para una tesis específica -->
      <div v-if="pcScreen === '2'" class="screen screen-2">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">ASIGNAR DICTAMINADORES</h2>
            <p class="card-sub">Seleccione los docentes evaluadores</p>
          </div>

          <!-- Panel de información: Muestra detalles de la tesis seleccionada -->
          <div class="info-panel">
            <div class="info-item">
              <span class="info-label">ID TESIS</span>
              <span class="info-value">{{ poTesis.CIDTESI }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">LÍNEA</span>
              <span class="info-value">{{ poTesis.CDESLIN }}</span>
            </div>
            <div class="info-item info-item-full">
              <span class="info-label">EGRESADO</span>
              <span class="info-value">{{ poTesis.CNOMEST }}</span>
            </div>
            <div class="info-item info-item-full">
              <span class="info-label">TÍTULO</span>
              <span class="info-value" style="line-height:1.4;">{{ poTesis.MTITULO }}</span>
            </div>
          </div>

          <div v-if="plLoadingDict" style="text-align:center; padding:40px;">
            <Spinner/>
          </div>

          <div v-else class="section">
            <h3 class="section-title">DICTAMINADORES DISPONIBLES</h3>
            <div class="dict-list">
              <!-- Bucle: Itera sobre paDictaminadores (Array de docentes seleccionados por backend) -->
              <div 
                v-for="doc in paDictaminadores" 
                :key="doc.CCODDOC"
                class="dict-card"
              >
                <div class="dict-info">
                  <div class="dict-code">
                    {{ doc.CCODDOC }}
                  </div>
                  <div class="dict-name">
                    {{ doc.CNOMBRE }}
                  </div>
                </div>

                <!-- Badge informativo: Indica que será asignado -->
                <div class="dict-badge">
                  ASIGNADO
                </div>
              </div>

              <div v-if="!paDictaminadores.length" class="no-data">
                NO HAY DICTAMINADORES DISPONIBLES
              </div>
            </div>
          </div>

          <div class="button-group button-group-end">
            <button class="btn btn-secondary" @click="f_Volver">VOLVER</button>
            <!-- f_Asignar() valida, envía datos al backend (TES1020g) y actualiza DB -->
            <button class="btn btn-primary" @click="f_Asignar">ASIGNAR</button>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const pcScreen = ref('1')
const plLoading = ref(false)
const plLoadingDict = ref(false)
const plWorking = ref(false)
const pcNomUni = ref('')
const paTesis = ref([])
const poTesis = ref({})
const paDictaminadores = ref([])

// Obtener código de usuario desde sessionStorage (viene del login)
const pcCodUsu = sessionStorage.getItem('CCODUSU')

// Computed para obtener nombre de usuario desde sessionStorage
const getNombre = computed(() => {
  return sessionStorage.getItem('CNOMBRE')
})

// Actualizar nombre cuando el componente monta
onMounted(() => {
  pcNombre.value = getNombre.value
  f_Init()
})

async function f_Init() {
  try {
    plLoading.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1020i', CCODUSU: pcCodUsu })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    // Asignar valores dinámicos desde backend
    pcNomUni.value = laData.CNOMUNI
    paTesis.value  = laData.DATOS
  } catch (e) {
    alert('ERROR AL CARGAR TESIS')
  } finally {
    plLoading.value = false
  }
}

async function f_Detalle(item) {
  poTesis.value = item
  paDictaminadores.value = []
  pcScreen.value = '2'
  try {
    plLoadingDict.value = true
    // Llamada al backend para obtener dictaminadores disponibles
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1020c', CIDTESI: item.CIDTESI })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    paDictaminadores.value = laData
  } catch (e) {
    alert('ERROR AL CARGAR DICTAMINADORES')
  } finally {
    plLoadingDict.value = false
  }
}

async function f_Asignar() {
  if (plWorking.value || paDictaminadores.value.length < 2) return
  plWorking.value = true

  try {
    // Enviar datos al backend para grabar asignación
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ID: 'TES1020g',
        CIDTESI: poTesis.value.CIDTESI,
        CCODUSU: pcCodUsu,
        DATOS: paDictaminadores.value.map(x => ({ CCODDOC: x.CCODDOC }))
      })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
    alert('DICTAMINADORES ASIGNADOS CORRECTAMENTE')

    // Volver a pantalla 1 y recargar lista de tesis
    f_Volver()
    f_Init()

  } catch (e) {
    alert('ERROR AL ASIGNAR')
  } finally {
    plWorking.value = false
  }
}

function f_Volver() {
  pcScreen.value = '1'
  poTesis.value = {}
  paDictaminadores.value = []
}

function f_Salir() {
  router.push('/mnu1001')
}
</script>

<style scoped>
@import url('/src/styles/Tes1200.css');
</style>

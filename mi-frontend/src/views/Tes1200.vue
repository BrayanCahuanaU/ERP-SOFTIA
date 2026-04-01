<template>
  <div class="tes-container">
    <!-- Header -->
    <div class="tes-header">
      <span class="logo-mark">●</span>
      <span class="logo-text">ASIGNACIÓN DE DICTAMINADORES</span>
      
      <div class="user-info">
        {{ pcNombre }}
      </div>
    </div>

    <!-- Main content -->
    <div class="tes-content">

      <!-- PANTALLA 1 - Lista de tesis -->
      <div v-if="pcScreen === '1'" class="screen screen-1">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">ASIGNAR DICTAMINADORES</h2>
            <p class="card-sub">Seleccione una tesis de la lista</p>
          </div>

          <!-- Carrera -->
          <div class="info-banner">
            <span class="info-banner-label">CARRERA</span>
            <span class="info-banner-value">{{ pcNomUni }}</span>
          </div>
          <div v-if="plLoading" style="text-align:center; padding:40px;">
            <Spinner/>
          </div>

          <div v-else class="section">
            <h3 class="section-title">TESIS DISPONIBLES</h3>
            <div class="tesis-list">
              <div 
                v-for="(item, index) in paTesis" 
                :key="index"
                class="tesis-card"
                @click="f_Detalle(item)"
              >
                <div class="tesis-header">
                  <span class="tesis-id">TESIS {{ item.CIDTESI }}</span>
                  <span class="tesis-fecha">{{ item.TPRESEN }}</span>
                </div>

                <div class="tesis-body">
                  <div class="tesis-egresado">
                    {{ item.CNOMEST }}{{ item.NFLAG > 1 ? ' (+1)' : '' }}
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

      <!-- PANTALLA 2 - Asignar dictaminadores -->
      <div v-if="pcScreen === '2'" class="screen screen-2">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">ASIGNAR DICTAMINADORES</h2>
            <p class="card-sub">Seleccione los docentes evaluadores</p>
          </div>

          <!-- Datos de la tesis -->
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router          = useRouter()
const pcScreen        = ref('1')
const plLoading       = ref(false)
const plLoadingDict   = ref(false)
const plWorking       = ref(false)
const pcNomUni        = ref('')
const paTesis         = ref([])
const poTesis         = ref({})
const paDictaminadores = ref([])
const paSeleccionados  = ref([])

// Código de usuario simulado — cuando haya login vendrá del sessionStorage
const pcCodUsu = sessionStorage.getItem('CCODUSU') || '1221'

onMounted(() => {
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
    pcNomUni.value = laData.CNOMUNI
    paTesis.value  = laData.DATOS
  } catch (e) {
    alert('ERROR AL CARGAR TESIS')
  } finally {
    plLoading.value = false
  }
}

async function f_Detalle(item) {
  poTesis.value         = item
  paSeleccionados.value = []
  paDictaminadores.value = []
  pcScreen.value        = '2'
  try {
    plLoadingDict.value = true
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
  if (plWorking.value) return

  if (paDictaminadores.value.length < 2) {
    alert('NO HAY DICTAMINADORES SUFICIENTES')
    return
  }

  plWorking.value = true

  try {
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ID:      'TES1020g',
        CIDTESI: poTesis.value.CIDTESI,
        CCODUSU: pcCodUsu,
        DATOS:   paDictaminadores.value.map(x => ({
          CCODDOC: x.CCODDOC
        }))
      })
    })

    const laData = await loRpta.json()

    if (laData.ERROR) {
      alert(laData.ERROR)
      return
    }

    alert('DICTAMINADORES ASIGNADOS CORRECTAMENTE')

    f_Volver()
    f_Init()

  } catch (e) {
    alert('ERROR AL ASIGNAR')
  } finally {
    plWorking.value = false
  }
}

function f_Volver() {
  pcScreen.value         = '1'
  poTesis.value          = {}
  paSeleccionados.value  = []
  paDictaminadores.value = []
}

function f_Salir() {
  router.push('/mnu1001')
}
</script>

<style scoped>
@import url('/src/styles/Tes1200.css');
</style>

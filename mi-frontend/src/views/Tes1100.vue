<template>
  <div class="tes-container">
    <!-- Header -->
    <div class="tes-header">
      <span class="logo-mark">●</span>
      <span class="logo-text">MIS TESIS REGISTRADAS</span>
    </div>

    <!-- Main content -->
    <div class="tes-content">
      <div class="screen screen-1">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">MIS TESIS REGISTRADAS</h2>
            <p class="card-sub">Lista de planes de tesis que has registrado</p>
          </div>

          <!-- Loading -->
          <div v-if="plLoading" style="text-align:center; padding:40px;">
            <Spinner/>
          </div>

          <!-- Lista de tesis -->
          <div v-else-if="paDatos.length > 0" class="tesis-list">
            <div v-for="item in paDatos" :key="item.CIDTESI" class="tesis-card">
              <div class="tesis-header">
                <div class="tesis-id">ID: {{ item.CIDTESI }}</div>
                <div class="tesis-carrera">{{ item.CNOMUNI }}</div>
              </div>

              <div class="tesis-body">
                <div class="tesis-field">
                  <span class="tesis-label">LÍNEA DE INVESTIGACIÓN:</span>
                  <span class="tesis-value">{{ item.CLINEA }} - {{ item.CDESCRI }}</span>
                </div>
                
                <div class="tesis-field">
                  <span class="tesis-label">TÍTULO:</span>
                  <span class="tesis-value">{{ item.MTITULO }}</span>
                </div>
              </div>

              <div class="tesis-actions">
                <button class="btn btn-secondary" @click="f_DescargarPDF(item.CIDTESI)">
                  📥 DESCARGAR PDF
                </button>
              </div>
            </div>
          </div>

          <!-- Sin tesis -->
          <div v-else class="empty-state">
            <div class="empty-icon">📋</div>
            <div class="empty-text">NO TIENES TESIS REGISTRADAS AÚN</div>
            <div class="empty-sub">Regístrate en el plan de tesis para comenzar</div>
          </div>

          <!-- Botones de acción -->
          <div class="button-group button-group-end" style="margin-top:30px;">
            <button class="btn btn-secondary" @click="f_Volver">VOLVER</button>
            <button class="btn btn-primary" @click="f_RegistrarTesis">+ REGISTRAR NUEVA TESIS</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Spinner from '@/components/Spinner.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const plLoading = ref(false)
const paDatos = ref([])

// Datos del login
const pcCodEst = sessionStorage.getItem('CCODEST') || sessionStorage.getItem('CCODUSU') || ''

onMounted(async () => {
  if (!pcCodEst) {
    alert('DATOS DE SESIÓN INVÁLIDOS. POR FAVOR INICIE SESIÓN')
    return
  }
  try {
    plLoading.value = true
    const loRpta = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ID: 'TES1100i', CCODEST: pcCodEst })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) {
      alert(laData.ERROR)
      return
    }
    paDatos.value = laData.DATOS || []
  } catch (e) {
    console.error('Error al cargar tesis:', e)
    alert(`ERROR AL CARGAR TESIS: ${e.message}`)
  } finally {
    plLoading.value = false
  }
})

// Descargar PDF
function f_DescargarPDF(pcIdTesi) {
  const enlace = document.createElement('a')
  enlace.href = `http://localhost:8000/descargar/T${pcIdTesi}.pdf`
  enlace.target = '_blank'
  enlace.download = `Tesis_${pcIdTesi}.pdf`
  enlace.click()
}

// Registrar nueva tesis
function f_RegistrarTesis() {
  router.push('/tes1010')
}

// Volver
function f_Volver() {
  router.push('/mnu1001')
}
</script>

<style scoped>
@import url('/src/styles/Tes1100.css');
</style>

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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Root ──────────────────────────────────────────────────── */
.tes-header {
  display: flex;
  align-items: center;
  justify-content: space-between; 
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
  width: 20px;
  height: 20px;
  border-radius: 20%;
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
  max-width: 900px;
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

/* ── Info Banner ───────────────────────────────────────────── */
.info-banner {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #ffffff;
  padding: 16px 18px;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.info-banner-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.85;
}

.info-banner-value {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.05em;
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

/* ── Table ─────────────────────────────────────────────────── */
.table-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  max-height: 500px;
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
  padding: 20px 20px;
  margin-bottom: 28px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-item-full {
  grid-column: 1 / -1;
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

/* ── Checkboxes ────────────────────────────────────────────── */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.checkbox-item input[type="checkbox"] {
  margin-top: 2px;
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #2563eb;
}

.checkbox-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
  cursor: pointer;
  flex: 1;
}

.checkbox-code {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.checkbox-name {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.no-data {
  padding: 20px;
  text-align: center;
  color: #94a3b8;
  font-weight: 500;
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
@media (max-width: 768px) {
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

  .screen {
    max-width: 100%;
  }

  .button-group {
    flex-direction: column-reverse;
  }

  .table-wrapper {
    max-height: 400px;
  }
}

.dict-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dict-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 14px 16px;
}

.dict-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dict-code {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
}

.dict-name {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.dict-badge {
  font-size: 11px;
  font-weight: 700;
  background: #16a34a;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.tesis-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.tesis-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.tesis-card:hover {
  border-color: #2563eb;
  background: #f8fafc;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.15);
}

.tesis-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.tesis-id {
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
}

.tesis-fecha {
  font-size: 12px;
  color: #64748b;
}

.tesis-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tesis-egresado {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
}

.tesis-titulo {
  font-size: 14px;
  font-weight: 500;
  color: #0f172a;
  line-height: 1.3;
}

.tesis-linea {
  font-size: 12px;
  color: #64748b;
}

.tesis-footer {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

.tesis-action {
  font-size: 11px;
  font-weight: 700;
  color: #2563eb;
  letter-spacing: 0.05em;
}
</style>
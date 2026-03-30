<template>
  <div>
    <LayoutBar pcTitulo="ASIGNACIÓN DE DICTAMINADORES"/>
    <div style="padding:20px; width:100%; box-sizing:border-box;">

      <!-- PANTALLA 1 - Lista de tesis -->
      <div v-if="pcScreen === '1'">
        <div v-if="plLoading" style="text-align:center; margin-top:20px;">
          <Spinner/>
        </div>
        <div v-else style="width:90%; margin:0 auto;">
          <!-- Unidad académica -->
          <div style="margin-bottom:10px; padding:10px; background:#010B6F; color:white;
                      font-weight:bold; border-radius:6px;">
            {{ pcNomUni }}
          </div>
          <div style="width:100%; max-height:400px; overflow-y:auto; border:1px solid #ccc;">
            <table border="1" style="width:100%; border-collapse:collapse; font-size:14px;">
              <thead>
                <tr style="background:#f2f2f2;">
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">#</th>
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">ID</th>
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">FECHA</th>
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:left;">EGRESADO</th>
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:left;">TÍTULO</th>
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:left;">LÍNEA</th>
                  <th style="padding:6px; position:sticky; top:0; background:#f2f2f2; text-align:center;">🔎</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in paTesis" :key="index">
                  <td style="padding:6px; text-align:center;">{{ index + 1 }}</td>
                  <td style="padding:6px; text-align:center;">{{ item.CIDTESI }}</td>
                  <td style="padding:6px; text-align:center;">{{ item.TPRESEN }}</td>
                  <td style="padding:6px;">{{ item.CNOMEST }}{{ item.NFLAG > 1 ? ' (+1)' : '' }}</td>
                  <td style="padding:6px;">{{ item.MTITULO }}</td>
                  <td style="padding:6px;">{{ item.CDESLIN }}</td>
                  <td style="padding:6px; text-align:center; cursor:pointer;" @click="f_Detalle(item)">🔎</td>
                </tr>
                <tr v-if="!paTesis.length">
                  <td colspan="7" style="padding:10px; text-align:center;">NO SE ENCONTRARON REGISTROS</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style="margin-top:15px; text-align:right;">
            <Boton3D texto="SALIR" color="rojo" style="width:10%;" @click="f_Salir"/>
          </div>
        </div>
      </div>

      <!-- PANTALLA 2 - Asignar dictaminadores -->
      <div v-if="pcScreen === '2'" style="width:60%; margin:0 auto;">
        <!-- Datos de la tesis -->
        <div style="margin-bottom:15px; padding:10px; background:#f2f2f2; border-radius:6px;">
          <div><span style="font-weight:bold;">ID TESIS:</span> {{ poTesis.CIDTESI }}</div>
          <div><span style="font-weight:bold;">LÍNEA:</span> {{ poTesis.CDESLIN }}</div>
          <div><span style="font-weight:bold;">TÍTULO:</span> {{ poTesis.MTITULO }}</div>
          <div><span style="font-weight:bold;">EGRESADO:</span> {{ poTesis.CNOMEST }}</div>
        </div>

        <div v-if="plLoadingDict" style="text-align:center; margin-top:20px;">
          <Spinner/>
        </div>
        <div v-else>
          <label style="font-weight:bold; display:block; margin-bottom:8px;">DICTAMINADORES DISPONIBLES:</label>
          <div v-for="doc in paDictaminadores" :key="doc.CCODDOC"
               style="display:flex; align-items:center; margin-bottom:8px;">
            <input type="checkbox" :value="doc" v-model="paSeleccionados"
                   style="margin-right:10px; width:16px; height:16px;">
            <span>{{ doc.CCODDOC }} - {{ doc.CNOMBRE }}</span>
          </div>
          <div v-if="!paDictaminadores.length" style="color:red;">
            NO HAY DICTAMINADORES DISPONIBLES
          </div>
        </div>

        <div style="margin-top:20px; display:flex; gap:10px; justify-content:flex-end;">
          <Boton3D texto="ASIGNAR" color="azul" style="width:20%;" @click="f_Asignar"/>
          <Boton3D texto="VOLVER"  color="rojo" style="width:20%;" @click="f_Volver"/>
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
  if (paSeleccionados.value.length === 0) {
    alert('DEBE SELECCIONAR AL MENOS UN DICTAMINADOR')
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
        DATOS:   paSeleccionados.value.map(x => ({ CCODDOC: x.CCODDOC }))
      })
    })
    const laData = await loRpta.json()
    if (laData.ERROR) { alert(laData.ERROR); return }
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
<template>
   <div>
      <LayoutBar pcTitulo="MANTENIMIENTO EQUIPOS LABORATORIO"/>
      <div class="dhb-main-container">
         <div v-if="pcScreen === '1'">
            <div class="dhb-list-wrapper">
               <div class="dhb-list-header">
               <div class="dhb-period-group">
                  <label class="dhb-period-label">PERIODO:</label>
                  <input v-model="pcPeriod" maxlength="4" inputmode="numeric" autofocus @input="pcPeriod = pcPeriod.replace(/[^0-9]/g,'')" class="dhb-period-input">
               </div>
               </div>
               <div class="dhb-list-content">
                  <div v-if="plLoading" class="dhb-loading">
                     <Spinner />
                  </div>
                  <div v-if="!plLoading && paDatos" class="dhb-table-wrapper">
                     <table class="dhb-table">
                        <thead>
                           <tr>
                           <th>#</th>
                           <th>ID</th>
                           <th class="text-left">LABORATORIO</th>
                           <th>🔎</th>
                           </tr>
                        </thead>
                        <tbody>
                           <tr v-for="(laItem, index) in paDatos" :key="index">
                              <td>{{index + 1}}</td>
                              <td>{{laItem.ID}}</td>
                              <td class="text-left">{{laItem.CEQUIPO}}</td>
                              <td class="icon-cell" @click="f_Detalle(laItem.CEQUIPO)" title="Ver detalle">🔎</td>
                           </tr>
                           <tr v-if="!paDatos.length">
                              <td colspan="4" class="dhb-table-empty">
                                 NO SE ENCONTRARON REGISTROS
                              </td>
                           </tr>
                        </tbody>
                     </table>
                  </div>
                  <!-- Botón Salir -->
                  <div class="dhb-button-group">
                     <Boton3D color="rojo" texto="SALIR" @click="f_Salir"></Boton3D>
                  </div>
               </div>
            </div>
         </div>
         <div v-if="pcScreen === '2'">
            <div class="dhb-detail-header">
               EQUIPO: {{pcIdEqui}} - {{pcEquipo}}
            </div>
            <div v-if="plLoading" class="dhb-loading">
               <Spinner />
            </div>
            <div v-if="!plLoading && paData" class="dhb-detail-table-wrapper">
               <table class="dhb-detail-table">
                  <thead>
                     <tr>
                     <th>#</th>
                     <th>ID</th>
                     <th>LABORATORIO</th>
                     <th>FECHA</th>
                     <th class="text-left">MANTENIMIENTO</th>
                     <th>TÉCNICO</th>
                     <th class="text-left">ESTADO</th>
                     </tr>
                  </thead>
                  <tbody>
                     <tr v-for="(laItem, index) in paData.DATOS" :key="index">
                        <td>{{index + 1}}</td>
                        <td>{{laItem.ID}}</td>
                        <td>{{laItem.CLABORA}}</td>
                        <td>{{laItem.DFECHA}}</td>
                        <td class="text-left">{{laItem.CTIPMTO}}</td>
                        <td>{{laItem.CTECNIC}}</td>
                        <td class="text-left">{{laItem.CESTADO}}</td>
                     </tr>
                     <!-- Si no hay resultados -->
                     <tr v-if="!paData?.DATOS?.length">
                        <td colspan="7" class="dhb-table-empty">
                           NO SE ENCONTRARON REGISTROS
                        </td>
                     </tr>
                  </tbody>
               </table>
            </div>
            <!-- Botón Regresar -->
            <div class="dhb-button-group">
               <Boton3D color="rojo" texto="REGRESAR" @click="f_Regresar"></Boton3D>
            </div>
         </div>
         <div v-if="pcScreen === '3'" class="dhb-image-screen">
            <div class="dhb-image-container">
            <div class="dhb-image-wrapper">
               <img v-if="poImage.imageUrl" :src="poImage.imageUrl"/>
            </div>
            </div>
            <div class="dhb-image-sidebar">
               <Boton3D color="rojo" texto="VOLVER" @click="f_Volver"></Boton3D>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup>
   import LayoutBar from '@/components/LayoutBar.vue'
   import Boton3D from '@/components/Boton3D.vue'
   import Spinner from '@/components/Spinner.vue'
   import {f_Format} from '@/utils/utils'
   import {ref, computed, onMounted} from 'vue'
   import {useRouter} from 'vue-router'

   const plLoading = ref(false)
   const poRouter  = useRouter()
   const paDatos   = ref([])
   const paData    = ref()
   const pcScreen  = ref("1")
   const plError   = ref(false)
   const pcPeriod  = ref('')
   const pcEquipo  = ref('')
   const pcIdEqui  = ref('')
   const poImage   = ref({imageUrl: null});
   const plWorking = ref(false)

   // Init
   onMounted(() => {
      //pcPeriod.value = new Date().getFullYear().toString();
      pcPeriod.value = '2025';
      f_Init();
   })

   async function f_Init() {
      try {
         plLoading.value = true;
         // SIMULADO - reemplazar cuando FastAPI esté listo
         await new Promise(r => setTimeout(r, 800)); // simula delay
         paDatos.value = [
            { ID: 1, CEQUIPO: 'COMPUTADORA' },
            { ID: 2, CEQUIPO: 'PROYECTOR' },
            { ID: 3, CEQUIPO: 'IMPRESORA' }
         ];
      } catch (error) {
         console.error("Error cargando datos:", error);
         alert("ERROR AL CARGAR DATOS");
      } finally {
         plLoading.value = false;
      }
   }

   async function f_Detalle(p_cEquipo) {
      try {
         plLoading.value = true;
         // SIMULADO - reemplazar cuando FastAPI esté listo
         await new Promise(r => setTimeout(r, 800));
         paData.value = {
            ID: 1,
            CEQUIPO: p_cEquipo,
            DATOS: [
            { ID: 1, CLABORA: 'LAB-01', DFECHA: '2025-03-01', CTIPMTO: 'PREVENTIVO', CTECNIC: 'JUAN PÉREZ', CESTADO: 'COMPLETADO' },
            { ID: 2, CLABORA: 'LAB-02', DFECHA: '2025-06-15', CTIPMTO: 'CORRECTIVO', CTECNIC: 'MARÍA LÓPEZ', CESTADO: 'PENDIENTE' }
            ]
         };
         pcIdEqui.value = paData.value.ID;
         pcEquipo.value = paData.value.CEQUIPO;
         pcScreen.value = '2';
      } catch (error) {
         console.error("Error cargando datos:", error);
         alert("ERROR AL CARGAR DATOS");
      } finally {
         plLoading.value = false;
      }
   }

   async function f_Grafico() {
      if (plWorking.value) return;
      plWorking.value = true
      console.log("CLICK", performance.now())
      try {
         plLoading.value = true;
         const loRpta = await fetch('http://localhost:8000/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ID: 'DHB0007', NSERIAL: pnSerial.value})
         })
         if (!loRpta.ok) {
            throw new Error('Error en la respuesta del servidor');
         }
         const blob = await loRpta.blob();
         //console.log("Blob size:", blob.size);
         //console.log("Blob type:", blob.type);
         const url = URL.createObjectURL(blob);
         poImage.value = {imageUrl: url};
         pcScreen.value = '3';
      } catch (error) {
         console.error("Error cargando datos:", error);
         alert(error);
      } finally {
         plLoading.value = false;
         plWorking.value = false
      }
   }

   function f_Regresar() {
      pcScreen.value = "1";
      paData.value   = null;
   }

   function f_Volver() {
      pcScreen.value = "2";
   }

   function f_Salir() {
      poRouter.push('/mnu1001');
   }
</script>

<style scoped>
@import url('/src/styles/Dhb1140.css');
</style>

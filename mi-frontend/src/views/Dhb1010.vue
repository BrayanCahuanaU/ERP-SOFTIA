<template>
   <div>
      <LayoutBar pcTitulo="COBRANZAS TASAS EDUCATIVAS"/>
      <br>
      <label style="margin-left:20px; font-family:Arial; font-size:14px;">
         <span style="font-weight:bold;">ID:</span>
         {{paData.CIDDATO}} - {{paData.CDESCRI}}
      </label>
      <div style="width:100%; padding:20px; box-sizing:border-box;">
         <div style="max-height:400px; overflow-y:auto; border:1px solid #ccc;">
            <table style="width:100%; border-collapse:collapse; font-family:Arial; font-size:14px;">
               <thead>
                  <tr>
                  <th style="background:#cce; color:#002060; padding:8px; border:1px solid #ccc; text-align:center; position:sticky; top:0; z-index:1;">FECHA</th>
                  <th style="background:#cce; color:#002060; padding:8px; border:1px solid #ccc; text-align:right; position:sticky; top:0; z-index:1;">EMITIDO</th>
                  <th style="background:#cce; color:#002060; padding:8px; border:1px solid #ccc; text-align:right; position:sticky; top:0; z-index:1;">PAGADO</th>
                  <th style="background:#cce; color:#002060; padding:8px; border:1px solid #ccc; text-align:right; position:sticky; top:0; z-index:1;">INCREMENTO</th>
                  <th style="background:#cce; color:#002060; padding:8px; border:1px solid #ccc; text-align:right; position:sticky; top:0; z-index:1;">CANT.</th>
                  <th style="background:#cce; color:#002060; padding:8px; border:1px solid #ccc; text-align:right; position:sticky; top:0; z-index:1;">% VENC.</th>
                  </tr>
               </thead>
               <tbody>
                  <tr v-for="(laItem, index) in paData.DATOS" :key="index" style="transition:background 0.2s; cursor:pointer;" @mouseover="filaHover=index" @mouseleave="filaHover=null" :style="{background: filaHover===index ? '#f0f8ff' : 'transparent'}">
                     <td style="padding:8px; border:1px solid #ddd; text-align:center;">{{laItem.DFECHA}}</td>
                     <td style="padding:8px; border:1px solid #ddd; text-align:right;">{{f_Format(laItem.NEMITID, 2)}}</td>
                     <td style="padding:8px; border:1px solid #ddd; text-align:right;">{{f_Format(laItem.NPAGADO, 2)}}</td>
                     <td style="padding:8px; border:1px solid #ddd; text-align:right;">{{f_Format(laItem.NINCREM, 2)}}</td>
                     <td style="padding:8px; border:1px solid #ddd; text-align:right;">{{f_Format(laItem.NCANALU, 0)}}</td>
                     <td style="padding:8px; border:1px solid #ddd; text-align:right;">{{f_Format(laItem.NPORVEN, 2)}}</td>
                  </tr>
                  <tr v-if="paData.length === 0">
                     <td colspan="6" style="padding:8px; text-align:center; color:#888;">Cargando datos...</td>
                  </tr>
               </tbody>
            </table>
         </div>
         <!--<div style="margin-top:20px; display:flex; justify-content:flex-end;">-->
         <div style="width:100%; display:flex; justify-content:flex-end; gap:10px;">
            <Boton3D color="azul" texto="GRAFICAR" style="width:10%;" @click="f_CargarGrafico"></Boton3D>
            <Boton3D color="rojo" texto="SALIR" style="width:10%;" @click="volver"></Boton3D>
         </div>
      </div>
   </div>
   <div v-if="plModal" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); display:flex; justify-content:center; align-items:center; z-index:999;">
      <div style="width:80%; height:80%; background:white; padding:20px; border-radius:8px; box-sizing:border-box; display:flex; flex-direction:column;">
         <div style="display:flex; justify-content:flex-end;">
            <Boton3D color="rojo" texto="CERRAR" style="width:120px;" @click="plModal=false"></Boton3D>
         </div>
         <div style="flex:1; margin-top:10px;">
            <canvas ref="graficoRef"></canvas>
         </div>
      </div>
   </div>
</template>

<script setup>
   import LayoutBar from '@/components/LayoutBar.vue'
   import Boton3D from '@/components/Boton3D.vue'
   import {ref, onMounted, nextTick} from 'vue'
   import {useRouter} from 'vue-router'
   import {f_Format} from '@/utils/utils'
   import {Chart} from 'chart.js/auto'

   const plModal   = ref(false)
   const loRouter  = useRouter()
   const paData    = ref([])
   //const filaHover = ref(null)

   function f_Volver() {
      loRouter.push('/mnu1001');
   }

   // Cargar datos desde API POST con JSON (recibidos tal cual)
   async function f_CallApi() {
      try {
         let laParam = { ID: "Dhb1010c", CIDDATO: "0A6" }
         let loRespon = await fetch('http://localhost:3000/', {method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(laParam)})
         if (!loRespon.ok) throw new Error('Error al cargar datos')
         const laData = await loRespon.json()
         paData.value = laData   
      } catch (err) {
         console.error("API Error:", err)
         paData.value = []
      }
   }

   const graficoRef = ref(null)
   let loGraph = null

   async function f_CargarGrafico() {
      // Mostrar modal
      plModal.value = true;
      await nextTick();
      // Destruir gráfico anterior si existe
      if (loGraph) {
         loGraph.destroy();
      }
      // Datos invertidos (más reciente primero)
      let laDatos = paData.value.DATOS;
      const labels = [...laDatos].map(f => f.DFECHA).reverse();
      const emitido = [...laDatos].map(f => Number(f.NEMITID)).reverse();
      const pagado = [...laDatos].map(f => Number(f.NPAGADO)).reverse()
      // Crear gráfico
      loGraph = new Chart(graficoRef.value, 
         {type: 'line', 
            data: {labels, datasets: [{label: 'Emitido', data: emitido, borderWidth: 3, tension: 0.3, pointRadius: 4, pointHoverRadius: 6},
                                      {label: 'Pagado', data: pagado, borderWidth: 3, tension: 0.3, pointRadius: 4, pointHoverRadius: 6}]},
            options: {responsive: true, maintainAspectRatio: false,
                      plugins: {title: {display: true, text: 'Cobranza de Tasas Educativas', color: '#000',
                                        font: {size: 18, weight: 'bold'}, padding: {top: 10, bottom: 20}},
                                legend: {labels: {color: '#000', font: {size: 14, weight: 'bold'}}},
                                tooltip: {callbacks: {label: function(context) { return context.dataset.label + ': ' +
                                                      Number(context.raw).toLocaleString('es-PE', {
                                                         minimumFractionDigits: 2,
                                                         maximumFractionDigits: 2})}}}
                               },
                      scales: {x: {ticks: {color: '#000', font: {size: 12, weight: 'bold'}}, grid: {color: '#ccc'}},
                               y: {ticks: {color: '#000', font: {size: 12, weight: 'bold'}, 
                                   callback: function(value) {
                                                return Number(value).toLocaleString('es-PE', {
                                                   minimumFractionDigits: 0, maximumFractionDigits: 0
                                                })
                                             }
                                          },
                                    grid: {color: '#ccc'}
                                  }
                              }
                     }
      })
   }
   // Montaje inicial
   onMounted(() => f_CallApi())
</script>

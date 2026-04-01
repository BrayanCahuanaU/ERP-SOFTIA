<template>
  <div class="not-found-container">
    <!-- Header bar -->
    <div class="header-bar">
      <span class="logo-mark">●</span>
      <span class="logo-text">SISTEMA ERP — TESIS</span>
    </div>

    <!-- Main content -->
    <div class="content-wrapper">
      <div class="error-card">
        <div class="error-code">404</div>
        <div class="error-title">PÁGINA NO ENCONTRADA</div>
        <p class="error-message">
          La página que intentas acceder no existe o ha sido movida.
        </p>
        <div class="error-icon">⚠️</div>
        <button @click="goBack" class="btn-volver">
          <span class="btn-icon">←</span> VOLVER AL INICIO
        </button>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer-bar">UCSM · Sistema de Gestión de Tesis · {{ new Date().getFullYear() }}</div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goBack() {
  const userType = sessionStorage.getItem('USER_TYPE')
  if (userType) {
    router.push('/mnu1001')
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
@import url('/src/styles/NotFound.css');
</style>

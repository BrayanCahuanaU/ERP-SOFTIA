<template>
  <div class="access-denied-container">
    <!-- Header bar -->
    <div class="header-bar">
      <span class="logo-mark">●</span>
      <span class="logo-text">SISTEMA ERP — TESIS</span>
    </div>

    <!-- Main content -->
    <div class="content-wrapper">
      <div class="error-card">
        <div class="error-code">403</div>
        <div class="error-title">ACCESO DENEGADO</div>
        <p class="error-message">
          No tienes permiso para acceder a esta página.<br>Por favor, inicia sesión o solicita acceso.
        </p>
        <div class="error-icon">🔒</div>
        <div class="button-group">
          <button @click="goToLogin" class="btn-login">
            <span class="btn-icon">→</span> IR A LOGIN
          </button>
          <button @click="goBack" class="btn-atras">
            <span class="btn-icon">←</span> ATRÁS
          </button>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer-bar">UCSM · Sistema de Gestión de Tesis · {{ new Date().getFullYear() }}</div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToLogin() {
  sessionStorage.clear()
  router.push('/login')
}

function goBack() {
  router.back()
}
</script>

<style scoped>
@import url('/src/styles/AccessDenied.css');
</style>

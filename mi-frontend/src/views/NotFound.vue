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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

.not-found-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f0f4f8;
  font-family: 'DM Sans', sans-serif;
}

.header-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.logo-mark {
  font-size: 10px;
  color: #2563eb;
}

.logo-text {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #2563eb;
  text-transform: uppercase;
}

.content-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.error-card {
  background: white;
  border-radius: 8px;
  padding: 50px 40px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  max-width: 500px;
  border: 1px solid #e2e8f0;
}

.error-code {
  font-size: 100px;
  font-weight: 700;
  color: #2563eb;
  line-height: 1;
  margin-bottom: 20px;
  letter-spacing: 0.1em;
}

.error-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.error-message {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
  line-height: 1.6;
  font-weight: 400;
}

.error-icon {
  font-size: 60px;
  margin: 20px 0 28px;
  opacity: 0.8;
}

.btn-volver {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
}

.btn-volver:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.btn-volver:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 14px;
  line-height: 1;
}

.footer-bar {
  margin-top: auto;
  padding: 16px 32px;
  font-size: 12.5px;
  color: #94a3b8;
  letter-spacing: 0.06em;
  text-align: center;
  border-top: 1px solid #e2e8f0;
  background: #ffffff;
}

@media (max-width: 640px) {
  .header-bar,
  .footer-bar {
    padding: 12px 20px;
  }

  .error-card {
    padding: 40px 24px;
  }

  .error-code {
    font-size: 80px;
  }

  .error-title {
    font-size: 20px;
  }
}
</style>

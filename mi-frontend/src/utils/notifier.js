import Swal from 'sweetalert2';

// Configuramos un estilo base para que todos se vean iguales
const Toast = Swal.mixin({
  background: '#1e1e1e',
  color: '#fff',
  confirmButtonColor: '#646cff',
  customClass: {
    popup: 'border-radius-10'
  }
});

export const notify = {
  // Para advertencias (como "Seleccione carrera")
  warn(msg) {
    Toast.fire({
      title: 'Atención',
      text: msg,
      icon: 'warning'
    });
  },
  // Para errores (como los de Postgres o Tesis pendiente)
  error(msg) {
    Toast.fire({
      title: 'Error del Sistema',
      text: msg,
      icon: 'error'
    });
  },
  // Para éxitos
  success(msg) {
    Toast.fire({
      title: '¡Logrado!',
      text: msg,
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });
  }
};
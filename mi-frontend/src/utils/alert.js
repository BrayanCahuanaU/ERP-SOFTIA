import Swal from 'sweetalert2';

// Esta función procesará cualquier objeto que venga de tu Python
export const manejarRespuesta = (res) => {
  // Si plOk es false, significa que Python llenó un pcError
  if (res.plOk === false || (res.pcError && res.pcError !== 'none')) {
    Swal.fire({
      title: 'Validación del Sistema',
      text: res.pcError, // Aquí entrará CUALQUIERA de tus mensajes de Python
      icon: 'warning',
      background: '#1e1e1e',
      color: '#fff',
      confirmButtonColor: '#646cff',
      confirmButtonText: 'Entendido'
    });
    return false; // Indica que hubo un error
  }
  
  return true; // Indica que todo está bien
};
// Espera a que todo el HTML esté cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {

  // 1. SELECCIONAR ELEMENTOS
  const form = document.getElementById('register-form');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  if (!form || !emailInput || !passwordInput) {
    console.warn('validaciones_login: elementos esperados (register-form, email, password) no encontrados en DOM.');
    return;
  }
  
  // Nuevo: referencias para validación de contraseña fuerte
  const password= passwordInput;
  const errorPassword = document.getElementById('error-password');

  // Lista de todos los campos que queremos validar
  const camposAValidar = [emailInput, passwordInput];

  // --- FUNCIÓN PRINCIPAL DE VALIDACIÓN ---
  // Esta función comprueba un solo campo y muestra u oculta su error
  function validarCampo(input) {
    const errorElement = document.getElementById('error-' + input.id);
    const validity = input.validity; // El objeto de validez del campo

    // Reseteamos cualquier error personalizado anterior
    input.setCustomValidity('');

    // Si el campo NO es válido...
    if (!validity.valid) {
      let mensajeError = ''; // Aquí guardaremos el mensaje de error

      // --- Manejar errores personalizados (customError) ---
      if (validity.customError) {
        // Usamos el mensaje que se haya seteado con setCustomValidity
        mensajeError = input.validationMessage || 'El valor ingresado es incorrecto.';
      }
      // --- Asignación de mensajes personalizados ---
      // Puedes añadir todos los 'else if' que necesites
      else if (validity.valueMissing) {
        mensajeError = 'Este campo es obligatorio.';
      } else if (validity.typeMismatch) {
        mensajeError = 'Debe ser un correo electrónico válido.';
      } else if (validity.tooShort) {
        mensajeError = `Debe tener al menos ${input.minLength} caracteres.`;
      } else if (validity.tooLong) {
        mensajeError = `No debe exceder de ${input.maxLength} caracteres.`;
      } else {
        // Un error genérico si no es ninguno de los anteriores
        mensajeError = 'El valor ingresado es incorrecto.';
      }
      
      
      // Mostramos el error
      errorElement.textContent = mensajeError;
      errorElement.classList.add('is-visible');
      input.classList.add('is-invalid');
      
      // (Opcional) Si quieres usar setCustomValidity para bloquear el form
      // input.setCustomValidity(mensajeError); 

      return false; // Indicamos que hubo un error
    } 
    // Si el campo SÍ es válido...
    else {
      // Limpiamos cualquier mensaje de error
      errorElement.textContent = '';
      errorElement.classList.remove('is-visible');
      input.classList.remove('is-invalid');
      
      return true; // Indicamos que todo está bien
    }
  }

  // --- EVENTO 1: VALIDACIÓN EN TIEMPO REAL (mientras se escribe) ---
  camposAValidar.forEach(input => {
    // Se dispara cada vez que el usuario escribe algo
    input.addEventListener('input', () => {
      validarCampo(input); // Valida solo este campo
    });
  });

  // --- VALIDACIÓN ESPECÍFICA: reglas de "pass-fuerte" ---
  password.addEventListener('input', () => {
    const pass = password.value;
    let mensajeError = '';

    // 1. Comprobar caracteres especiales
    if (!/[@$!%*?&]/.test(pass)) {
      mensajeError = 'Debe contener al menos un carácter especial.';
    }
    // 2. Comprobar longitud
    if (pass.length < 8) {
      mensajeError = 'Debe tener al menos 8 caracteres.';
    } 
    // 3. Comprobar mayúscula (usando regex)
    else if (!/[A-Z]/.test(pass)) {
      mensajeError = 'Debe contener al menos una letra mayúscula.';
    }
    // 4. Comprobar minúscula
    else if (!/[a-z]/.test(pass)) {
      mensajeError = 'Debe contener al menos una letra minúscula.';
    }
    // 5. Comprobar número
    else if (!/[0-9]/.test(pass)) {
      mensajeError = 'Debe contener al menos un número.';
    }
    
    // Si hubo algún error (mensajeError no está vacío)
    if (mensajeError) {
      passwordInput.setCustomValidity(mensajeError);
      if (errorPassword) errorPassword.textContent = mensajeError;
    } else {
      // Si pasó todas las reglas, limpiamos
      passwordInput.setCustomValidity('');
      if (errorPassword) errorPassword.textContent = '';
    }

    // Opcional: reportar el error inmediatamente
    // passwordInput.reportValidity(); 
  });

  // --- EVENTO 2: VALIDACIÓN FINAL (al intentar enviar) ---
  form.addEventListener('submit', (event) => {
    // Prevenimos que el formulario se envíe automáticamente
    event.preventDefault(); 
    
    let esFormularioValido = true;
    
    // Validamos todos los campos uno por uno
    camposAValidar.forEach(input => {
      // Si *alguno* de los campos no es válido, el formulario entero no lo es
      if (!validarCampo(input)) {
        esFormularioValido = false;
      }
    });

    
    
    // Si después de validar todos, el formulario sigue siendo válido...
    if (esFormularioValido) {
      console.log('¡Formulario válido! Enviando...');
      // Aquí es donde realmente enviarías el formulario:
      // form.submit(); 
      // o usarías fetch() para enviarlo por AJAX
    } else {
      console.log('El formulario contiene errores.');
    }
  });

});
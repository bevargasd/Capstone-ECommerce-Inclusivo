document.addEventListener('DOMContentLoaded', () => {
  // Obtener referencia al formulario principal
  const form = document.getElementById('register-form');
  if (!form) return;

  // Objeto con referencias a todos los campos del formulario
  const fields = {
    username: document.getElementById('id_username'),
    email: document.getElementById('id_email'),
    firstName: document.getElementById('id_first_name'),
    lastName: document.getElementById('id_last_name'),
    pw1: document.getElementById('id_password1'),
    pw2: document.getElementById('id_password2'),
    phone: document.getElementById('id_phone'),
    dob: document.getElementById('id_dob'),
    avatar: document.getElementById('id_avatar'),
    terms: document.getElementById('id_terms_accepted'),
    zip: document.getElementById('id_zip_code'),
    street: document.getElementById('id_street'),
    city: document.getElementById('id_city'),
    state: document.getElementById('id_state'), 
    country: document.getElementById('id_country'),
  };

  // Función auxiliar: crea o encuentra el elemento de error después del input
  function getErrorEl(input) {
    if (!input) return null;
    const id = 'error-' + input.id;
    let el = document.getElementById(id);
    if (!el) {
      el = document.createElement('div');
      el.id = id;
      el.className = 'error-message';
      el.style.color = 'red';
      el.style.fontSize = '0.9rem';
      input.insertAdjacentElement('afterend', el);
    }
    return el;
  }

  // Función para mostrar u ocultar mensajes de error
  function setError(input, msg) {
    const el = getErrorEl(input);
    if (!input) return;
    if (msg) {
      input.classList.add('is-invalid');
      input.setCustomValidity(msg);
      if (el) el.textContent = msg;
    } else {
      input.classList.remove('is-invalid');
      input.setCustomValidity('');
      if (el) el.textContent = '';
    }
  }

  // --- REGLAS DE VALIDACIÓN POR CAMPO ---

  // Validación de nombre de usuario
  function validateUsername(input) {
    if (!input) return true;
    const v = input.value.trim();
    if (!v) { setError(input, 'Nombre de usuario obligatorio.'); return false; }
    if (v.length < 3) { setError(input, 'Debe tener al menos 3 caracteres.'); return false; }
    if (!/^[a-zA-Z0-9_]+$/.test(v)) { setError(input, 'Sólo letras, números y guion bajo.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de correo electrónico
  function validateEmail(input) {
    if (!input) return true;
    const v = input.value.trim();
    if (!v) { setError(input, 'Correo obligatorio.'); return false; }
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!re.test(v)) { setError(input, 'Correo inválido.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de nombres y apellidos
  function validateName(input) {
    if (!input) return true;
    const v = input.value.trim();
    if (!v) { setError(input, ''); return true; } // optional
    if (v.length > 50) { setError(input, 'Demasiado largo.'); return false; }
    if (!/^[\p{L}\s'.-]+$/u.test(v)) { setError(input, 'Caracteres inválidos.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de contraseña principal
  function validatePassword1(input) {
    if (!input) return true;
    const v = input.value;
    if (!v) { setError(input, 'Contraseña obligatoria.'); return false; }
    if (v.length < 8) { setError(input, 'Debe tener al menos 8 caracteres.'); return false; }
    if (!/[A-Z]/.test(v)) { setError(input, 'Debe contener al menos una mayúscula.'); return false; }
    if (!/[a-z]/.test(v)) { setError(input, 'Debe contener al menos una minúscula.'); return false; }
    if (!/[0-9]/.test(v)) { setError(input, 'Debe contener al menos un número.'); return false; }
    if (!/[@$!%*?&\W]/.test(v)) { setError(input, 'Debe contener al menos un carácter especial.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de confirmación de contraseña
  function validatePassword2(input) {
    if (!input) return true;
    const v = input.value;
    if (!v) { setError(input, 'Confirma la contraseña.'); return false; }
    if (fields.pw1 && fields.pw1.value !== v) { setError(input, 'Las contraseñas no coinciden.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de teléfono (opcional)
  function validatePhone(input) {
    if (!input) return true;
    const v = input.value.trim();
    if (!v) { setError(input, ''); return true; } // optional
    if (!/^[+\d]?(?:[\d\s\-]{6,})$/.test(v)) { setError(input, 'Teléfono inválido.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de fecha de nacimiento
  function validateDOB(input) {
    if (!input) return true;
    const v = input.value;
    if (!v) { setError(input, ''); return true; } // optional
    const dob = new Date(v);
    if (isNaN(dob)) { setError(input, 'Fecha inválida.'); return false; }
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) age--;
    if (age < 13) { setError(input, 'Debes tener al menos 13 años.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de avatar/imagen
  function validateAvatar(input) {
    if (!input) return true;
    const f = input.files && input.files[0];
    if (!f) { setError(input, ''); return true; }
    const max = 2 * 1024 * 1024; // 2MB
    if (f.size > max) { setError(input, 'El archivo debe ser <= 2MB.'); return false; }
    if (!/^image\/(jpeg|png)$/.test(f.type)) { setError(input, 'Sólo JPG o PNG.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de código postal
  function validateZip(input) {
    if (!input) return true;
    const v = input.value.trim();
    if (!v) { setError(input, ''); return true; }
    if (!/^[0-9A-Za-z\- ]{3,10}$/.test(v)) { setError(input, 'Código postal inválido.'); return false; }
    setError(input, '');
    return true;
  }

  // Validación de términos y condiciones
  function validateTerms(input) {
    if (!input) return true;
    if (!input.checked) { setError(input, 'Debes aceptar los términos.'); return false; }
    setError(input, '');
    return true;
  }

  // Función dispatched que determina qué validación aplicar según el campo
  function validateInput(input) {
    if (!input) return true;
    switch (input.id) {
      case 'id_username': return validateUsername(input);
      case 'id_email': return validateEmail(input);
      case 'id_first_name': return validateName(input);
      case 'id_last_name': return validateName(input);
      case 'id_password1': {
        const ok = validatePassword1(input);
        // revalidate confirmation
        if (fields.pw2) validatePassword2(fields.pw2);
        return ok;
      }
      case 'id_password2': return validatePassword2(input);
      case 'id_phone': return validatePhone(input);
      case 'id_dob': return validateDOB(input);
      case 'id_avatar': return validateAvatar(input);
      case 'id_zip_code': return validateZip(input);
      case 'id_terms_accepted': return validateTerms(input);
      default:
        // simple length checks for address fields
        if (['id_street','id_city','id_state','id_country'].includes(input.id)) {
          if (input.value && input.value.length > 100) { setError(input, 'Demasiado largo.'); return false; }
          setError(input, ''); return true;
        }
        return true;
    }
  }

  // Agregar listeners para validación en tiempo real
  Object.values(fields).forEach(el => {
    if (!el) return;
    // Usar 'change' para checkbox/select/file, 'input' para texto
    const ev = (el.type === 'checkbox' || el.tagName === 'SELECT' || el.type === 'file') ? 'change' : 'input';
    el.addEventListener(ev, () => validateInput(el));
  });

  // Validación al enviar el formulario
  form.addEventListener('submit', (e) => {
    let valid = true;
    // Orden de validación (prioridad visual)
    const order = ['id_username','id_email','id_first_name','id_last_name','id_password1','id_password2',
                   'id_phone','id_dob','id_avatar','id_street','id_city','id_state','id_zip_code','id_country','id_terms_accepted'];
    let firstInvalid = null;
    
    // Validar todos los campos en orden
    order.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      const ok = validateInput(el);
      if (!ok) {
        valid = false;
        if (!firstInvalid) firstInvalid = el;
      }
    });

    // Si hay errores, prevenir envío y enfocar primer campo inválido
    if (!valid) {
      e.preventDefault();
      if (firstInvalid) firstInvalid.focus();
      return false;
    }
    return true; // Permitir envío si todo está válido
  });

});
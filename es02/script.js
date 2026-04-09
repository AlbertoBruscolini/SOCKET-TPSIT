const form = document.getElementById('studentForm');
const ripetente = document.getElementById('ripetente');
const anniRipetuti = document.getElementById('anniRipetuti');
const errorContainer = document.getElementById('formErrors');

ripetente.addEventListener('change', () => {
  anniRipetuti.disabled = !ripetente.checked;
  if (!ripetente.checked) {
    anniRipetuti.value = '';
    anniRipetuti.classList.remove('field-error');
  }
});

function getSelectedValues(select) {
  return Array.from(select.options)
    .filter(option => option.selected)
    .map(option => option.value);
}

function clearValidation() {
  errorContainer.innerHTML = '';
  form.querySelectorAll('.field-error').forEach(el => el.classList.remove('field-error'));
}

function validateField(element, message) {
  element.classList.add('field-error');
  return message;
}

form.addEventListener('submit', event => {
  event.preventDefault();
  clearValidation();

  const nome = document.getElementById('nome');
  const cognome = document.getElementById('cognome');
  const dataNascita = document.getElementById('dataNascita');
  const codiceFiscale = document.getElementById('codiceFiscale');
  const classe = document.getElementById('classe');
  const sezione = document.getElementById('sezione');
  const uscitaCheckboxes = document.querySelectorAll('input[name="uscita"]:checked');

  const errors = [];

  if (!nome.value.trim()) {
    errors.push(validateField(nome, 'Nome è obbligatorio.'));
  }

  if (!cognome.value.trim()) {
    errors.push(validateField(cognome, 'Cognome è obbligatorio.'));
  }

  if (!dataNascita.value) {
    errors.push(validateField(dataNascita, 'Data di nascita è obbligatoria.'));
  }

  const cfValue = codiceFiscale.value.trim().toUpperCase();
  const cfRegex = /^[A-Z0-9]{16}$/;
  if (!cfValue) {
    errors.push(validateField(codiceFiscale, 'Codice fiscale è obbligatorio.'));
  } else if (!cfRegex.test(cfValue)) {
    errors.push(validateField(codiceFiscale, 'Codice fiscale deve essere 16 caratteri alfanumerici.'));
  }

  const selectedClassi = getSelectedValues(classe);
  if (selectedClassi.length === 0) {
    errors.push(validateField(classe, 'Devi selezionare almeno una classe.'));
  }

  const selectedSezioni = getSelectedValues(sezione);
  if (selectedSezioni.length === 0) {
    errors.push(validateField(sezione, 'Devi selezionare almeno una sezione.'));
  }

  const selectedUscite = Array.from(uscitaCheckboxes).map(checkbox => checkbox.value);
  if (selectedUscite.length === 0) {
    const uscitaGroup = document.getElementById('uscitaGroup');
    uscitaGroup.classList.add('field-error');
    errors.push('Devi selezionare almeno un tipo di uscita.');
  }

  if (ripetente.checked) {
    const anni = anniRipetuti.value;
    if (anni === '' || Number(anni) < 1) {
      errors.push(validateField(anniRipetuti, 'Inserisci almeno 1 anno ripetuto.'));
    }
  }

  if (errors.length > 0) {
    errorContainer.innerHTML = '<strong>Problemi rilevati:</strong><ul>' + errors.map(err => `<li>${err}</li>`).join('') + '</ul>';
    window.scrollTo({ top: errorContainer.offsetTop - 20, behavior: 'smooth' });
    return;
  }

  const result = {
    nome: nome.value.trim(),
    cognome: cognome.value.trim(),
    dataNascita: dataNascita.value,
    codiceFiscale: cfValue,
    classi: selectedClassi,
    sezioni: selectedSezioni,
    ripetente: ripetente.checked,
    anniRipetuti: ripetente.checked ? Number(anniRipetuti.value) : 0,
    uscita: selectedUscite
  };

  localStorage.setItem('studentRegistrationResult', JSON.stringify(result, null, 2));
  window.location.href = 'result.html';
});

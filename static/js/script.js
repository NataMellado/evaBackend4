usersContainer = document.getElementById("formContainer");
console.log(personas);

var usersList = [];

var isEditing = false;
var lastEdited = null;

for (const persona of personas) {
  personaAgregar = {
    userId: persona.id,
    nombre: persona.nombre,
    apellidos: persona.apellidos,
    edad: persona.edad.toString(),
    fecha_nacimiento: persona.fecha_nacimiento.toString(),
    telefono: persona.telefono.toString(),
    email: persona.email.toString(),
    cant_visitas: persona.cant_visitas.toString(),
  };
  usersList.push(personaAgregar);
}
console.log("userslist");
console.log(usersList);
/**
 * Obtiene un usuario con sus datos por defecto
 */
const getUser = (userId) => {
  for (const user of usersList) {
    if (user.userId == userId) {
      console.log("user encontrado: " + userId);
      console.log(user)
      return user;
    }
  }
  return null;
};

/**
 * Detecta si hay cambios en los inputs de un usuario
 * Hace lo siguiente:
 * 1. Obtiene los datos por defecto
 * 2. Compara los datos por defecto del usuario
 * con los datos de los inputs de ese usuario
 */
const detectChanges = (userId) => {
  defaultData = getUser(userId);
  // console.log("default data!:")
  // console.log(defaultData)
  nombre = document.getElementById("nombre" + userId).value;
  apellidos = document.getElementById("apellidos" + userId).value;
  edad = document.getElementById("edad" + userId).value;
  fecha_nacimiento = document.getElementById("fecha_nacimiento" + userId).value;
  telefono = document.getElementById("telefono" + userId).value;
  email = document.getElementById("email" + userId).value;
  cant_visitas = document.getElementById("cant_visitas" + userId).value;
  // console.log(
  //   {
  //     nombre,
  //     apellidos,
  //     edad,
  //     fecha_nacimiento,
  //     telefono,
  //     email,
  //     cant_visitas,
  //   }
  // )
  if (
    nombre !== defaultData.nombre ||
    apellidos !== defaultData.apellidos ||
    edad !== defaultData.edad ||
    fecha_nacimiento !== defaultData.fecha_nacimiento ||
    telefono !== defaultData.telefono ||
    email !== defaultData.email ||
    cant_visitas !== defaultData.cant_visitas
  ) {
    console.log("Se detectaron cambios");
    return true;
  }
  console.log("No se detectaron cambios");
  return false;
};

/**
 * Habilita o deshabilita los inputs de un usuario
 * También si se le da un 2do parámetro:
 * ["disable", "enable"]
 * puede deshabilitar o habilitar los inputs de dicho usuario
 */
const toggleUserInputs = (userId, toggleTo = null) => {
  
  // Si se "deshabilita" y NO tiene el atributo disabled
  if (
    toggleTo == "disable" &&
    !document.getElementById("nombre" + userId).hasAttribute("disabled")
  ) {
    document.getElementById("nombre" + userId).disabled = true;
    document.getElementById("apellidos" + userId).disabled = true;
    document.getElementById("edad" + userId).disabled = true;
    document.getElementById("fecha_nacimiento" + userId).disabled = true;
    document.getElementById("telefono" + userId).disabled = true;
    document.getElementById("email" + userId).disabled = true;
    document.getElementById("cant_visitas" + userId).disabled = true;
    return;
  // Si se "habilita" y SÍ tiene el atributo disabled
  } else if (
    toggleTo == "enable" &&
    document.getElementById("nombre" + userId).hasAttribute("disabled")
  ) {
    document.getElementById("nombre" + userId).removeAttribute("disabled");
    document.getElementById("apellidos" + userId).removeAttribute("disabled");
    document.getElementById("edad" + userId).removeAttribute("disabled");
    document.getElementById("fecha_nacimiento" + userId).removeAttribute("disabled");
    document.getElementById("telefono" + userId).removeAttribute("disabled");
    document.getElementById("email" + userId).removeAttribute("disabled");
    document.getElementById("cant_visitas" + userId).removeAttribute("disabled");
    return;
  }
  // Si en este punto el toggleTo es null, se retorna
  if (toggleTo != null) return;
  
  // Revisa si tiene un campo deshabilitado, y si lo tiene habilita todos los campos
  if (document.getElementById("nombre" + userId).hasAttribute("disabled")) {
    document.getElementById("nombre" + userId).removeAttribute("disabled");
    document.getElementById("apellidos" + userId).removeAttribute("disabled");
    document.getElementById("edad" + userId).removeAttribute("disabled");
    document.getElementById("fecha_nacimiento" + userId).removeAttribute("disabled");
    document.getElementById("telefono" + userId).removeAttribute("disabled");
    document.getElementById("email" + userId).removeAttribute("disabled");
    document.getElementById("cant_visitas" + userId).removeAttribute("disabled");
  // Si no tiene ningún campo deshabilitado, deshabilita todos los campos
  } else { 
    document.getElementById("nombre" + userId).disabled = true;
    document.getElementById("apellidos" + userId).disabled = true;
    document.getElementById("edad" + userId).disabled = true;
    document.getElementById("fecha_nacimiento" + userId).disabled = true;
    document.getElementById("telefono" + userId).disabled = true;
    document.getElementById("email" + userId).disabled = truedisabled = true;
    document.getElementById("cant_visitas" + userId).disabled = true;
  }
};

/**
 * Toma el usuario por defecto, busca sus inputs y les
 * coloca la información que viene por defecto desde la base de datos
 * Luego DESHABILITA los inputs del usuario
 * y se setea isEditing a false
 */
const resetUserData = (userId) => {
  user = getUser(userId);
  document.getElementById("nombre" + userId).value = user.nombre;
  document.getElementById("apellidos" + userId).value = user.apellidos;
  document.getElementById("edad" + userId).value = user.edad;
  document.getElementById("fecha_nacimiento" + userId).value = user.fecha_nacimiento;
  document.getElementById("telefono" + userId).value = user.telefono;
  document.getElementById("email" + userId).value = user.email;
  document.getElementById("cant_visitas" + userId).value = user.cant_visitas;
  toggleUserInputs(userId, "disable");
  isEditing = false;
  lastEdited = null;
};


/**
 * Función que se llama al hacer click en el botón de editar un usuario ->
 * 
 * Al hacer click en un usuario:
 * 
 * Primero verifica si se estaba editando un usuario diferente al clickeado.
 * 
 * Luego, si se estaba editando un usuario y no es el mismo,
 * se verifica si hay cambios en el usuario editado
 *
 * Si se encuentran cambios, se pregunta si se desean guardar los cambios
 ** Al guardar los cambios:
 *  Se llama la función {[saveUserForm()]} pasándole el usuario que se editó
 ** Al NO guardar los cambios:
 * Se restauran los datos por defecto del usuario editado (y se deshabilita input)
 * y se habilita el input del nuevo usuario clickeado
 */
const editFunction = (event, userId) => {
  console.log("Editando: " + userId);
  if (lastEdited != null && lastEdited != userId && detectChanges(lastEdited)) {
    var deseaGuardarCambios = confirm(
      "¿Deseas guardar los cambios realizados?"
    );
    // Si se desean guardar los cambios, enviar formulario
    if (deseaGuardarCambios) {
      saveUserForm(event, lastEdited);
      return;
    // Si no, resetear datos del user editado y habilitar inputs del user clickeado
    } else {
      resetUserData(lastEdited);
      toggleUserInputs(userId, "enable");
      lastEdited = userId;
      isEditing = true;
      lastEditedUser = getUser(userId);
      return;
    }
  // Si se hace click en el mismo usuario que se estaba editando, no hacer nada
  } else if (lastEdited == userId) {
    //TODO: Se pueden detectar cambios y hacer la misma pregunta
    return;
  }

  /* Si se clickea un usuario diferente, se resetea el usuario anterior */
  if (lastEdited != null && lastEdited != userId) {
    resetUserData(lastEdited);
  }

  // Se intercambian los inputs del usuario que se clickeó
  // (si estaba habilitado, se deshabilitan y viceversa)
  toggleUserInputs(userId);
  // Se establece isEditing a verdadero
  // Se establece lastEdited como la ID usuario que se está editando
  isEditing = true;
  lastEdited = userId;
  lastEditedUser = getUser(userId);
};

/**
 * Función que se llama al hacer click en el botón de guardar un usuario ->
 * Verifica si se estaba editando un usuario antes de guardar
 ** Si no se editó ningún usuario, se muestra un alert
 ** Si se clickea guardar a otro usuario que no se editó, se muestra un alert
 */
const saveFunction = (event, userId) => {
  if (lastEdited == null) {
    alert("No hay cambios que guardar!");
    return;
  }
  // Si el click en GUARDAR es a un usuario diferente al que se editó, alerta
  if (lastEdited != userId) {
    window.location.href = "/users/?message=error";
    return;
  }

  sendForm(event, userId);
};

/**
 * Función que envía el formulario de un usuario
 */
const sendForm = (event, userId) => {
  event.preventDefault();
  const form = document.getElementById("usersContainerForm" + userId);

  if (form.classList.contains("submitting")) {
    return; // Evita enviar el formulario nuevamente
  }
  form.addEventListener("submit", () => {
    // Simula un retraso para quitar la clase al completarse el envío
    setTimeout(() => form.classList.remove("submitting"), 5000);
  });
  // Marcar el formulario como enviándose
  form.classList.add("submitting");

  // Crea el input hidden para enviar el userId en la request
  var hiddenInput = document.createElement("input");
  hiddenInput.setAttribute("type", "hidden");
  hiddenInput.setAttribute("name", "userId");
  hiddenInput.setAttribute("value", userId);

  // Se agrega el input hidden al formulario de dicho usuario
  document
    .getElementById("usersContainerForm" + userId)
    .appendChild(hiddenInput);

  // Se envía el formulario
  form.submit();
};

/**
 * Función que deshabilita todos los inputs de todos los usuarios
 */
const disableUserInputs = (usersList) => {
  // Recorre la lista usuarios 
  usersList.forEach((persona) => {
    console.log("Deshabilitando inputs de user:" + persona.userId);
    // Para cada ID de usuario, deshabilita los inputs
    toggleUserInputs(persona.userId, "disable");
  });
};

/**
 * Función que guarda los datos de un usuario ESPECÍFICO
 * Sirve para guardar cuando se solicita la confirmación, y no
 * directamente desde el botón guardar
 */
const saveUserForm = (event, userId) => {
  // RECORDAR:
  // - Los inputs del usuario a guardar deben estar habilitados
  // es decir, sin la etiqueta "disabled" al momento de enviarse
  console.log(usersList);
  // Se deshabilitan todos los inputs de todos los usuarios
  // disableUserInputs(usersList);
  console.log("Habilitando inputs de user");
  // Se habilitan sólo los inputs del usuario a guardar
  toggleUserInputs(userId, "enable");
  console.log("Enviando form");
  // Se envía el formulario de dicho usuario
  sendForm(event, userId);
};

/**
 * Función que se llama al hacer click en el botón de eliminar un usuario ->
 */
const deleteFunction = (userId) => {
  const form = document.getElementById("usersContainerForm" + userId);

  // Detectar si el formulario ya se está enviando
  if (form.classList.contains("submitting")) {
    return; // Evita enviar el formulario nuevamente
  }

  form.addEventListener("submit", () => {
    // Simula un retraso para quitar la clase al completarse el envío
    setTimeout(() => form.classList.remove("submitting"), 5000);
  });
  // Marcar el formulario como enviándose
  form.classList.add("submitting");
  // Crea el input hidden para enviar el userId en la request
  var hiddenInput = document.createElement("input");
  hiddenInput.setAttribute("type", "hidden");
  hiddenInput.setAttribute("name", "deleteUser");
  hiddenInput.setAttribute("value", userId);

  // Se agrega el input hidden al formulario de dicho usuario
  document
    .getElementById("usersContainerForm" + userId)
    .appendChild(hiddenInput);

  // Se envía el formulario
  form.submit();
  
}

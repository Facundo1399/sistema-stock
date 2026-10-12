const API_URL = "http://127.0.0.1:8000";

function getAuthorizationHeaders(token) {
  if (!token?.trim()) {
    throw new Error("Se necesita iniciar sesión para operar con productos.");
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}

async function getErrorMessage(response) {
  const responseText = await response.text();

  if (!responseText) {
    return `Error de la API: ${response.status}`;
  }

  try {
    const errorData = JSON.parse(responseText);
    const detail = errorData.detail;
    return typeof detail === "string"
      ? detail
      : detail
        ? JSON.stringify(detail)
        : responseText;
  } catch {
    return responseText;
  }
}

async function checkResponse(response) {
  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return response.json();
}

export async function iniciarSesion(email, password) {
  const credentials = new URLSearchParams({
    username: email,
    password,
  });
  const response = await fetch(`${API_URL}/users/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: credentials,
  });

  return checkResponse(response);
}

export async function obtenerProductos(token) {
  const response = await fetch(`${API_URL}/productos/`, {
    headers: getAuthorizationHeaders(token),
  });

  return checkResponse(response);
}

export async function obtenerProveedores(token) {
  const response = await fetch(`${API_URL}/proveedores/`, {
    headers: getAuthorizationHeaders(token),
  });

  return checkResponse(response);
}

export async function crearProducto(producto, token) {
  const response = await fetch(`${API_URL}/productos/`, {
    method: "POST",
    headers: {
      ...getAuthorizationHeaders(token),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(producto),
  });

  return checkResponse(response);
}

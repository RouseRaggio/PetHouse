import API_URL from './api';

/* =========================
   GET ALL USERS
========================= */
export async function getUsers() {
	const response = await fetch(`${API_URL}/users/`);

	if (!response.ok) {
		throw new Error('Error obteniendo usuarios');
	}

	return await response.json();
}

/* =========================
   GET USER BY ID
========================= */
export async function getUser(id) {
	const response = await fetch(`${API_URL}/users/${id}`);

	if (!response.ok) {
		throw new Error('Usuario no encontrado');
	}

	return await response.json();
}

/*
   GET USER BY EMAIL
========================= */
export async function getUserByEmail(email) {
	const response = await fetch(`${API_URL}/users/email/${email}`);

	if (!response.ok) {
		throw new Error('Usuario no encontrado');
	}

	return await response.json();
}

/* =========================
   LOGIN USER
========================= */
export async function loginUser(email, password) {
	const response = await fetch(`${API_URL}/users/login`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ email, password })
		
	});

	if (!response.ok) {
		throw new Error('Credenciales incorrectas');
	}

	return await response.json();
}

export async function createUser(userData) {
	const response = await fetch(`${API_URL}/users/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${localStorage.getItem('token')}`
		},
		body: JSON.stringify(userData)
	});

	if (!response.ok) {
		const errorData = await response.json().catch(() => ({}));
		throw new Error(errorData.detail || 'Error creando usuario');
	}

	return await response.json();
}

/* =========================
   REGISTER USER (Public)
========================= */
export async function registerUser(userData) {
	const response = await fetch(`${API_URL}/users/register`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(userData)
	});

	if (!response.ok) {
		const errorData = await response.json().catch(() => ({}));
		throw new Error(errorData.detail || 'Error en el registro');
	}

	return await response.json();
}

/* =========================
   UPDATE USER
========================= */
export async function updateUser(id, user) {
	const response = await fetch(`${API_URL}/users/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${localStorage.getItem('token')}`
		},
		body: JSON.stringify(user)
	});

	if (!response.ok) {
		throw new Error('Error actualizando usuario');
	}

	return await response.json();
}

/* =========================
   DELETE USER (SOFT DELETE)
========================= */
export async function deleteUser(id) {
	const response = await fetch(`${API_URL}/users/${id}`, {
		method: 'DELETE'
	});

	if (!response.ok) {
		throw new Error('Error eliminando usuario');
	}

	return await response.json();
}

/* =========================
   RESTORE USER
========================= */
export async function restoreUser(id) {
	const response = await fetch(`${API_URL}/users/restore/${id}`, {
		method: 'PUT'
	});

	if (!response.ok) {
		throw new Error('Error restaurando usuario');
	}

	return await response.json();
}

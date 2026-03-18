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

/* =========================
   CREATE USER
========================= */
export async function createUser(userData) {
	const response = await fetch(`${API_URL}/users`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(userData)
	});

	if (!response.ok) {
		throw new Error('Error creando usuario');
	}

	return await response.json();
}

/* =========================
   UPDATE USER
========================= */
export async function updateUser(id, user) {
	const res = await fetch(`http://localhost:8000/users/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(user)
	});

	if (!res.ok) {
		throw new Error('Error actualizando usuario');
	}

	return await res.json();
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

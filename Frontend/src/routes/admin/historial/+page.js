import { PUBLIC_API_URL } from '$env/static/public';

export async function load({ fetch, cookies }) {
	try {
		// Obtener token de las cookies (para acceso en el servidor)
		const token = cookies.get('token');
		const headers = {
			'Content-Type': 'application/json',
			...(token ? { 'Authorization': `Bearer ${token}` } : {})
		};

		const apiUrl = PUBLIC_API_URL || 'http://localhost:8000';

		// Obtener logs de auditoría real del backend
		const logsRes = await fetch(`${apiUrl}/audit-logs/?limit=100&offset=0`, { headers });

		if (!logsRes.ok) {
			console.error('Error fetching audit logs:', logsRes.status, logsRes.statusText);
			throw new Error(`Error al cargar historial: ${logsRes.status}`);
		}

		const logs = await logsRes.json();
		
		// Obtener información de usuarios para enriquecer los datos
		const usersRes = await fetch(`${apiUrl}/users/`, { headers });
		const users = usersRes.ok ? await usersRes.json() : [];

		return {
			historial: Array.isArray(logs) ? logs : [],
			users: Array.isArray(users) ? users : []
		};
	} catch (error) {
		console.error('Error en load:', error);
		return {
			historial: [],
			users: [],
			error: error.message
		};
	}
}

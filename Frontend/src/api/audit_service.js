import API_URL, { getAuthHeaders } from './api.js';

/**
 * Simula auditoría usando endpoints reales del backend
 * ya que no existe /audit-logs en el backend actual.
 */
export async function getAuditLogs(params = {}) {
	try {
		const headers = getAuthHeaders();

		const [adoptionsRes, usersRes] = await Promise.all([
			fetch(`${API_URL}/adoptions/`, { headers }),
			fetch(`${API_URL}/users/`, { headers })
		]);

		const adoptions = adoptionsRes.ok ? await adoptionsRes.json() : [];
		const users = usersRes.ok ? await usersRes.json() : [];

		// Convertir adopciones en registros de auditoría
		let logs = adoptions.map((a) => ({
			id: a.id,
			user_id: a.adoptante_id,
			action: a.status_id === 1 ? 'create' : 'update',
			resource: 'adoption',
			resource_id: a.id,
			details: `Solicitud de adopción mascota #${a.pet_id}`,
			changes: a,
			timestamp: a.fecha_solicitud,
			status: 'success',
			ip_address: null
		}));

		// Aplicar filtros
		if (params.action)     logs = logs.filter((l) => l.action === params.action);
		if (params.resource)   logs = logs.filter((l) => l.resource === params.resource);
		if (params.user_id)    logs = logs.filter((l) => l.user_id === Number(params.user_id));
		if (params.start_date) logs = logs.filter((l) => new Date(l.timestamp) >= new Date(params.start_date));
		if (params.end_date)   logs = logs.filter((l) => new Date(l.timestamp) <= new Date(params.end_date));

		// Paginación
		const offset = params.offset || 0;
		const limit  = params.limit  || 20;
		return logs.slice(offset, offset + limit);

	} catch (error) {
		console.error('getAuditLogs:', error);
		return [];
	}
}

export async function exportAuditLogsCSV(params = {}) {
	const logs = await getAuditLogs(params);

	const headers = ['ID', 'Usuario', 'Acción', 'Recurso', 'Recurso ID', 'Fecha', 'Estado'];
	const rows = logs.map((l) => [
		l.id,
		l.user_id ? `Usuario #${l.user_id}` : 'Sistema',
		l.action,
		l.resource,
		l.resource_id || '-',
		l.timestamp ? new Date(l.timestamp).toLocaleString('es-CO') : '-',
		l.status
	]);

	const csv = [headers, ...rows].map((r) => r.join(',')).join('\n');

	return {
		content: csv,
		filename: `auditoria_${new Date().toISOString().slice(0, 10)}.csv`
	};
}
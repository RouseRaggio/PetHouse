import API_URL, { getAuthHeaders } from './api';

export const getAuditLogs = async ({ user_id, action, resource, start_date, end_date, limit = 20, offset = 0 } = {}) => {
  try {
    const params = new URLSearchParams();

    if (user_id) params.append('user_id', user_id);
    if (action) params.append('action', action);
    if (resource) params.append('resource', resource);
    if (start_date) params.append('start_date', start_date);
    if (end_date) params.append('end_date', end_date);
    params.append('limit', limit);
    params.append('offset', offset);

    const response = await fetch(`${API_URL}/audit-logs?${params.toString()}`, {
      credentials: 'include',
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || error.message || 'Error al obtener el historial de auditoría');
    }

    return await response.json();
  } catch (error) {
    console.error('getAuditLogs:', error);
    throw error;
  }
};

export const exportAuditLogsCSV = async ({ user_id, action, resource, start_date, end_date } = {}) => {
  try {
    const params = new URLSearchParams();

    if (user_id) params.append('user_id', user_id);
    if (action) params.append('action', action);
    if (resource) params.append('resource', resource);
    if (start_date) params.append('start_date', start_date);
    if (end_date) params.append('end_date', end_date);

    const response = await fetch(`${API_URL}/audit-logs/export/csv?${params.toString()}`, {
      credentials: 'include',
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || error.message || 'Error al exportar el historial');
    }

    return await response.json();
  } catch (error) {
    console.error('exportAuditLogsCSV:', error);
    throw error;
  }
};

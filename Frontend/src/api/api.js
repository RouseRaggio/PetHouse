const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default API_URL;

export function getAuthHeaders() {
	const token = localStorage.getItem('token');
	return {
		'Content-Type': 'application/json',
		...(token ? { 'Authorization': `Bearer ${token}` } : {})
	};
}
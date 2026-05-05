const API_URL = "http://localhost:8000";

export default API_URL;

export function getAuthHeaders() {
	const token = localStorage.getItem('token');
	return {
		'Content-Type': 'application/json',
		...(token ? { 'Authorization': `Bearer ${token}` } : {})
	};
}	

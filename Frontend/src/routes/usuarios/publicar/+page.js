import { redirect } from '@sveltejs/kit';

export async function load({ url, depends }) {
	// Mark this load function as depending on auth
	depends('app:auth');

	// Check if we're on the client side
	if (typeof window !== 'undefined') {
		const token = localStorage.getItem('token');
		const userStr = localStorage.getItem('user');

		// If not authenticated, save the URL and redirect to login
		if (!token || !userStr) {
			localStorage.setItem('redirectAfterLogin', url.pathname);
			throw redirect(302, '/login?message=Para publicar una mascota debe iniciar sesión');
		}

		try {
			const user = JSON.parse(userStr);
			return { user };
		} catch (error) {
			localStorage.removeItem('token');
			localStorage.removeItem('user');
			localStorage.setItem('redirectAfterLogin', url.pathname);
			throw redirect(302, '/login?message=Para publicar una mascota debe iniciar sesión');
		}
	}

	// On server side, no auth check needed (SSR will be skipped)
	return {};
}
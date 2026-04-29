import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const initialAuth = {
	token: null,
	user: null
};

export const auth = writable(initialAuth);

if (browser) {
	const storedToken = localStorage.getItem('token');
	const storedUser = localStorage.getItem('user');

	if (storedToken || storedUser) {
		auth.set({
			token: storedToken,
			user: storedUser ? JSON.parse(storedUser) : null
		});
	}
}

export function setAuth(token, user) {
	if (browser) {
		localStorage.setItem('token', token);
		localStorage.setItem('user', JSON.stringify(user));
	}
	auth.set({ token, user });
}

export function clearAuth() {
	if (browser) {
		localStorage.removeItem('token');
		localStorage.removeItem('user');
	}
	auth.set(initialAuth);
}

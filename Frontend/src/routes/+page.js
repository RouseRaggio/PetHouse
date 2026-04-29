import { getPets } from '../api/pet_service.js';

export async function load() {
	try {
		const pets = await getPets();
		return { pets };
	} catch (error) {
		console.error('Error loading pets:', error);
		return { pets: [] };
	}
}

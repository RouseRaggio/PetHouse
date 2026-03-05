//import { getPets } from '$lib/services/api';

/*//export async function load() {
	try {
		const pets = await getPets();
		return { pets };
	} catch (error) {
		console.error("Error cargando mascotas:", error);
		return { pets: [] };
	}
}//*/

//este es pa ve lo que estoy haciendo mientras mientras, es el de arriba
export async function load() {
	return {
		pets: [
			{
				id: 1,
				name: "Luna",
				species: "Perro",
                race: "Labrador",
				age: 2,
				gender: "Hembra",
				description: "Muy cariñosa y sociable. tiene todas sus vacunas al dia",
                status: "Disponible",
				image_url: "https://placedog.net/400"
			},
			{
				id: 2,
				name: "Milo",
				species: "Gato",
                race: "Siames",
				age: 1,
				gender: "Macho",
				description: "Tranquilo y curioso. con sus vacunas al dia y está castrado",
                status: "Disponible",
				image_url: "https://tugatos.com/wp-content/uploads/2025/01/WhatsApp-Image-2025-08-13-at-3.30.28-PM.jpeg"
			},
			{
				id: 3,
				name: "Rocky",
				species: "Perro",
                race: "Bulldog",
				age: 4,
				gender: "Macho",
				description: "Protector y juguetón.",
                status: "Disponible",
				image_url: "https://placedog.net/401"
			}
		]
	};
}
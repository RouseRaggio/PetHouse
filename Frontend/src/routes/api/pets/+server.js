import { json } from '@sveltejs/kit';

export async function GET({ params }) {
	// Aquí base real viejo armando, osea la lógica para
	//  obtener las mascotas desde la base de datos, eso es solo un ejemplo
	//  luego se reemplaza con la lógica real
	const id = params.id;

	const pets = [
		{
			id: 1,
			name: "Luna",
			specie: "Perro",
            raice: "Labrador",
			age: "2 años",
			gender: "Hembra",
			description: "Cariñosa y sociable.",
            status: "Disponible"// o "adoptado"
			,image_url: "https://placedog.net/400/300?id=1"
		}
	];
	const pet = pets.find(p => p.id === id);
	return json({ pet });
}
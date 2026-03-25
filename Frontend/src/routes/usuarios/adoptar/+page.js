export async function load({ url }) {
	const petId = url.searchParams.get('pet_id');

	console.log('pet_id recibido:', petId);

	if (!petId) {
		return { pet: null };
	}

	const res = await fetch(`http://localhost:8000/pets/${petId}`);
	const pet = await res.json();

	console.log('pet recibido:', pet);

	return { pet };
}

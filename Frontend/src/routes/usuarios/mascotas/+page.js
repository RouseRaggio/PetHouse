export async function load() {
	const res = await fetch('http://localhost:8001/pets');
	if (!res.ok) {
		return { pets: [] };
	}

	const pets = await res.json();
	return { pets };
}

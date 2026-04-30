const BASE_URL = 'http://localhost:8000/pets'; // ojo ahi cambia esto a la URL del backend

export async function getPets() {
	const res = await fetch(`${BASE_URL}/pets`);
	if (!res.ok) throw new Error("Error obteniendo mascotas");
	return res.json();
}

export async function createPet(petData) {
    const res = await fetch(`${BASE_URL}/pets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(petData)
    });
    if (!res.ok) throw new Error("Error creando mascota");
    return res.json();
}

export async function updatePet(id, petData) {
    const res = await fetch(`${BASE_URL}/pets/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(petData)
    });
    if (!res.ok) throw new Error("Error actualizando mascota");
    return res.json();
}

export async function deletePet(id) {
    const res = await fetch(`${BASE_URL}/pets/${id}`, {
        method: 'DELETE'
    });
    if (!res.ok) throw new Error("Error eliminando mascota");
    return res.json();
}


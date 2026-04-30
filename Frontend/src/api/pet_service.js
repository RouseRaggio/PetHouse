
import API_URL, { getAuthHeaders } from './api';
// =========================
// CREATE PET
// =========================
export const createPet = async (formData) => {
  try {
    const token = localStorage.getItem('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    const response = await fetch(`${API_URL}/pets`, {
      method: "POST",
      headers: headers,
      body: formData,  // FormData ya incluye el Content-Type
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error al crear mascota");
    }

    return await response.json();
  } catch (error) {
    console.error("createPet:", error);
    throw error;
  }
};

// =========================
// GET ALL PETS
// =========================
export const getPets = async () => {
  try {
    const response = await fetch(`${API_URL}/pets`);

    if (!response.ok) {
      throw new Error("Error al obtener mascotas");
    }

    return await response.json();
  } catch (error) {
    console.error("getPets:", error);
    throw error;
  }
};

// =========================
// GET ONE PET
// =========================
export const getPet = async (id) => {
  try {
    const response = await fetch(`${API_URL}/pets/${id}`);

    if (!response.ok) {
      throw new Error("Mascota no encontrada");
    }

    return await response.json();
  } catch (error) {
    console.error("getPet:", error);
    throw error;
  }
};

// =========================
// UPDATE PET
// =========================
export const updatePet = async (id, data) => {
  try {
    const response = await fetch(`${API_URL}/pets/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders()
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error al actualizar mascota");
    }

    return await response.json();
  } catch (error) {
    console.error("updatePet:", error);
    throw error;
  }
};

// =========================
// DELETE PET (SOFT DELETE)
// =========================
export const deletePet = async (id) => {
  try {
    const response = await fetch(`${API_URL}/pets/${id}`, {
      method: "DELETE",
      headers: getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error("Error al eliminar mascota");
    }

    return await response.json();
  } catch (error) {
    console.error("deletePet:", error);
    throw error;
  }
};

import API_URL, { getAuthHeaders } from './api';
// =========================
// CREATE ADOPTION
// =========================
export const createAdoption = async (data) => {
  try {
    const response = await fetch(`${API_URL}/adoptions`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error al crear adopción");
    }

    return await response.json();
  } catch (error) {
    console.error("createAdoption:", error);
    throw error;
  }
};

// =========================
// GET ALL
// =========================
export const getAdoptions = async () => {
  try {
    const response = await fetch(`${API_URL}/adoptions`);

    if (!response.ok) {
      throw new Error("Error al obtener adopciones");
    }

    return await response.json();
  } catch (error) {
    console.error("getAdoptions:", error);
    throw error;
  }
};

// =========================
// GET ONE
// =========================
export const getAdoption = async (id) => {
  try {
    const response = await fetch(`${API_URL}/adoptions/${id}`);

    if (!response.ok) {
      throw new Error("Adopción no encontrada");
    }

    return await response.json();
  } catch (error) {
    console.error("getAdoption:", error);
    throw error;
  }
};

// =========================
// CHANGE STATUS
// =========================
export const changeAdoptionStatus = async (id, status_id) => {
  try {
    const response = await fetch(`${API_URL}/adoptions/${id}/status`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status_id }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error al cambiar estado");
    }

    return await response.json();
  } catch (error) {
    console.error("changeAdoptionStatus:", error);
    throw error;
  }
};

// =========================
// DELETE (SOFT DELETE)
// =========================
export const deleteAdoption = async (id) => {
  try {
    const response = await fetch(`${API_URL}/adoptions/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Error al eliminar adopción");
    }

    return await response.json();
  } catch (error) {
    console.error("deleteAdoption:", error);
    throw error;
  }
};

export interface Pet {
  // Campos obligatorios
  id: number;
  publisher_id: number;
  name: string;
  species: string;
  created_at: string;

  // Campos opcionales
  race?: string | null;
  birth_date?: string | null;
  gender?: string | null;
  description?: string | null;
  image_url?: string | null;
  status?:
    | 'AVAILABLE'
    | 'ADOPTED'
    | 'RESERVED'
    | 'UNAVAILABLE'
    | 'PENDING_APPROVAL'
    | 'REJECTED'
    | null;
  modalidad?: 'sede' | 'hogar' | null;
  telefono_contacto?: string | null;
  adopter_name?: string | null;
  adopter_id?: number | null;
  publisher_name?: string | null;
}

export interface PetCreate {
  name: string;
  species: string;
  race?: string | null;
  birth_date?: string | null;
  gender?: string | null;
  description?: string | null;
  image_url?: string | null;
  modalidad?: 'sede' | 'hogar';
  telefono_contacto?: string | null;
}

export interface PetUpdate {
  name?: string | null;
  species?: string | null;
  race?: string | null;
  birth_date?: string | null;
  gender?: string | null;
  description?: string | null;
  image_url?: string | null;
  status?: string | null;
  modalidad?: string | null;
  telefono_contacto?: string | null;
}

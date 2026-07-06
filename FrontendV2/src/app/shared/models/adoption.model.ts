export interface AdoptionStatus {
  id: number;
  name: 'PENDING' | 'APPROVED' | 'REJECTED';
}

export interface AdoptionUser {
  id: number;
  name: string;
  last_name: string;
  email: string;
}

export interface Adoption {
  // Campos obligatorios
  id: number;
  pet_id: number;
  adoptante_id: number;
  status_id: number;
  fecha_solicitud: string;

  // Campos opcionales
  fecha_respuesta?: string | null;
  cedula_url?: string | null;
  recibo_url?: string | null;
  deleted_at?: string | null;

  // Relaciones (vienen del backend como objetos anidados)
  pet?: { id: number; name: string; image_url?: string | null };
  status?: AdoptionStatus;
  adoptante?: AdoptionUser;
}

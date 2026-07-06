export interface Role {
  id: number;
  name: string;
}

export interface User {
  // Campos obligatorios
  id: number;
  role_id: number;
  name: string;
  last_name: string;
  email: string;
  created_at: string;

  // Campos opcionales
  updated_at?: string | null;
  deleted_at?: string | null;
  is_active?: boolean;

  // Relación
  role?: Role;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

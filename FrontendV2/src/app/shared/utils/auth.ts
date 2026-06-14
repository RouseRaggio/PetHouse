import { Router } from '@angular/router';
import Swal from 'sweetalert2';

interface AuthUser {
  [key: string]: any;
}

/**
 * Verifica si el usuario está autenticado
 */
export function getCurrentUser(): AuthUser | null {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');

  if (!token || !userStr) return null;

  try {
    return JSON.parse(userStr);
  } catch {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return null;
  }
}

/**
 * Guarda la URL de destino antes de redirigir al login
 */
export function saveRedirectUrl(redirectUrl: string): void {
  localStorage.setItem('redirectAfterLogin', redirectUrl);
}

/**
 * Obtiene y limpia la URL de redirección guardada
 */
export function getAndClearRedirectUrl(): string | null {
  const redirectUrl = localStorage.getItem('redirectAfterLogin');
  if (redirectUrl) {
    localStorage.removeItem('redirectAfterLogin');
    return redirectUrl;
  }
  return null;
}

/**
 * Verifica autenticación y maneja redirección con mensaje.
 * Requiere el Router de Angular porque ya no hay $app/navigation de Svelte.
 */
export async function requireAuth(
  router: Router,
  currentUrl: string,
  message = 'Para realizar esta acción debe iniciar sesión',
): Promise<{ user: AuthUser }> {
  const user = getCurrentUser();

  if (!user) {
    saveRedirectUrl(currentUrl);

    await Swal.fire({
      title: '¡Acceso requerido!',
      text: message,
      icon: 'info',
      confirmButtonText: 'Iniciar Sesión',
    });

    router.navigate(['/login']);
    throw new Error('AUTH_REQUIRED');
  }

  return { user };
}

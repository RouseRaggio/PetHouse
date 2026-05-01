<script>
    import { onMount } from 'svelte';
    import { setAuth } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import Swal from 'sweetalert2';

    onMount(async () => {
        const url = new URL(window.location.href);
        const token = url.searchParams.get('token');
        const error = url.searchParams.get('error');

        if (error) {
            Swal.fire('Error', 'No se pudo iniciar sesión con Google', 'error');
            setTimeout(() => goto('/login'), 2000);
            return;
        }

        if (token) {
            try {
                // Obtener datos del usuario desde nuestro backend
                const response = await fetch('http://localhost:8000/api/auth/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const userData = await response.json();
                    setAuth(token, userData);
                    
                    Swal.fire({
                        title: 'Bienvenido',
                        text: `Hola ${userData.name}`,
                        icon: 'success',
                        timer: 1500,
                        showConfirmButton: false
                    });

                    // Redirigir al home después del mensaje
                    setTimeout(() => {
                        goto('/');
                    }, 1500);
                } else {
                    Swal.fire('Error', 'Token inválido', 'error');
                    setTimeout(() => goto('/login'), 2000);
                }
            } catch (err) {
                console.error('Error:', err);
                Swal.fire('Error', 'Error de conexión', 'error');
                setTimeout(() => goto('/login'), 2000);
            }
        } else {
            goto('/login');
        }
    });
</script>

<div class="d-flex flex-column justify-content-center align-items-center" style="min-height: 80vh;">
    <div class="spinner-border text-primary mb-3" role="status"></div>
    <p class="text-muted">Iniciando sesión con Google...</p>
</div>

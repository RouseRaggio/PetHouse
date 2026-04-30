<script>
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/Navbar.svelte';

	export let data;

	let pet = data?.pet || null;
	let loading = !pet;
	let cedulaFile = null;
	let reciboFile = null;
	let quiere_tracker = false;
	let acceptedTerms = false;
	let message = '';
	let success = false;

	const API = 'http://localhost:8000';

	onMount(() => {
		if (!pet) {
			const stored = localStorage.getItem('selectedPet');
			if (stored) pet = JSON.parse(stored);
		}
		loading = false;
	});

	function handleCedula(e) { cedulaFile = e.target.files[0]; }
	function handleRecibo(e) { reciboFile = e.target.files[0]; }

	async function submitSolicitud() {
		message = '';

		if (!cedulaFile || !reciboFile) {
			message = 'Debes subir tu cédula y recibo de servicios';
			success = false;
			return;
		}

		if (!acceptedTerms) {
			message = 'Debes aceptar los términos y el compromiso de adopción responsable';
			success = false;
			return;
		}

		const token = localStorage.getItem('token');
		const userStr = localStorage.getItem('user') || localStorage.getItem('pethouse_user');
		if (!token || !userStr) {
			message = 'Debes iniciar sesión para adoptar';
			success = false;
			return;
		}

		try {
			loading = true;

			const fd = new FormData();
			fd.append('pet_id', pet.id);
			fd.append('quiere_tracker', quiere_tracker);
			fd.append('cedula', cedulaFile);
			fd.append('recibo', reciboFile);

			const res = await fetch(`${API}/adoptions/`, {
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${token}`
				},
				body: fd
			});

			const dataRes = await res.json();

			if (res.ok) {
				message = 'Solicitud enviada correctamente';
				success = true;
				cedulaFile = null;
				reciboFile = null;
				quiere_tracker = false;
				localStorage.removeItem('selectedPet');
				// Opcional: redirigir a la pagina principal después de un tiempo
				setTimeout(() => {
					window.location.href = '/usuarios/mascotas';
				}, 2000);
				
			} else {
				message = dataRes.detail || dataRes.message || 'No se pudo enviar la solicitud';
				success = false;
			}
		} catch (e) {
			message = 'Error de conexión con el servidor';
			success = false;
			console.error(e);
		} finally {
			loading = false;
		}
	}
</script>

<Navbar />
<div class="container mt-5">
	<div class="row justify-content-center">
		<div class="col-md-8">
			{#if loading}
				<div class="text-center py-5">
					<div class="spinner-border text-primary" role="status"></div>
				</div>
			{:else if !pet}
				<div class="alert alert-warning text-center">
					No se seleccionó ninguna mascota.
					<a href="/" class="alert-link">Volver al catálogo</a>
				</div>
			{:else}
				<div class="card shadow">
					<div class="card-header bg-primary text-white">
						<h4 class="mb-0">Solicitud de Adopción</h4>
					</div>

					<div class="card-body">
						{#if message}
							<div class="alert {success ? 'alert-success' : 'alert-danger'}">{message}</div>
						{/if}

						<!-- Info mascota -->
						<div class="d-flex align-items-center gap-3 p-3 mb-4 border rounded bg-light">
							{#if pet.image_url}
								<img src={pet.image_url} alt={pet.name} class="rounded"
									style="width:80px; height:80px; object-fit:cover;" />
							{/if}
							<div>
								<h5 class="mb-0 fw-bold">{pet.name}</h5>
								<p class="text-muted mb-0">
									{pet.age ?? '?'} meses · {pet.species ?? ''} · {pet.gender ?? ''}
								</p>
								{#if pet.race}<small class="text-muted">{pet.race}</small>{/if}
							</div>
						</div>

						<div class="row">
							<div class="col-md-6 mb-3">
								<label class="form-label fw-semibold" for="cedula">Cédula de identidad *</label>
								<input id="cedula" type="file" class="form-control"
									accept="image/*,application/pdf" on:change={handleCedula} />
							</div>
							<div class="col-md-6 mb-3">
								<label class="form-label fw-semibold" for="recibo">Recibo de servicios *</label>
								<input id="recibo" type="file" class="form-control"
									accept="image/*,application/pdf" on:change={handleRecibo} />
							</div>
							<div class="col-12 mb-4">
								<div class="p-3 bg-light border rounded mb-4">
									<h6 class="fw-bold text-dark mb-3"><i class="bi bi-shield-check"></i> Requisitos Legales y Compromisos (Colombia)</h6>
									<div class="small text-muted">
										<p class="mb-2">De acuerdo con la <strong>Ley 1774 de 2016</strong> y la <strong>Ley 2054 de 2020</strong>, la adopción implica una responsabilidad legal sobre el bienestar animal. Al enviar esta solicitud, te comprometes a:</p>
										<ul class="mb-3">
											<li>Ser mayor de edad (+18 años) con identificación válida.</li>
											<li>Garantizar un espacio seguro y digno para el animal.</li>
											<li>Cubrir gastos de alimentación, salud (vacunas, desparasitación) y bienestar.</li>
											<li><strong>Esterilización obligatoria</strong> (si no lo está ya).</li>
											<li>No abandonar, maltratar ni ceder el animal a terceros sin aviso.</li>
											<li>Permitir visitas de seguimiento por parte de PetHouse.</li>
										</ul>
									</div>
									<div class="form-check">
										<input class="form-check-input" type="checkbox" id="terms" bind:checked={acceptedTerms} required />
										<label class="form-check-label fw-bold text-primary" for="terms">
											Acepto los términos del Contrato de Adopción Responsable
										</label>
									</div>
								</div>

								<div class="form-check form-switch p-3 border rounded">
									<input class="form-check-input ms-0 me-2" type="checkbox" id="quiere_tracker"
										bind:checked={quiere_tracker} />
									<label class="form-check-label fw-bold" for="quiere_tracker">
										¿Deseas incluir un tracker GPS para tu mascota?
									</label>
									<p class="x-small text-muted mb-0 ms-4">Recomendado para mayor seguridad en zonas abiertas.</p>
								</div>
							</div>
						</div>

						<button class="btn btn-primary w-100 py-3 fw-bold shadow-sm" on:click={submitSolicitud}
							disabled={loading || success || !acceptedTerms}>
							{loading ? 'Procesando Solicitud...' : 'Confirmar y Enviar Solicitud Legal'}
						</button>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
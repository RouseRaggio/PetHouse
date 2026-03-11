<script>
	import Navbar from '$lib/components/Navbar.svelte';

	let name = '';
	let species = '';
	let race = '';
	let birth_date = '';
	let gender = '';
	let description = '';
	let imageFile = null;

	let preview = '';
	let message = '';
	let success = false;

	function handleImage(e) {
		imageFile = e.target.files[0];

		if (imageFile) {
			preview = URL.createObjectURL(imageFile);
		}
	}

	async function publishPet() {
		if (!name || !species) {
			message = 'Debes completar los campos obligatorios';
			success = false;
			return;
		}

		const formData = new FormData();

		formData.append('name', name);
		formData.append('species', species);
		formData.append('race', race);
		formData.append('birth_date', birth_date);
		formData.append('gender', gender);
		formData.append('description', description);

		if (imageFile) {
			formData.append('image', imageFile);
		}

		const res = await fetch('http://localhost:8000/pets', {
			method: 'POST',
			body: formData
		});

		const data = await res.json();

		message = data.message;
		success = true;

		name = '';
		species = '';
		race = '';
		birth_date = '';
		gender = '';
		description = '';
		imageFile = null;
		preview = '';
	}
</script>

<Navbar />
<div class="container mt-5">
	<div class="row justify-content-center">
		<div class="col-md-8">
			<div class="card shadow">
				<div class="card-header bg-primary text-white">
					<h4 class="mb-0">Publicar Mascota</h4>
				</div>

				<div class="card-body">
					{#if message}
						<div class="alert {success ? 'alert-success' : 'alert-danger'}">
							{message}
						</div>
					{/if}

					<div class="row">
						<div class="col-md-6 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Nombre *</label>
							<input class="form-control" bind:value={name} />
						</div>

						<div class="col-md-6 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Especie *</label>
							<select class="form-select" bind:value={species}>
								<option value="">Seleccionar</option>
								<option value="perro">Perro</option>
								<option value="gato">Gato</option>
							</select>
						</div>

						<div class="col-md-6 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Raza</label>
							<input class="form-control" bind:value={race} />
						</div>

						<div class="col-md-6 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Fecha de nacimiento</label>
							<input type="date" class="form-control" bind:value={birth_date} />
						</div>

						<div class="col-md-6 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Género</label>
							<select class="form-select" bind:value={gender}>
								<option value="">Seleccionar</option>
								<option value="macho">Macho</option>
								<option value="hembra">Hembra</option>
							</select>
						</div>

						<div class="col-md-6 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Subir imagen</label>
							<input type="file" class="form-control" accept="image/*" on:change={handleImage} />
						</div>

						<div class="col-12 mb-3">
							<!-- svelte-ignore a11y_label_has_associated_control -->
							<label class="form-label">Descripción</label>
							<textarea class="form-control" rows="3" bind:value={description}></textarea>
						</div>
					</div>

					<button class="btn btn-primary w-100" on:click={publishPet}> Publicar mascota </button>

					{#if preview}
						<div class="text-center mt-4">
							<p class="text-muted">Vista previa</p>
							<img src={preview} class="img-fluid rounded" style="max-height:200px;" alt="" />
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
</div>

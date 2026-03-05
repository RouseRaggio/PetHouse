<script>
	export let data;
	const pet = data.pet;
</script>

<section class="container py-5">
	<h1 class="mb-4">{pet.name}</h1>

	<div class="row">
		<div class="col-md-4">
			<img src={pet.image_url} class="img-fluid rounded shadow" alt={pet.name} />
		</div>

		<div class="col-md-8">
			<div class="detail-box p-4 shadow-sm rounded">
				<p><strong>Edad:</strong> {pet.age} años</p>
				<p><strong>Sexo:</strong> {pet.gender} ni idea</p>
				<p><strong>Vacunado:</strong> {pet.vaccinated}</p>
			</div>
		</div>
	</div>
</section>

<style>
	.detail-box {
		background: #f8f9fa;
	}
</style>

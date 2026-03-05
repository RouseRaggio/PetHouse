<script>
	import { createEventDispatcher } from "svelte";
    import '../../app.css';
	export let pet;
	const dispatch = createEventDispatcher();
</script>

<div class="card shadow-sm h-100 small-card">
	<img src={pet.image_url} class="card-img-top" alt={pet.name} />

	<div class="card-body text-center">
		<h5 class="fw-bold">{pet.name}</h5>
		<p class="text-muted">{pet.age} meses</p>

		<button
			class="btn btn-outline-primary btn-sm"
			on:click={() => dispatch("view")}
		>
			Ver detalles
		</button>
	</div>
</div>
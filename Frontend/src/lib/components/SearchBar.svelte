<script>
	export let search = "";
</script>

<div class="row justify-content-center mt-4">
	<div class="col-md-6">
		<input
			type="text"
			class="form-control"
			placeholder="Buscar por nombre o especie..."
			bind:value={search}
		/>
	</div>
</div>
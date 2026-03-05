<script>
	export let title = 'Reporte';
	export let src = '';
	export let height = '400px';
</script>

<div class="card mt-5 p-3">
	<h5>{title}</h5>

	<!-- svelte-ignore a11y_missing_attribute -->
	<iframe width="100%" {height} {src} frameborder="0" allowFullScreen="true"></iframe>
</div>

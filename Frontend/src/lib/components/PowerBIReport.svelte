<script>
	export let title = 'Reporte';
	export let src = '';
	export let height = '400px';
</script>

<div class="card mt-5 p-3">
	<h5>{title}</h5>

	<iframe {title} width="100%" {height} {src} frameborder="0" allowFullScreen></iframe>
</div>

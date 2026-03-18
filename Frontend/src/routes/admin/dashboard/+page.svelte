<script>
    import PowerBIReport from "$lib/components/PowerBIReport.svelte";
    import AdminNavbar from "$lib/components/AdminNavbar.svelte";
</script>

<AdminNavbar />
<h1 class="text-center mt-3">Reporte de mascotas</h1>

<section class="container mt-0 mb-0">
        <PowerBIReport
            title=""
            src="https://app.powerbi.com/view?r=eyJrIjoiZjU0ZWNhMjEtYjIyMy00MTllLTlmZmYtOTNhZjI0ZjA4MjY0IiwidCI6IjFlOWFhYmU4LTY3ZjgtNGYxYy1hMzI5LWE3NTRlOTI0OTlhZSIsImMiOjR9"
            height="600px"
            width="100%"
        />
</section>

<h1 class="text-center mt-3 mb-0">Reporte de Usuarios</h1>

<div>
    <section class="container mt-0">
        <PowerBIReport
            title=""
            src="AQUI_VA_EL_SEGUNDO_LINK_DE_POWERBI"
            height="600px"
            width="100%"
        />
    </section>
</div>
<style>
    h1 {
        font-weight: bold;
        font-size: 3rem;
    }
</style>
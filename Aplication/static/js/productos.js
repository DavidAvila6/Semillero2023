document.addEventListener('DOMContentLoaded', function () {
    const ubicacionSelect = document.getElementById('{{ form.ubicacion.id_for_label }}');
    const otraUbicacionGroup = document.getElementById('otra-ubicacion-group');

    function toggleOtraUbicacion() {
        otraUbicacionGroup.style.display = ubicacionSelect.value === 'OTRO' ? 'block' : 'none';
    }

    ubicacionSelect.addEventListener('change', toggleOtraUbicacion);

    // Al cargar la página, también verifica la condición inicial
    toggleOtraUbicacion();
});
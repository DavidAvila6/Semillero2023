document.addEventListener('DOMContentLoaded', function () {
    // Obtener el contenedor de la card y la tabla
    const cardContainer = document.querySelector('.movimientos-preview-card');
    const tableContainer = document.querySelector('.movimientos-table-container');

    // Obtener la URL de la vista que devuelve los movimientos (asegúrate de tener la URL correcta)
    const url = '{% url "lista_movimientos" %}';

    // Función para cargar y mostrar la tabla de movimientos en la card
    function loadMovimientosTable() {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                tableContainer.innerHTML = data;
            })
            .catch(error => {
                console.error('Error al cargar la tabla de movimientos:', error);
            });
    }

    // Cargar la tabla al cargar la página
    loadMovimientosTable();
});

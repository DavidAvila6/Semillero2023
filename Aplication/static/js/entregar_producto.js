// entregar_producto.js
function checkEnter(event, nextFieldId) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById(nextFieldId).focus();
    }
}

function validateForm() {
    var usuario_id = document.getElementById('usuario_id').value.trim();
    var producto_id = document.getElementById('producto_id').value.trim();
    
    if (usuario_id === "") {
        alert("Por favor, complete el campo del usuario antes de continuar.");
        return false;
    }
    
    if (producto_id === "") {
        alert("Por favor, seleccione un producto antes de enviar el formulario.");
        return false;
    }
    
    return true;
}

function updateAvailability() {
    var productoSelect = document.getElementById('producto_id');
    var selectedProductId = productoSelect.value;

    if (selectedProductId !== "") {
        document.getElementById('comentario-input').style.display = 'block';
        document.getElementById('submit-button').style.display = 'block';
    } else {
        document.getElementById('comentario-input').style.display = 'none';
        document.getElementById('submit-button').style.display = 'none';
    }
}

document.getElementById('usuario_id').addEventListener('input', function() {
    var usuario_id = this.value.trim();
    if (usuario_id !== "") {
        document.getElementById('producto-input').style.display = 'block';
    }
});

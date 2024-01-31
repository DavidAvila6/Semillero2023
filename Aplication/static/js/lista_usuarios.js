document.addEventListener("DOMContentLoaded", function () {
    const carreraSelect = document.getElementById('carrera-select');
    const searchInput = document.getElementById('search-input');
    const userCards = document.querySelectorAll('.user-card');

    carreraSelect.addEventListener('change', filterUsers);
    searchInput.addEventListener('input', filterUsers);

    function filterUsers() {
        const selectedCarrera = carreraSelect.value.toLowerCase();
        const searchString = searchInput.value.toLowerCase();

        userCards.forEach(card => {
            const cardCarrera = card.getAttribute('data-carrera').toLowerCase();
            const cardName = card.querySelector('a').innerText.toLowerCase();

            const carreraCondition = selectedCarrera === 'todos' || cardCarrera === selectedCarrera;
            const searchCondition = cardName.includes(searchString);

            if (carreraCondition && searchCondition) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
});

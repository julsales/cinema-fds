const ratingForm = document.getElementById('rating-form');
const stars = document.querySelectorAll('.star-rating input[type="radio"]');
const starLabels = document.querySelectorAll('.star-rating label');

stars.forEach(star => {
    star.addEventListener('change', () => {
        stars.forEach(s => s.checked = false);
        star.checked = true;
    });
});

ratingForm.addEventListener('submit', e => {
    e.preventDefault();
    const selectedStar = document.querySelector('.star-rating input[type="radio"]:checked');
    if (selectedStar) {
        const ratingValue = selectedStar.value;
        // Aqui você pode enviar o valor da avaliação para o backend usando AJAX ou um formulário normal
        alert('Avaliação enviada: ' + ratingValue + ' estrela(s)');
    } else {
        alert('Por favor, selecione uma avaliação.');
    }
});

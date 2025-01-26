document.addEventListener('DOMContentLoaded', () => {
    const errorTitles = document.querySelectorAll('.error-title');
    const toggleAllButton = document.getElementById('toggleAll');
    const errorDetails = document.querySelectorAll('.error-details');

    function toggleDetails(details, show) {
        details.classList.toggle('show', show);
    }

    errorTitles.forEach(title => {
        title.addEventListener('click', () => {
            const details = title.nextElementSibling;
            const isVisible = details.classList.contains('show');

            // Oculta todos os detalhes e remove a classe active de todos os títulos
            errorDetails.forEach(detail => toggleDetails(detail, false));
            errorTitles.forEach(t => t.classList.remove('active'));

            // Mostra ou oculta o detalhe correspondente ao título clicado
            if (!isVisible) {
                toggleDetails(details, true);
                title.classList.add('active');
            }
        });
    });

    if (toggleAllButton) {
        toggleAllButton.addEventListener('click', () => {
            const allVisible = Array.from(errorDetails).every(detail => detail.classList.contains('show'));

            // Alterna a visibilidade de todos os detalhes e altera o texto do botão
            errorDetails.forEach(detail => toggleDetails(detail, !allVisible));
            errorTitles.forEach(title => title.classList.toggle('active', !allVisible));
            toggleAllButton.textContent = allVisible ? 'Show All' : 'Hide All';
        });
    } else {
        console.warn('Toggle All button not found.');
    }
});

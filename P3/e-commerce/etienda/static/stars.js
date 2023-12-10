function generateStarsHTML(rating) {
    const maxStars = 5;
    let starsHTML = '';
    const roundedRating = Math.round(rating);
    for (let i = 0; i < maxStars; i++) {
        if (i < roundedRating) {
            starsHTML += '<span class="fa fa-star checked"></span>';
        } else {
            starsHTML += '<span class="fa fa-star not_checked"></span>';
        }
    }
    return starsHTML;
}

function updateRating(elemento, newRating){

    const productId = elemento.getAttribute('data-product-id');
    fetch(`http://localhost:8000/etienda/api/modifyrating/${productId}/${newRating}`, {
            method: 'PUT',  
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}


document.addEventListener('DOMContentLoaded', () => {
    const span_para_estrellas = document.querySelectorAll('span.sp');

    span_para_estrellas.forEach((ele) => {
        const productId = ele.dataset.productId;

        fetch(`http://localhost:8000/etienda/api/getproductbyid/${productId}`)
            .then(res => res.json())
            .then(res => {
                const rating = res.rating.rate;
                ele.innerHTML = generateStarsHTML(rating);

                const stars = ele.querySelectorAll('.fa-star');
                stars.forEach((star, index) => {
                    star.addEventListener('click', () => {

                        // Actualizar la visualización de las estrellas
                        stars.forEach((s, i) => {
                            if (i <= index) {
                                s.classList.add('checked');
                                s.classList.remove('not_checked');
                            } else {
                                s.classList.add('not_checked');
                                s.classList.remove('checked');
                            }
                        });

                        // Enviar la nueva calificación a la API
                        updateRating(ele, index+1);
                    });
                });
            })
            .catch(error => alert(`Hay un ${error}.`));
    });
});

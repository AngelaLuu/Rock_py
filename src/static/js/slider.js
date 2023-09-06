(function(){
    // Selecciona todos los elementos con la clase 'testimony__body' y los almacena en un array.
    const sliders = [...document.querySelectorAll('.testimony__body')];
    // Selecciona los botones de navegación siguiente y anterior.
    const buttonNext = document.querySelector('#next');
    const buttonBefore = document.querySelector('#before');
    let value;   // Variable para rastrear la posición actual del testimonio.

    // Agrega un evento click al botón "Siguiente".
    buttonNext.addEventListener('click', ()=>{
        changePosition(1);
    });

    // Agrega un evento click al botón "Anterior".
    buttonBefore.addEventListener('click', ()=>{
        changePosition(-1);
    });

    // Función para cambiar la posición del testimonio.
    const changePosition = (add)=>{
        // Obtiene el valor actual del atributo 'data-id' del testimonio que se está mostrando.
        const currentTestimony = document.querySelector('.testimony__body--show').dataset.id;
        // Convierte el valor actual a un número.
        value = Number(currentTestimony);
        // Incrementa o decrementa el valor según la dirección de la navegación.

        value+= add;

        // Elimina la clase 'testimony__body--show' del testimonio actual.
        sliders[Number(currentTestimony)-1].classList.remove('testimony__body--show');
        // Verifica si se llegó al final o al principio del carrusel.
        if(value === sliders.length+1 || value === 0){
            // Si es el final, regresa al primer testimonio. Si es el principio, avanza al último testimonio.
            value = value === 0 ? sliders.length  : 1;
        }
        // Agrega la clase 'testimony__body--show' al testimonio actualizado para mostrarlo.
        sliders[value-1].classList.add('testimony__body--show');
    }
})();

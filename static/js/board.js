// if (document.documentElement.clientWidth < document.documentElement.scrollWidth) {
//     const prof = document.getElementById("userprofile")
//     prof.classList.add("pb-2")
// } else {
//     if (prof.classList.contains("pb-2")) {
//         prof.classList.remove("pb-2")
//     }
// }

const cards = document.querySelectorAll('.drag[draggable="true"]');
const dropzones = document.querySelectorAll('.dropzone');

cards.forEach((card) => {
    card.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text/plain', event.target.id);
    });
});

dropzones.forEach((dropzone) => {
    dropzone.addEventListener('dragover', (event) => {
        event.preventDefault();
    });

    dropzone.addEventListener('drop', (event) => {
        event.preventDefault();
        const card_id = event.dataTransfer.getData('text/plain');
        const droppedElement = document.getElementById(card_id);
        const before = dropzone.querySelector("#newcard")
        const col_id = dropzone.id
        dropzone.insertBefore(droppedElement, before);

        // Send a POST request to the server when a card is dropped
        fetch(`/update-position`, {
            method: 'POST',
            body: new URLSearchParams({
                col_id: col_id,
                card_id: card_id
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        })
    });
});
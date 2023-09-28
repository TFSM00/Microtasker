if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
    document.getElementById('color-theme').setAttribute('class', "bi bi-moon-stars-fill")
  } else {
    document.getElementById('color-theme').setAttribute('class', "bi bi-brightness-high-fill")
  }
//   document.getElementById('btnSwitch').addEventListener('click',()=>{
//   if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
//       document.documentElement.setAttribute('data-bs-theme','light')
//       document.getElementById('color-theme').setAttribute('class', "bi bi-brightness-high-fill")

//   }
//   else {
//       document.documentElement.setAttribute('data-bs-theme','dark')
//       document.getElementById('color-theme').setAttribute('class', "bi bi-moon-stars-fill")
//   }
// })

// Change dropdown button color
// const dropdown = document.getElementById('dropdown-1');
// dropdown.addEventListener('click', function() {
//     const currentAriaExpanded = dropdown.getAttribute("aria-expanded") === 'true';
//     if (currentAriaExpanded) {
//         dropdown.classList.add('active');
//     } else {
//         dropdown.classList.remove('active');
//     }
// });

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne trimiterea formularului

    // Logica pentru verificarea autentificării ar trebui adăugată aici
    // De exemplu, trimiterea datelor la un server și verificarea răspunsului

    // Dacă autentificarea este reușită, redirecționează către pagina de home
    window.location.href = 'home.html';
});

document.getElementById('createAccountForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne trimiterea formularului

    // Logica pentru crearea contului ar trebui adăugată aici
    // De exemplu, trimiterea datelor la un server și verificarea răspunsului

    // Dacă crearea contului este reușită, redirecționează către pagina de home
    window.location.href = 'home.html';
});

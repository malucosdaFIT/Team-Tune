document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;

    // Enviar o email para o servidor (usando AJAX ou Fetch API)
    fetch('/cadastrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email})
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Erro ao cadastrar e-mail');
        }
        return response.json();
    })
    .then(function(data) {
        alert('E-mail cadastrado com sucesso!');
    })
    .catch(function(error) {
        alert(error.message);
    });
});

document.getElementById('form-email').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    fetch('/cadastrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem);

        // Redirecionar para a página de feedback
        window.location.href = '/feedback';
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
});

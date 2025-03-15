

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('cadastroForm');
  // @ts-ignore
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    // @ts-ignore
    const formData = new FormData(form);

    fetch('/cadastrar', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then((response) => response.json())
    .then((data) => {
         alert(data.message);
        if (data.message === 'Cadastro realizado com sucesso!') {
            // @ts-ignore
            form.reset();
        }  
      })

        .catch(error => {
            console.error('Erro', error);
            
        });
  });
});

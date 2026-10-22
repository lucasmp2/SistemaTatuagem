// Restringe o cadastro de funcionários à administração do estúdio.
if (protegerPagina()) {
  if (lerTipoToken() !== 'admin') window.location.replace('dashboard.html')
  montarNavegacao('cadastro.html')
}

const formCadastro = document.getElementById('form-cadastro')
const mensagemCadastro = document.getElementById('mensagem')

formCadastro.addEventListener('submit', async evento => {
  evento.preventDefault()
  const botao = formCadastro.querySelector('button[type="submit"]')
  botao.disabled = true
  try {
    const resposta = await fetchAutenticado(`${API}/usuarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome: document.getElementById('nome').value, email: document.getElementById('email').value, senha: document.getElementById('senha').value })
    })
    await jsonDaResposta(resposta)
    mostrarMensagem(mensagemCadastro, 'Funcionário cadastrado.', true)
    formCadastro.reset()
  } catch (erro) {
    mostrarMensagem(mensagemCadastro, erro.message)
  } finally {
    botao.disabled = false
  }
})
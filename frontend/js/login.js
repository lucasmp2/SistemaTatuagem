// Autentica a equipe e armazena o token emitido pela API.
const formLogin = document.getElementById('form-login')
const mensagemLogin = document.getElementById('mensagem')

formLogin.addEventListener('submit', async evento => {
  evento.preventDefault()
  const botao = formLogin.querySelector('button[type="submit"]')
  botao.disabled = true
  try {
    const resposta = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: document.getElementById('email').value, senha: document.getElementById('senha').value })
    })
    const dados = await jsonDaResposta(resposta)
    localStorage.setItem('token', dados.access_token)
    window.location.assign('dashboard.html')
  } catch (erro) {
    mostrarMensagem(mensagemLogin, erro.message)
  } finally {
    botao.disabled = false
  }
})
// Monta navegação comum e oferece utilitários para as telas internas.
const rotasNavegacao = [
  ['Painel', 'dashboard.html'],
  ['Clientes', 'clientes.html'],
  ['Tatuadores', 'tatuadores.html'],
  ['Agendamentos', 'agendamentos.html'],
  ['Senioridade', 'senioridade.html'],
  ['Estilos', 'estilos.html']
]

function escaparHtml(valor) {
  return String(valor ?? '').replace(/[&<>"']/g, caractere => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[caractere])
}

function mostrarMensagem(elemento, mensagem, sucesso = false) {
  elemento.textContent = mensagem
  elemento.classList.toggle('success', sucesso)
}

function mostrarErroApi(erro) {
  return erro.detail || erro.erro || 'Não foi possível concluir a operação.'
}

async function jsonDaResposta(resposta) {
  const dados = await resposta.json().catch(() => ({}))
  if (!resposta.ok) throw new Error(mostrarErroApi(dados))
  return dados
}

function montarNavegacao(paginaAtual) {
  const raiz = document.getElementById('nav-root')
  if (!raiz) return
  const links = rotasNavegacao.map(([nome, destino]) =>
    `<a href="${destino}" ${destino === paginaAtual ? 'aria-current="page"' : ''}>${nome}</a>`
  ).join('')
  const cadastro = lerTipoToken() === 'admin' ? '<a href="cadastro.html">Novo funcionário</a>' : ''
  raiz.innerHTML = `<header class="site-header"><a class="brand" href="dashboard.html"><span class="brand-mark">E</span><span>ESTÚDIO / TATUAGEM</span></a><nav class="site-nav" aria-label="Navegação principal">${links}${cadastro}<button type="button" data-sair>Sair</button></nav></header>`
  raiz.querySelector('[data-sair]').addEventListener('click', sair)
}

function confirmarExclusao(rotulo) {
  return window.confirm(`Excluir ${rotulo}? Esta ação não pode ser desfeita.`)
}

function dataLocalHoje() {
  const agora = new Date()
  const local = new Date(agora.getTime() - agora.getTimezoneOffset() * 60000)
  return local.toISOString().slice(0, 10)
}
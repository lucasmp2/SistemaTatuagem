// Funções comuns para login, autorização das páginas e chamadas autenticadas.
const API = window.location.protocol === 'file:'
  ? 'http://127.0.0.1:8000'
  : window.location.origin

function protegerPagina() {
  if (!localStorage.getItem('token')) {
    window.location.replace('login.html')
    return false
  }
  return true
}

async function fetchAutenticado(url, opcoes = {}) {
  const token = localStorage.getItem('token')
  const resposta = await fetch(url, {
    ...opcoes,
    headers: { ...opcoes.headers, Authorization: `Bearer ${token}` }
  })
  if (resposta.status === 401) {
    localStorage.removeItem('token')
    window.location.replace('login.html')
  }
  return resposta
}

function sair() {
  localStorage.removeItem('token')
  window.location.replace('login.html')
}

function lerTipoToken() {
  try {
    const payload = localStorage.getItem('token').split('.')[1]
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/'))).tipo
  } catch {
    return ''
  }
}
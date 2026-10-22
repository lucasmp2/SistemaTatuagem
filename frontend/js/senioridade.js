// Protege a tela e conecta o formulário ao CRUD de senioridades.
if (protegerPagina()) montarNavegacao('senioridade.html')

const formSenioridade = document.getElementById('form-senioridade')
const corpoSenioridade = document.getElementById('corpo-tabela')
const mensagemSenioridade = document.getElementById('mensagem')
const botaoSenioridade = document.getElementById('btn-submit')
let senioridadesCarregadas = []

async function listarSenioridades() {
  try {
    senioridadesCarregadas = await jsonDaResposta(await fetchAutenticado(`${API}/senioridade`))
    corpoSenioridade.innerHTML = senioridadesCarregadas.length ? senioridadesCarregadas.map(item => `
      <tr><td>${item.idsenioridade}</td><td>${escaparHtml(item.nome)}</td><td><div class="row-actions"><button class="button secondary small" data-editar="${item.idsenioridade}">Editar</button><button class="button danger small" data-excluir="${item.idsenioridade}">Excluir</button></div></td></tr>`).join('') : '<tr><td colspan="3" class="empty-state">Nenhum nível cadastrado.</td></tr>'
  } catch (erro) { mostrarMensagem(mensagemSenioridade, erro.message) }
}

formSenioridade.addEventListener('submit', async evento => {
  evento.preventDefault()
  const id = formSenioridade.dataset.idSenioridade
  try {
    await jsonDaResposta(await fetchAutenticado(`${API}/senioridade${id ? `/${id}` : ''}`, {
      method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome: document.getElementById('nome').value.trim() })
    }))
    limparFormularioSenioridade()
    mostrarMensagem(mensagemSenioridade, id ? 'Nível atualizado.' : 'Nível cadastrado.', true)
    await listarSenioridades()
  } catch (erro) { mostrarMensagem(mensagemSenioridade, erro.message) }
})

function limparFormularioSenioridade() {
  formSenioridade.reset()
  delete formSenioridade.dataset.idSenioridade
  botaoSenioridade.textContent = 'Adicionar nível'
  document.getElementById('btn-cancelar').hidden = true
}

corpoSenioridade.addEventListener('click', async evento => {
  const editar = evento.target.closest('[data-editar]')?.dataset.editar
  const excluir = evento.target.closest('[data-excluir]')?.dataset.excluir
  if (editar) {
    const item = senioridadesCarregadas.find(registro => String(registro.idsenioridade) === editar)
    document.getElementById('nome').value = item?.nome || ''
    formSenioridade.dataset.idSenioridade = editar
    botaoSenioridade.textContent = 'Salvar alterações'
    document.getElementById('btn-cancelar').hidden = false
  }
  if (excluir && confirmarExclusao('este nível') ) {
    try {
      await jsonDaResposta(await fetchAutenticado(`${API}/senioridade/${excluir}`, { method: 'DELETE' }))
      mostrarMensagem(mensagemSenioridade, 'Nível excluído.', true)
      await listarSenioridades()
    } catch (erro) { mostrarMensagem(mensagemSenioridade, erro.message) }
  }
})

document.getElementById('btn-cancelar').addEventListener('click', limparFormularioSenioridade)
listarSenioridades()
// Protege a tela e conecta o formulário ao CRUD de estilos.
if (protegerPagina()) montarNavegacao('estilos.html')

const formEstilo = document.getElementById('form-estilo')
const corpoEstilos = document.getElementById('corpo-tabela')
const mensagemEstilos = document.getElementById('mensagem')
const botaoEstilo = document.getElementById('btn-submit')
let estilosCarregados = []

async function listarEstilos() {
  try {
    estilosCarregados = await jsonDaResposta(await fetchAutenticado(`${API}/estilos`))
    corpoEstilos.innerHTML = estilosCarregados.length ? estilosCarregados.map(item => `
      <tr><td>${item.idestilo}</td><td>${escaparHtml(item.descricao)}</td><td><div class="row-actions"><button class="button secondary small" data-editar="${item.idestilo}">Editar</button><button class="button danger small" data-excluir="${item.idestilo}">Excluir</button></div></td></tr>`).join('') : '<tr><td colspan="3" class="empty-state">Nenhum estilo cadastrado.</td></tr>'
  } catch (erro) { mostrarMensagem(mensagemEstilos, erro.message) }
}

formEstilo.addEventListener('submit', async evento => {
  evento.preventDefault()
  const id = formEstilo.dataset.idEstilo
  try {
    await jsonDaResposta(await fetchAutenticado(`${API}/estilos${id ? `/${id}` : ''}`, {
      method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ descricao: document.getElementById('descricao').value.trim() })
    }))
    limparFormularioEstilo()
    mostrarMensagem(mensagemEstilos, id ? 'Estilo atualizado.' : 'Estilo cadastrado.', true)
    await listarEstilos()
  } catch (erro) { mostrarMensagem(mensagemEstilos, erro.message) }
})

function limparFormularioEstilo() {
  formEstilo.reset()
  delete formEstilo.dataset.idEstilo
  botaoEstilo.textContent = 'Adicionar estilo'
  document.getElementById('btn-cancelar').hidden = true
}

corpoEstilos.addEventListener('click', async evento => {
  const editar = evento.target.closest('[data-editar]')?.dataset.editar
  const excluir = evento.target.closest('[data-excluir]')?.dataset.excluir
  if (editar) {
    const item = estilosCarregados.find(registro => String(registro.idestilo) === editar)
    document.getElementById('descricao').value = item?.descricao || ''
    formEstilo.dataset.idEstilo = editar
    botaoEstilo.textContent = 'Salvar alterações'
    document.getElementById('btn-cancelar').hidden = false
  }
  if (excluir && confirmarExclusao('este estilo')) {
    try {
      await jsonDaResposta(await fetchAutenticado(`${API}/estilos/${excluir}`, { method: 'DELETE' }))
      mostrarMensagem(mensagemEstilos, 'Estilo excluído.', true)
      await listarEstilos()
    } catch (erro) { mostrarMensagem(mensagemEstilos, erro.message) }
  }
})

document.getElementById('btn-cancelar').addEventListener('click', limparFormularioEstilo)
listarEstilos()
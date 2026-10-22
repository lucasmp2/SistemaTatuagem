// Protege a tela e conecta tatuadores às senioridades e estilos.
if (protegerPagina()) montarNavegacao('tatuadores.html')

const formTatuador = document.getElementById('form-tatuador')
const corpoTatuadores = document.getElementById('corpo-tabela')
const mensagemTatuadores = document.getElementById('mensagem')
const botaoTatuador = document.getElementById('btn-submit')
let tatuadoresCarregados = []

async function carregarOpcoesTatuador() {
  try {
    const [senioridades, estilos] = await Promise.all([
      jsonDaResposta(await fetchAutenticado(`${API}/senioridade`)),
      jsonDaResposta(await fetchAutenticado(`${API}/estilos`))
    ])
    document.getElementById('idsenioridade').innerHTML = '<option value="">Selecione...</option>' + senioridades.map(item => `<option value="${item.idsenioridade}">${escaparHtml(item.nome)}</option>`).join('')
    document.getElementById('lista-estilos').innerHTML = estilos.map(item => `<label class="check-option"><input type="checkbox" value="${item.idestilo}" data-estilo><span>${escaparHtml(item.descricao)}</span></label>`).join('') || '<span class="loading">Cadastre um estilo para habilitar esta seleção.</span>'
  } catch (erro) { mostrarMensagem(mensagemTatuadores, erro.message) }
}

async function listarTatuadores() {
  try {
    tatuadoresCarregados = await jsonDaResposta(await fetchAutenticado(`${API}/tatuadores`))
    corpoTatuadores.innerHTML = tatuadoresCarregados.length ? tatuadoresCarregados.map(item => `
      <tr><td>${item.idtatuador}</td><td>${escaparHtml(item.nometatuador)}</td><td>${escaparHtml(item.cpf)}</td><td>${escaparHtml(item.email || '—')}</td>
      <td>${escaparHtml(item.telefone || '—')}</td><td>${escaparHtml(item.senioridade)}</td><td>${escaparHtml(item.estilos || '—')}</td>
      <td><div class="row-actions"><button class="button secondary small" data-editar="${item.idtatuador}">Editar</button><button class="button danger small" data-excluir="${item.idtatuador}">Excluir</button></div></td></tr>`).join('') : '<tr><td colspan="8" class="empty-state">Nenhum tatuador cadastrado.</td></tr>'
  } catch (erro) { mostrarMensagem(mensagemTatuadores, erro.message) }
}

formTatuador.addEventListener('submit', async evento => {
  evento.preventDefault()
  const id = formTatuador.dataset.idTatuador
  const dados = {
    nometatuador: document.getElementById('nometatuador').value.trim(), cpf: document.getElementById('cpf').value.trim(),
    email: document.getElementById('email').value.trim() || null, telefone: document.getElementById('telefone').value.trim() || null,
    datacontratacao: dataLocalHoje(), idsenioridade: Number(document.getElementById('idsenioridade').value)
  }
  const idsMarcados = [...document.querySelectorAll('[data-estilo]:checked')].map(campo => Number(campo.value))
  try {
    const resposta = await fetchAutenticado(`${API}/tatuadores${id ? `/${id}` : ''}`, {
      method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados)
    })
    const salvo = await jsonDaResposta(resposta)
    const idSalvo = id || salvo.idtatuador
    await jsonDaResposta(await fetchAutenticado(`${API}/tatuadores/${idSalvo}/estilos`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ idestilos: idsMarcados })
    }))
    limparFormularioTatuador()
    mostrarMensagem(mensagemTatuadores, id ? 'Tatuador atualizado.' : 'Tatuador cadastrado.', true)
    await listarTatuadores()
  } catch (erro) { mostrarMensagem(mensagemTatuadores, erro.message) }
})

async function preencherFormularioTatuador(id) {
  const item = tatuadoresCarregados.find(registro => String(registro.idtatuador) === id)
  if (!item) return
  for (const campo of ['nometatuador', 'cpf', 'email', 'telefone', 'idsenioridade']) document.getElementById(campo).value = item[campo] || ''
  document.querySelectorAll('[data-estilo]').forEach(campo => { campo.checked = false })
  try {
    const estilos = await jsonDaResposta(await fetchAutenticado(`${API}/tatuadores/${id}/estilos`))
    estilos.forEach(estilo => {
      const campo = document.querySelector(`[data-estilo][value="${estilo.idestilo}"]`)
      if (campo) campo.checked = true
    })
    formTatuador.dataset.idTatuador = id
    botaoTatuador.textContent = 'Salvar alterações'
    document.getElementById('btn-cancelar').hidden = false
    formTatuador.scrollIntoView({ behavior: 'smooth', block: 'center' })
  } catch (erro) { mostrarMensagem(mensagemTatuadores, erro.message) }
}

function limparFormularioTatuador() {
  formTatuador.reset()
  delete formTatuador.dataset.idTatuador
  botaoTatuador.textContent = 'Cadastrar tatuador'
  document.getElementById('btn-cancelar').hidden = true
}

corpoTatuadores.addEventListener('click', async evento => {
  const editar = evento.target.closest('[data-editar]')?.dataset.editar
  const excluir = evento.target.closest('[data-excluir]')?.dataset.excluir
  if (editar) await preencherFormularioTatuador(editar)
  if (excluir && confirmarExclusao('este tatuador')) {
    try {
      await jsonDaResposta(await fetchAutenticado(`${API}/tatuadores/${excluir}`, { method: 'DELETE' }))
      mostrarMensagem(mensagemTatuadores, 'Tatuador excluído.', true)
      await listarTatuadores()
    } catch (erro) { mostrarMensagem(mensagemTatuadores, erro.message) }
  }
})

document.getElementById('btn-cancelar').addEventListener('click', limparFormularioTatuador)
carregarOpcoesTatuador()
listarTatuadores()
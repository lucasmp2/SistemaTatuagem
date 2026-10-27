// Protege a tela e conecta os agendamentos aos clientes e tatuadores.
if (protegerPagina()) montarNavegacao('agendamentos.html')

const formAgendamento = document.getElementById('form-agendamento')
const corpoAgendamentos = document.getElementById('corpo-tabela')
const mensagemAgendamentos = document.getElementById('mensagem')
const botaoAgendamento = document.getElementById('btn-submit')
const blocoStatus = document.getElementById('bloco-status')
let agendamentosCarregados = []

async function carregarOpcoesAgendamento() {
  try {
    const [clientes, tatuadores] = await Promise.all([
      jsonDaResposta(await fetchAutenticado(`${API}/clientes`)),
      jsonDaResposta(await fetchAutenticado(`${API}/tatuadores`))
    ])
    document.getElementById('idcliente').innerHTML = '<option value="">Selecione...</option>' + clientes.map(item => `<option value="${item.idcliente}">${escaparHtml(item.nome)}</option>`).join('')
    document.getElementById('idtatuador').innerHTML = '<option value="">Selecione...</option>' + tatuadores.map(item => `<option value="${item.idtatuador}">${escaparHtml(item.nometatuador)}</option>`).join('')
  } catch (erro) { mostrarMensagem(mensagemAgendamentos, erro.message) }
}

async function listarAgendamentos() {
  try {
    agendamentosCarregados = await jsonDaResposta(await fetchAutenticado(`${API}/agendamentos`))
    corpoAgendamentos.innerHTML = agendamentosCarregados.length ? agendamentosCarregados.map(item => `
      <tr><td>${item.idagendamento}</td><td>${escaparHtml(item.cliente || 'Cliente removido')}</td><td>${escaparHtml(item.tatuador)}</td>
      <td>${escaparHtml(String(item.dataagendamento).slice(0, 10))}</td><td>${escaparHtml(String(item.horaagendamento).slice(0, 5))}</td>
      <td>${item.valortatuagem == null ? '—' : Number(item.valortatuagem).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
      <td><span class="status ${escaparHtml(item.status)}">${escaparHtml(item.status)}</span></td>
      <td>${item.desenhoaprovado ? `<a href="${API}/uploads/${encodeURIComponent(item.desenhoaprovado)}" target="_blank" rel="noreferrer"><img class="thumbnail" src="${API}/uploads/${encodeURIComponent(item.desenhoaprovado)}" alt="Desenho aprovado"></a>` : '—'}</td>
      <td><div class="row-actions"><button class="button secondary small" data-editar="${item.idagendamento}">Editar</button><button class="button danger small" data-excluir="${item.idagendamento}">Excluir</button></div></td></tr>`).join('') : '<tr><td colspan="9" class="empty-state">Nenhum agendamento cadastrado.</td></tr>'
  } catch (erro) { mostrarMensagem(mensagemAgendamentos, erro.message) }
}

formAgendamento.addEventListener('submit', async evento => {
  evento.preventDefault()
  const id = formAgendamento.dataset.idAgendamento
  const dados = {
    idcliente: Number(document.getElementById('idcliente').value), idtatuador: Number(document.getElementById('idtatuador').value),
    dataagendamento: document.getElementById('dataagendamento').value, horaagendamento: document.getElementById('horaagendamento').value,
    descricaotatuagem: document.getElementById('descricaotatuagem').value.trim() || null,
    valortatuagem: document.getElementById('valortatuagem').value ? Number(document.getElementById('valortatuagem').value) : null,
    status: document.getElementById('status').value || null
  }
  try {
    let idSalvo = id
    const resposta = await fetchAutenticado(`${API}/agendamentos${id ? `/${id}` : ''}`, {
      method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados)
    })
    const resultado = await jsonDaResposta(resposta)
    if (!id) idSalvo = resultado.idagendamento
    const arquivo = document.getElementById('desenho').files[0]
    if (arquivo) {
      const formularioArquivo = new FormData()
      formularioArquivo.append('arquivo', arquivo)
      await jsonDaResposta(await fetchAutenticado(`${API}/agendamentos/${idSalvo}/desenho`, { method: 'POST', body: formularioArquivo }))
    }
    limparFormularioAgendamento()
    mostrarMensagem(mensagemAgendamentos, id ? 'Agendamento atualizado.' : 'Sessão agendada.', true)
    await listarAgendamentos()
  } catch (erro) { mostrarMensagem(mensagemAgendamentos, erro.message) }
})

function preencherFormularioAgendamento(id) {
  const item = agendamentosCarregados.find(registro => String(registro.idagendamento) === id)
  if (!item) return
  document.getElementById('idcliente').value = item.idcliente
  document.getElementById('idtatuador').value = item.idtatuador
  document.getElementById('dataagendamento').value = String(item.dataagendamento).slice(0, 10)
  document.getElementById('horaagendamento').value = String(item.horaagendamento).slice(0, 5)
  document.getElementById('descricaotatuagem').value = item.descricaotatuagem || ''
  document.getElementById('valortatuagem').value = item.valortatuagem ?? ''
  document.getElementById('status').value = item.status
  blocoStatus.hidden = false
  formAgendamento.dataset.idAgendamento = id
  botaoAgendamento.textContent = 'Salvar alterações'
  document.getElementById('btn-cancelar').hidden = false
  formAgendamento.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

function limparFormularioAgendamento() {
  formAgendamento.reset()
  delete formAgendamento.dataset.idAgendamento
  blocoStatus.hidden = true
  botaoAgendamento.textContent = 'Agendar sessão'
  document.getElementById('btn-cancelar').hidden = true
}

corpoAgendamentos.addEventListener('click', async evento => {
  const editar = evento.target.closest('[data-editar]')?.dataset.editar
  const excluir = evento.target.closest('[data-excluir]')?.dataset.excluir
  if (editar) preencherFormularioAgendamento(editar)
  if (excluir && confirmarExclusao('este agendamento')) {
    try {
      await jsonDaResposta(await fetchAutenticado(`${API}/agendamentos/${excluir}`, { method: 'DELETE' }))
      mostrarMensagem(mensagemAgendamentos, 'Agendamento excluído.', true)
      await listarAgendamentos()
    } catch (erro) { mostrarMensagem(mensagemAgendamentos, erro.message) }
  }
})

document.getElementById('btn-cancelar').addEventListener('click', limparFormularioAgendamento)
carregarOpcoesAgendamento()
listarAgendamentos()
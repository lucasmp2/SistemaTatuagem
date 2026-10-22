// Protege a tela e conecta o formulário ao CRUD de clientes.
if (protegerPagina()) montarNavegacao('clientes.html')

const formCliente = document.getElementById('form-cliente')
const corpoClientes = document.getElementById('corpo-tabela')
const mensagemClientes = document.getElementById('mensagem')
const botaoCliente = document.getElementById('btn-submit')
let clientesCarregados = []

async function listarClientes() {
  try {
    const resposta = await fetchAutenticado(`${API}/clientes`)
    clientesCarregados = await jsonDaResposta(resposta)
    corpoClientes.innerHTML = clientesCarregados.length ? clientesCarregados.map(cliente => `
      <tr><td>${cliente.idcliente}</td><td>${escaparHtml(cliente.nome)}</td><td>${escaparHtml(cliente.cpf)}</td>
      <td>${escaparHtml(cliente.telefone || '—')}</td><td>${escaparHtml(cliente.cidade || '—')}</td><td>${escaparHtml(cliente.uf || '—')}</td>
      <td><div class="row-actions"><button class="button secondary small" data-editar="${cliente.idcliente}">Editar</button><button class="button danger small" data-excluir="${cliente.idcliente}">Excluir</button></div></td></tr>`).join('') : '<tr><td colspan="7" class="empty-state">Nenhum cliente cadastrado.</td></tr>'
  } catch (erro) { mostrarMensagem(mensagemClientes, erro.message) }
}

formCliente.addEventListener('submit', async evento => {
  evento.preventDefault()
  const id = formCliente.dataset.idCliente
  const dados = {
    nome: document.getElementById('nome').value.trim(), cpf: document.getElementById('cpf').value.trim(),
    telefone: document.getElementById('telefone').value.trim() || null, datacadastro: dataLocalHoje(),
    cidade: document.getElementById('cidade').value.trim() || null, uf: document.getElementById('uf').value.trim().toUpperCase() || null
  }
  try {
    const resposta = await fetchAutenticado(`${API}/clientes${id ? `/${id}` : ''}`, {
      method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados)
    })
    await jsonDaResposta(resposta)
    limparFormularioCliente()
    mostrarMensagem(mensagemClientes, id ? 'Cliente atualizado.' : 'Cliente cadastrado.', true)
    await listarClientes()
  } catch (erro) { mostrarMensagem(mensagemClientes, erro.message) }
})

function limparFormularioCliente() {
  formCliente.reset()
  delete formCliente.dataset.idCliente
  botaoCliente.textContent = 'Cadastrar cliente'
  document.getElementById('btn-cancelar').hidden = true
}

corpoClientes.addEventListener('click', async evento => {
  const idEditar = evento.target.closest('[data-editar]')?.dataset.editar
  const idExcluir = evento.target.closest('[data-excluir]')?.dataset.excluir
  if (idEditar) {
    const cliente = clientesCarregados.find(item => String(item.idcliente) === idEditar)
    if (!cliente) return
    for (const campo of ['nome', 'cpf', 'telefone', 'cidade', 'uf']) document.getElementById(campo).value = cliente[campo] || ''
    formCliente.dataset.idCliente = idEditar
    botaoCliente.textContent = 'Salvar alterações'
    document.getElementById('btn-cancelar').hidden = false
    formCliente.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
  if (idExcluir && confirmarExclusao('este cliente')) {
    try {
      await jsonDaResposta(await fetchAutenticado(`${API}/clientes/${idExcluir}`, { method: 'DELETE' }))
      mostrarMensagem(mensagemClientes, 'Cliente excluído.', true)
      await listarClientes()
    } catch (erro) { mostrarMensagem(mensagemClientes, erro.message) }
  }
})

document.getElementById('btn-cancelar').addEventListener('click', limparFormularioCliente)
listarClientes()
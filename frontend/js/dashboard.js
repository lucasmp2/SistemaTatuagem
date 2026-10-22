// Protege o painel e carrega um resumo das informações cadastradas.
if (protegerPagina()) {
  montarNavegacao('dashboard.html')
  document.getElementById('data-hoje').textContent = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'long' }).format(new Date())
  document.getElementById('atalho-funcionario').hidden = lerTipoToken() !== 'admin'
  carregarResumo()
}

async function carregarResumo() {
  const recursos = [
    ['clientes', 'total-clientes'],
    ['tatuadores', 'total-tatuadores'],
    ['agendamentos', 'total-agendamentos']
  ]
  await Promise.all(recursos.map(async ([rota, elementoId]) => {
    try {
      const resposta = await fetchAutenticado(`${API}/${rota}`)
      const dados = await resposta.json()
      if (resposta.ok) document.getElementById(elementoId).textContent = dados.length
      if (rota === 'agendamentos' && resposta.ok) {
        document.getElementById('total-pendentes').textContent = dados.filter(item => item.status === 'pendente').length
      }
    } catch {
      document.getElementById(elementoId).textContent = '—'
    }
  }))
}
const API_PRODUCAO = 'http://localhost:5001';
const API_QUALIDADE = 'http://localhost:5002';
const API_PECAS = 'http://localhost:5003';
const API_RELATORIOS = 'http://localhost:5004';

async function criarOrdem() {
  const modelo = document.getElementById('modelo').value;
  try {
    const resp = await fetch(`${API_PRODUCAO}/ordens`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ modelo })
    });
    if (!resp.ok) throw new Error(`Erro ao criar ordem: ${resp.status}`);
    await listarOrdens();
  } catch (error) {
    alert(error.message);
  }
}

async function listarOrdens() {
  try {
    const resp = await fetch(`${API_PRODUCAO}/ordens`);
    if (!resp.ok) throw new Error(`Erro ao listar ordens: ${resp.status}`);
    const ordens = await resp.json();

    const ul = document.getElementById('ordens');
    ul.innerHTML = '';

    for (const o of ordens) {
      let etapas = [];
      try {
        const etapasResp = await fetch(`${API_PRODUCAO}/ordens/${o.id}/etapas`);
        if (etapasResp.ok) {
          etapas = await etapasResp.json();
        }
      } catch (error) {
        console.warn(`Erro ao buscar etapas da ordem ${o.id}`, error);
      }

      const li = document.createElement('li');
      li.innerHTML = `
        <strong>ID:</strong> ${o.id}, 
        <strong>Modelo:</strong> ${o.modelo}, 
        <strong>Status:</strong> ${o.status}
        <ul>
          ${etapas.map(e => `<li>${e.descricao} - ${e.status}</li>`).join('')}
        </ul>
      `;
      ul.appendChild(li);
    }
  } catch (error) {
    alert(error.message);
  }
}

async function adicionarEtapa() {
  const ordemId = document.getElementById('etapa_ordem_id').value;
  const descricao = document.getElementById('etapa_descricao').value;
  const status = document.getElementById('etapa_status').value;

  try {
    const resp = await fetch(`${API_PRODUCAO}/ordens/${ordemId}/etapas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ descricao, status })
    });
    if (!resp.ok) throw new Error(`Erro ao adicionar etapa: ${resp.status}`);
    await listarOrdens();
  } catch (error) {
    alert(error.message);
  }
}

async function registrarInspecao() {
  const ordem_id = document.getElementById('ordem_id').value;
  const descricao = document.getElementById('descricao_inspecao').value;
  const conforme = document.getElementById('conforme').checked;

  try {
    const resp = await fetch(`${API_QUALIDADE}/inspecao`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ordem_id, descricao, conforme })
    });
    if (!resp.ok) throw new Error(`Erro ao registrar inspeção: ${resp.status}`);
    await listarInspecoes();
  } catch (error) {
    alert(error.message);
  }
}

async function listarInspecoes() {
  try {
    const resp = await fetch(`${API_QUALIDADE}/inspecao`);
    if (!resp.ok) throw new Error(`Erro ao listar inspeções: ${resp.status}`);
    const dados = await resp.json();
    const ul = document.getElementById('inspecoes');
    ul.innerHTML = '';
    dados.forEach(i => {
      const li = document.createElement('li');
      li.textContent = `Ordem: ${i.ordem_id}, Desc: ${i.descricao}, Conforme: ${i.conforme}`;
      ul.appendChild(li);
    });
  } catch (error) {
    alert(error.message);
  }
}

async function registrarPeca() {
  const codigo = document.getElementById('codigo_peca').value;
  const descricao = document.getElementById('descricao_peca').value;
  const vin = document.getElementById('vin').value;

  try {
    const resp = await fetch(`${API_PECAS}/entrada`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo, descricao, vin })
    });
    if (!resp.ok) throw new Error(`Erro ao registrar peça: ${resp.status}`);
    await listarPecas();
  } catch (error) {
    alert(error.message);
  }
}

async function listarPecas() {
  try {
    const resp = await fetch(`${API_PECAS}/entrada`);
    if (!resp.ok) throw new Error(`Erro ao listar peças: ${resp.status}`);
    const dados = await resp.json();
    const ul = document.getElementById('pecas');
    ul.innerHTML = '';
    dados.forEach(p => {
      const li = document.createElement('li');
      li.textContent = `Código: ${p.codigo}, Descrição: ${p.descricao}, VIN: ${p.vin}`;
      ul.appendChild(li);
    });
  } catch (error) {
    alert(error.message);
  }
}

async function dashboard() {
  try {
    const resp = await fetch(`${API_RELATORIOS}/dashboard`);
    if (!resp.ok) throw new Error('Erro ao buscar dashboard');
    const dados = await resp.json();

    console.log('Dados do dashboard:', dados);  // <<< veja no console do navegador o formato exato

    const dash = document.getElementById('dashboard');

    // Ajuste aqui os campos conforme o retorno real
    const producao = dados.producao || dados.producao || {};
    const qualidade = dados.qualidade || {};

    dash.innerHTML = `
      <style>
        #dashboard {
          display: flex;
          gap: 20px;
          flex-wrap: wrap;
        }
        .card {
          background: #fff;
          border-radius: 8px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          padding: 20px;
          flex: 1 1 250px;
          min-width: 250px;
        }
        .card h3 {
          margin-top: 0;
          color: #333;
          font-family: Arial, sans-serif;
        }
        .card ul {
          list-style: none;
          padding-left: 0;
          font-family: Arial, sans-serif;
        }
        .card ul li {
          margin-bottom: 8px;
          font-size: 16px;
          color: #555;
        }
      </style>

      <div class="card">
        <h3>Indicadores de Produção</h3>
        <ul>
          <li><strong>Total de Ordens:</strong> ${producao.total_ordens || 0}</li>
          <li><strong>Em Andamento:</strong> ${producao.andamento || 0}</li>
          <li><strong>Concluídas:</strong> ${producao.concluidas || 0}</li>
        </ul>
      </div>

      <div class="card">
        <h3>Indicadores de Qualidade</h3>
        <ul>
          <li><strong>Inspeções Totais:</strong> ${qualidade.total_inspecoes || 0}</li>
          <li><strong>Não Conformes:</strong> ${qualidade.nao_conformes || 0}</li>
          <li><strong>Conformidade:</strong> ${qualidade.percentual_conformidade != null ? qualidade.percentual_conformidade + '%' : 'N/A'}</li>
        </ul>
      </div>
    `;
  } catch (error) {
    const dash = document.getElementById('dashboard');
    dash.innerText = 'Erro ao carregar dashboard';
    console.error(error);
  }
}


// Inicialização
listarOrdens();
listarInspecoes();
listarPecas();
dashboard();

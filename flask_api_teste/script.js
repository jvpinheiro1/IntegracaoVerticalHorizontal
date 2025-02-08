// @ts-nocheck
const ctx = document.getElementById('sensorChart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      { label: 'Temperartura (ºC)', data: [], borderColor: 'red', fill: false },
      { label: 'Umidade(%)', data: [], borderColor: 'blue', fill: false },
      { label: 'Pressão (hPa)', data: [], borderColor: 'green', fill: false },
      { label: 'Gas (PpM)', data: [], borderColor: 'purple', fill: false },
      { label: 'Agua (ml)', data: [], borderColor: 'black', fill: false },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Tempo ' } },
    },
  },
});

let intervalId = setInterval(atualizarSensores, 2000);

async function atualizarSensores() {
  try {
    const response = await fetch('http://127.0.0.1:5000/sensores');

    const data = await response.json();

    document.getElementById('temp').innerText = data.temperatura;
    document.getElementById('hum').innerText = data.umidade;
    document.getElementById('pres').innerText = data.pressao;
    document.getElementById('gas').innerText = data.gas;
    document.getElementById('agua').innerText = data.agua;

    if (
      data.temperatura > 75 ||
      data.umidade > 590 ||
      data.pressao > 1090 ||
      data.gas > 990 ||
      data.agua > 790
    ) {
      window.alert('Dados Criticos');
      clearInterval(intervalId);
      document.getElementById('pauseBtn').style.display = 'none';
      document.getElementById('resumeBtn').style.display = 'inline-block';
    }

    chart.data.labels.push(data.data);
    chart.data.datasets[0].data.push(data.temperatura);
    chart.data.datasets[1].data.push(data.umidade);
    chart.data.datasets[2].data.push(data.pressao);
    chart.data.datasets[3].data.push(data.gas);
    chart.data.datasets[4].data.push(data.agua);

    if (chart.data.labels.length > 10) {
      chart.data.labels.shift();
      chart.data.datasets.forEach((dataset) => dataset.data.shift());
    }
    // Atualiza o gráfico na tela
    chart.update();
  } catch (error) {
    console.error('Erro ao buscar dados: ', error);
  }
}

document.getElementById('pauseBtn').addEventListener('click', () => {
  clearInterval(intervalId);
  document.getElementById('pauseBtn').style.display = 'none';
  document.getElementById('resumeBtn').style.display = 'inline-block';
});

document.getElementById('resumeBtn').addEventListener('click', () => {
  intervalId = setInterval(atualizarSensores, 2000);
  document.getElementById('resumeBtn').style.display = 'none';
  document.getElementById('pauseBtn').style.display = 'inline-block';
});

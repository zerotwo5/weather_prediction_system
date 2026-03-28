const API = 'https://weather-prediction-system-vuzl.onrender.com/predict';

/* ── Form Submit ──────────────────────────────────────────────── */
document.getElementById('weatherForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const btn    = document.getElementById('submitBtn');
  const errBox = document.getElementById('errorBox');
  const result = document.getElementById('result');

  // Reset state
  errBox.classList.remove('show');
  result.classList.remove('show');
  btn.classList.add('loading');
  btn.textContent = '⏳ PREDICTING...';

  // Collect & parse form values
  const fd = new FormData(e.target);
  const payload = {};
  for (const [k, v] of fd.entries()) payload[k] = parseFloat(v);

  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    showResult(data);

  } catch (err) {
    errBox.textContent =
      '⚠️  ' + (err.message || 'Could not reach the API. Please check your connection.');
    errBox.classList.add('show');

  } finally {
    btn.classList.remove('loading');
    btn.textContent = '⚡ PREDICT TOMORROW';
  }
});

/* ── Show Result ──────────────────────────────────────────────── */
function showResult(data) {
  const isRain  = data.prediction === 1;
  const inner   = document.getElementById('resultInner');
  const emoji   = document.getElementById('resultEmoji');
  const verdict = document.getElementById('resultVerdict');
  const sub     = document.getElementById('resultSub');
  const rainBar = document.getElementById('rainBar');
  const sunBar  = document.getElementById('sunBar');
  const rainPct = document.getElementById('rainPct');
  const sunPct  = document.getElementById('sunPct');

  // Theme
  inner.className = 'result-inner ' + (isRain ? 'rain' : 'sun');

  // Content
  emoji.textContent   = isRain ? '🌧️' : '☀️';
  verdict.textContent = isRain ? 'RAIN EXPECTED TOMORROW' : 'CLEAR SKIES TOMORROW';
  sub.textContent     = isRain
    ? 'High chance of precipitation — consider carrying an umbrella.'
    : 'Enjoy the sunshine — no rain in the forecast.';

  // Probability bars (delayed for pop-in effect)
  rainPct.textContent = data.probability_rain    + '%';
  sunPct.textContent  = data.probability_no_rain + '%';

  setTimeout(() => {
    rainBar.style.width = data.probability_rain    + '%';
    sunBar.style.width  = data.probability_no_rain + '%';
  }, 300);

  // Show panel & scroll into view
  const result = document.getElementById('result');
  result.classList.add('show');
  result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  // Rain animation if predicted
  if (isRain) spawnRain();
}

/* ── Rain Drop Animation ──────────────────────────────────────── */
function spawnRain() {
  const container = document.getElementById('rainDrops');
  container.innerHTML = '';
  container.classList.add('active');

  for (let i = 0; i < 60; i++) {
    const drop = document.createElement('div');
    drop.className = 'drop';
    drop.style.cssText = `
      left:                ${Math.random() * 100}vw;
      height:              ${20 + Math.random() * 50}px;
      animation-duration:  ${0.6 + Math.random() * 0.8}s;
      animation-delay:     ${Math.random() * 1.2}s;
    `;
    container.appendChild(drop);
  }

  setTimeout(() => {
    container.classList.remove('active');
    container.innerHTML = '';
  }, 2800);
}

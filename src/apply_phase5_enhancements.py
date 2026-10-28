import re
from pathlib import Path

html_path = Path('ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html')
content = html_path.read_text(encoding='utf-8')

print("Iniciando aplicacion de mejoras de Fase 5...")

# ==============================================================================
# 1. TABULAR NUMS Y TOUCH TARGETS EN CSS
# ==============================================================================
css_enhancements = """
    /* FASE 5: TABULAR NUMS Y TIPOGRAFIA DETERMINISTA */
    body, .data-table, .hud-num, .metric-data, .metric-val, .table-container, .latency-val, .status-val {
      font-variant-numeric: tabular-nums;
      font-feature-settings: "tnum";
    }

    .pin-key {
      background: #334155;
      color: #ffffff;
      border: 1px solid #475569;
      border-radius: 12px;
      font-size: 20px;
      font-weight: 700;
      height: 52px;
      cursor: pointer;
      transition: background 0.15s, transform 0.1s;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .pin-key:hover { background: #475569; }
    .pin-key:active { transform: scale(0.96); }

    /* FASE 5: TOUCH TARGETS ERGONOMICOS (>= 48px) EN MOVILES */
    @media (max-width: 768px) {
      .btn-wa-action, .btn-copy, .btn-open-wa, .tab-btn, .btn-lock-header {
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .pill-btn, .toggle-btn {
        min-height: 44px !important;
        padding: 8px 16px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .filter-group, .tabs-nav {
        gap: 8px !important;
      }
    }
"""

marker_style_close = "  </style>"
assert marker_style_close in content, "Marker </style> not found"
content = content.replace(marker_style_close, css_enhancements + "\n  </style>", 1)

# ==============================================================================
# 2. BOTON BLOQUEAR EN HEADER
# ==============================================================================
lock_button_html = """        <button onclick="lockDashboard()" class="pill-btn btn-lock-header" style="background: #1e293b; color: #cbd5e1; border: 1px solid #334155; padding: 7px 14px; font-size: 12px; font-weight: 700; cursor: pointer; border-radius: 8px; display: inline-flex; align-items: center; gap: 6px;">
          <span>🔒</span> Bloquear
        </button>"""

target_header_btn = """        <button onclick="openDropzoneModal()" class="pill-btn active" style="background: #0f172a; color: #ffffff; padding: 7px 16px; font-size: 12px; font-weight: 800; display: inline-flex; align-items: center; gap: 6px; border: none; cursor: pointer; border-radius: 8px;">
          <span>📥</span> Actualizar / Soltar Reporte (Dropzone)
        </button>"""

repl_header_btns = target_header_btn + "\n" + lock_button_html
assert target_header_btn in content, "target_header_btn not found"
content = content.replace(target_header_btn, repl_header_btns, 1)

# ==============================================================================
# 3. HTML DEL LOCK SCREEN (GATEKEEPER SHA-256)
# ==============================================================================
lock_screen_html = """
  <!-- ==================== LOCK SCREEN DIRECTIVO (SHA-256) ==================== -->
  <div id="lock-screen" style="position: fixed; inset: 0; background: #0f172a; z-index: 99999; display: flex; align-items: center; justify-content: center; padding: 20px;">
    <div style="background: #1e293b; border: 1px solid #334155; border-radius: 24px; max-width: 400px; width: 100%; padding: 36px 28px; text-align: center; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);">
      <div style="font-size: 40px; margin-bottom: 8px;">🌿</div>
      <h2 style="font-size: 20px; font-weight: 900; color: #ffffff; letter-spacing: -0.02em;">Qali Kay S.A.C.</h2>
      <p style="font-size: 13px; color: #94a3b8; margin-top: 4px; margin-bottom: 22px;">
        Centro de Inteligencia Comercial<br>
        <strong style="color: #38bdf8;">Acceso Exclusivo para Dirección General</strong>
      </p>

      <div style="margin-bottom: 18px;">
        <input type="password" id="pin-input" maxlength="6" inputmode="numeric" placeholder="••••" style="width: 100%; max-width: 220px; background: #0f172a; border: 2px solid #475569; border-radius: 14px; padding: 12px; font-size: 28px; text-align: center; letter-spacing: 0.3em; color: #38bdf8; font-family: monospace; outline: none; transition: border-color 0.2s;" onkeydown="if(event.key==='Enter') submitPin()" />
      </div>

      <div id="lock-error-msg" style="display: none; color: #f87171; font-size: 12px; font-weight: 700; margin-bottom: 16px;">
        ❌ PIN incorrecto. Ingrese clave autorizada de Dirección.
      </div>

      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 260px; margin: 0 auto 20px;">
        <button onclick="appendPin('1')" class="pin-key">1</button>
        <button onclick="appendPin('2')" class="pin-key">2</button>
        <button onclick="appendPin('3')" class="pin-key">3</button>
        <button onclick="appendPin('4')" class="pin-key">4</button>
        <button onclick="appendPin('5')" class="pin-key">5</button>
        <button onclick="appendPin('6')" class="pin-key">6</button>
        <button onclick="appendPin('7')" class="pin-key">7</button>
        <button onclick="appendPin('8')" class="pin-key">8</button>
        <button onclick="appendPin('9')" class="pin-key">9</button>
        <button onclick="clearPin()" class="pin-key" style="font-size: 14px; color: #94a3b8;">C</button>
        <button onclick="appendPin('0')" class="pin-key">0</button>
        <button onclick="submitPin()" class="pin-key" style="background: #2563eb; color: #ffffff; font-size: 16px;">✓</button>
      </div>

      <button onclick="submitPin()" class="pill-btn active" style="width: 100%; max-width: 260px; min-height: 48px; font-size: 14px; font-weight: 800; border-radius: 12px; background: #2563eb; color: #ffffff; border: none; cursor: pointer;">
        🔓 Desbloquear Tablero
      </button>
    </div>
  </div>
"""

body_start = "<body>"
assert body_start in content, "<body> not found"
content = content.replace(body_start, body_start + "\n" + lock_screen_html, 1)

# ==============================================================================
# 4. ELEVACIÓN DE TODAS LAS FUENTES MENORES A 12px
# ==============================================================================
# Reemplazar patrones CSS y estilos inline
sub_sizes = ['11.5px', '11px', '10px', '9.5px', '9px']
for sz in sub_sizes:
    # font-size: 11px -> font-size: 12px
    content = re.sub(rf'font-size:\s*{re.escape(sz)}', 'font-size: 12px', content)

# ==============================================================================
# 5. JAVASCRIPT: LOGICA DEL LOCK SCREEN (SHA-256 + FALLBACK) Y PAGINACION FEED
# ==============================================================================
js_phase5_logic = """
    // ==========================================================================
    // FASE 5: LOCK SCREEN DIRECTIVO (SHA-256 PURO + WEB CRYPTO API)
    // ==========================================================================
    const VALID_PIN_HASHES = [
      '158a323a7ba44870f23d96f1516dd70aa48e9a72db4ebb026b0a89e212a208ab', // PIN: 2026
      '92c23d77b6b8e8327128859040f3feddb2fbdc914a09f8d37e222f30b4f1a38c'  // PIN: 7361
    ];

    function sha256PureJs(ascii) {
      function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount));
      }
      var mathPow = Math.pow;
      var maxWord = mathPow(2, 32);
      var lengthProperty = 'length';
      var i, j;
      var result = '';
      var words = [];
      var asciiBitLength = ascii[lengthProperty] * 8;
      var hash = sha256PureJs.h = sha256PureJs.h || [];
      var k = sha256PureJs.k = sha256PureJs.k || [];
      var primeCounter = k[lengthProperty];
      var isComposite = {};
      for (var candidate = 2; primeCounter < 64; candidate++) {
        if (!isComposite[candidate]) {
          for (i = 0; i < 313; i += candidate) {
            isComposite[i] = candidate;
          }
          hash[primeCounter] = (mathPow(candidate, 0.5) * maxWord) | 0;
          k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
        }
      }
      ascii += '\\x80';
      while (ascii[lengthProperty] % 64 - 56) ascii += '\\x00';
      for (i = 0; i < ascii[lengthProperty]; i++) {
        j = ascii.charCodeAt(i);
        if (j >> 8) return;
        words[i >> 2] |= j << ((3 - i) % 4) * 8;
      }
      words[words[lengthProperty]] = (asciiBitLength / maxWord) | 0;
      words[words[lengthProperty]] = asciiBitLength;
      for (j = 0; j < words[lengthProperty];) {
        var w = words.slice(j, j += 16);
        var oldHash = hash;
        hash = hash.slice(0, 8);
        for (i = 0; i < 64; i++) {
          var i2 = i + j;
          var w15 = w[i - 15], w2 = w[i - 2];
          var a = hash[0], e = hash[4];
          var temp1 = hash[7]
            + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25))
            + ((e & hash[5]) ^ ((~e) & hash[6]))
            + k[i]
            + (w[i] = (i < 16) ? w[i] : (
                w[i - 16]
                + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3))
                + w[i - 7]
                + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
              ) | 0
            );
          var temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22))
            + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
          hash = [(temp1 + temp2) | 0].concat(hash);
          hash[4] = (hash[4] + temp1) | 0;
        }
        for (i = 0; i < 8; i++) {
          hash[i] = (hash[i] + oldHash[i]) | 0;
        }
      }
      for (i = 0; i < 8; i++) {
        for (j = 3; j >= 0; j--) {
          var b = (hash[i] >> (8 * j)) & 255;
          result += (b < 16 ? '0' : '') + b.toString(16);
        }
      }
      return result;
    }

    async function hashPin(pin) {
      if (typeof window !== 'undefined' && window.crypto && window.crypto.subtle && window.isSecureContext) {
        try {
          const msgUint8 = new TextEncoder().encode(pin);
          const hashBuffer = await window.crypto.subtle.digest('SHA-256', msgUint8);
          const hashArray = Array.from(new Uint8Array(hashBuffer));
          return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        } catch (e) {}
      }
      return sha256PureJs(pin);
    }

    function checkAuthStatus() {
      const auth = sessionStorage.getItem('qalikay_auth');
      const screen = document.getElementById('lock-screen');
      if (!screen) return;
      if (auth === 'authenticated') {
        screen.style.display = 'none';
      } else {
        screen.style.display = 'flex';
        const input = document.getElementById('pin-input');
        if (input) setTimeout(() => input.focus(), 100);
      }
    }

    function lockDashboard() {
      sessionStorage.removeItem('qalikay_auth');
      const screen = document.getElementById('lock-screen');
      if (screen) {
        screen.style.display = 'flex';
        clearPin();
        const input = document.getElementById('pin-input');
        if (input) setTimeout(() => input.focus(), 100);
      }
    }

    async function submitPin() {
      const input = document.getElementById('pin-input');
      const pin = input ? input.value.trim() : '';
      if (!pin) return;
      const h = await hashPin(pin);
      if (VALID_PIN_HASHES.includes(h)) {
        sessionStorage.setItem('qalikay_auth', 'authenticated');
        const screen = document.getElementById('lock-screen');
        if (screen) screen.style.display = 'none';
        const errMsg = document.getElementById('lock-error-msg');
        if (errMsg) errMsg.style.display = 'none';
      } else {
        const errMsg = document.getElementById('lock-error-msg');
        if (errMsg) errMsg.style.display = 'block';
        clearPin();
      }
    }

    function appendPin(num) {
      const input = document.getElementById('pin-input');
      if (input && input.value.length < 6) {
        input.value += num;
      }
    }

    function clearPin() {
      const input = document.getElementById('pin-input');
      if (input) input.value = '';
    }

    // ==========================================================================
    // FASE 5: PAGINACIÓN PROGRESIVA DEL FEED (50 EN 50)
    // ==========================================================================
    let feedDisplayLimit = 50;
    const FEED_PAGE_SIZE = 50;

    function resetFeedLimit() {
      feedDisplayLimit = 50;
    }

    function loadMoreFeed() {
      feedDisplayLimit += FEED_PAGE_SIZE;
      renderActionCards(activeFilter);
      renderTableRows(activeFilter);
    }

    function showAllFeed() {
      feedDisplayLimit = 999999;
      renderActionCards(activeFilter);
      renderTableRows(activeFilter);
    }
"""

# Inyectar las funciones de Fase 5 antes de renderActionCards
target_render_func = "    function renderActionCards(filter) {"
assert target_render_func in content, "target_render_func not found"
content = content.replace(target_render_func, js_phase5_logic + "\n" + target_render_func, 1)

# ==============================================================================
# 6. MODIFICAR renderActionCards Y renderTableRows PARA APLICAR PAGINACION
# ==============================================================================
old_render_cards_block = """      list.forEach((c) => {
        const card = document.createElement('div');"""

new_render_cards_block = """      const visibleList = list.slice(0, feedDisplayLimit);
      visibleList.forEach((c) => {
        const card = document.createElement('div');"""

assert old_render_cards_block in content, "old_render_cards_block not found"
content = content.replace(old_render_cards_block, new_render_cards_block, 1)

# Añadir botones de paginacion al final de renderActionCards
old_end_render_cards = """        container.appendChild(card);
      });
    }"""

new_end_render_cards = """        container.appendChild(card);
      });

      if (list.length > feedDisplayLimit) {
        const pagDiv = document.createElement('div');
        pagDiv.style.gridColumn = '1 / -1';
        pagDiv.style.display = 'flex';
        pagDiv.style.justifyContent = 'center';
        pagDiv.style.alignItems = 'center';
        pagDiv.style.gap = '12px';
        pagDiv.style.padding = '24px 0';
        pagDiv.style.flexWrap = 'wrap';

        const remaining = list.length - feedDisplayLimit;
        pagDiv.innerHTML = `
          <button onclick="loadMoreFeed()" class="pill-btn active" style="min-height: 48px; padding: 10px 24px; font-size: 13px; font-weight: 800; cursor: pointer; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            📥 Mostrar siguientes ${Math.min(50, remaining)} cuentas (Quedan ${remaining})
          </button>
          <button onclick="showAllFeed()" class="pill-btn" style="min-height: 48px; padding: 10px 20px; font-size: 13px; font-weight: 700; cursor: pointer; border-radius: 12px; background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;">
            ⚡ Ver todas las ${list.length} cuentas
          </button>
        `;
        container.appendChild(pagDiv);
      }
    }"""

assert old_end_render_cards in content, "old_end_render_cards not found"
content = content.replace(old_end_render_cards, new_end_render_cards, 1)

# Modificar renderTableRows
old_render_table_block = """      list.forEach((c) => {
        const tr = document.createElement('tr');"""

new_render_table_block = """      const visibleList = list.slice(0, feedDisplayLimit);
      visibleList.forEach((c) => {
        const tr = document.createElement('tr');"""

assert old_render_table_block in content, "old_render_table_block not found"
content = content.replace(old_render_table_block, new_render_table_block, 1)

old_end_render_table = """        tbody.appendChild(tr);
      });
    }"""

new_end_render_table = """        tbody.appendChild(tr);
      });

      if (list.length > feedDisplayLimit) {
        const remaining = list.length - feedDisplayLimit;
        const trPag = document.createElement('tr');
        trPag.innerHTML = `
          <td colspan="9" style="text-align: center; padding: 20px;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 12px; flex-wrap: wrap;">
              <button onclick="loadMoreFeed()" class="pill-btn active" style="min-height: 48px; padding: 10px 24px; font-size: 13px; font-weight: 800; cursor: pointer; border-radius: 12px;">
                📥 Mostrar siguientes ${Math.min(50, remaining)} cuentas (Quedan ${remaining})
              </button>
              <button onclick="showAllFeed()" class="pill-btn" style="min-height: 48px; padding: 10px 20px; font-size: 13px; font-weight: 700; cursor: pointer; border-radius: 12px; background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;">
                ⚡ Ver todas las ${list.length} cuentas
              </button>
            </div>
          </td>
        `;
        tbody.appendChild(trPag);
      }
    }"""

assert old_end_render_table in content, "old_end_render_table not found"
content = content.replace(old_end_render_table, new_end_render_table, 1)

# En filterFeed(f), resetear límite de paginación
old_filter_feed = """    function filterFeed(f) {
      activeFilter = f;"""

new_filter_feed = """    function filterFeed(f) {
      activeFilter = f;
      resetFeedLimit();"""

assert old_filter_feed in content, "old_filter_feed not found"
content = content.replace(old_filter_feed, new_filter_feed, 1)

# Añadir checkAuthStatus() a la inicialización
old_init_block = """    // INICIALIZACIÓN COMPLETA
    applyRealDataToDom();"""

new_init_block = """    // INICIALIZACIÓN COMPLETA
    checkAuthStatus();
    applyRealDataToDom();"""

assert old_init_block in content, "old_init_block not found"
content = content.replace(old_init_block, new_init_block, 1)

html_path.write_text(content, encoding='utf-8')
print("Mejoras de Fase 5 aplicadas exitosamente en el archivo HTML!")

#!/usr/bin/env python3
"""
차티스트 인사이트 index.html 패치 v2
- 매매일지 개선 (1~11번)
- 알트코인 RSI 블러 + 색상 (15~16번)
- 자산제곱 디자인 벤치마킹
"""
import re, os, shutil

HTML = '/home/ubuntu/chartist-insight/index.html'

if not os.path.exists(HTML):
    print(f"❌ 파일 없음: {HTML}")
    exit(1)

with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

orig_size = len(content)
shutil.copy(HTML, HTML + '.bak_v2')
print(f"백업 완료: {HTML}.bak_v2")

patches = []

# ══════════════════════════════════════════════
# [1] CSS 추가 - </style> 바로 앞에 삽입
# ══════════════════════════════════════════════
NEW_CSS = """
  /* ══ [v2] 매매일지 개선 CSS ══ */
  /* 스피너 화살표 숨기기 */
  input[type=number]::-webkit-inner-spin-button,
  input[type=number]::-webkit-outer-spin-button { -webkit-appearance:none; margin:0; }
  input[type=number] { -moz-appearance:textfield; }

  /* 연승/연패 폰트 통일 */
  .jsc-val { font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:700; letter-spacing:-0.5px; }
  .jsc-val.up { color:var(--green); }
  .jsc-val.dn { color:var(--red); }
  .jsc-val.neu { color:var(--text3); }

  /* 인사이트 박스 (자산제곱 벤치마킹) */
  .insight-box {
    background:#0d0d0d;
    border-left:3px solid var(--gold);
    border-radius:0 8px 8px 0;
    padding:10px 14px;
    margin:8px 0;
    font-size:12px;
    color:var(--text2);
    line-height:1.75;
  }
  .insight-box strong { color:var(--text); }

  /* 상태 배지 (자산제곱 벤치마킹) */
  .stat-badge {
    display:inline-flex;align-items:center;
    font-size:10px;font-family:'JetBrains Mono',monospace;font-weight:700;
    padding:3px 8px;border-radius:4px;letter-spacing:.04em;
    text-transform:uppercase;white-space:nowrap;
  }
  .stat-badge.green { background:rgba(76,175,125,0.15);color:var(--green);border:1px solid rgba(76,175,125,0.3); }
  .stat-badge.red   { background:rgba(224,85,85,0.15);color:var(--red2);border:1px solid rgba(224,85,85,0.3); }
  .stat-badge.gold  { background:rgba(201,168,76,0.12);color:var(--gold);border:1px solid rgba(201,168,76,0.3); }
  .stat-badge.neu   { background:rgba(255,255,255,0.05);color:var(--text3);border:1px solid rgba(255,255,255,0.1); }

  /* 히어로 카드 개선 (자산제곱 벤치마킹) */
  .market-card { position:relative; transition:border-color 0.2s; }
  .market-card:hover { border-color:rgba(201,168,76,0.3); }
  .mc-desc { font-size:10px;color:var(--text3);margin-top:6px;padding-top:6px;border-top:0.5px solid var(--border); }

  /* 매매일지 통계 카드 개선 */
  .jstat-card {
    background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;
    padding:16px;transition:border-color 0.2s;
  }
  .jstat-card:hover { border-color:var(--border2); }
  .jstat-label { font-size:11px;color:var(--text3);margin-bottom:8px;font-weight:500; }
  .jstat-val-wrap { display:flex;align-items:flex-end;justify-content:space-between; }
  .jstat-val { font-size:22px;font-weight:700;font-family:'JetBrains Mono',monospace;letter-spacing:-0.5px; }

  /* 승률 게이지 개선 */
  .wr-gauge-wrap { margin-top:8px; }
  .wr-gauge-bg { height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden; }
  .wr-gauge-fill { height:100%;border-radius:2px;transition:width 0.5s ease;background:var(--green); }

  /* 자동완성 드롭다운 */
  .ticker-autocomplete {
    position:absolute;top:100%;left:0;right:0;z-index:100;
    background:var(--bg2);border:0.5px solid var(--border2);
    border-radius:0 0 8px 8px;max-height:200px;overflow-y:auto;
  }
  .ticker-autocomplete-item {
    padding:8px 12px;font-size:12px;cursor:pointer;
    display:flex;align-items:center;justify-content:space-between;
    border-bottom:0.5px solid var(--border);transition:background 0.1s;
  }
  .ticker-autocomplete-item:hover { background:rgba(201,168,76,0.08); }
  .ticker-autocomplete-item:last-child { border-bottom:none; }
  .tac-symbol { color:var(--text);font-weight:500; }
  .tac-name { color:var(--text3);font-size:11px; }
  .ticker-input-wrap { position:relative; }

  /* 매매 수정 폼 */
  .journal-edit-form {
    background:var(--bg3);border:0.5px solid var(--border2);
    border-radius:10px;padding:14px;margin-top:8px;
  }

  /* RSI 다이버전스 색상 */
  .sig-rsi-bull { background:rgba(224,85,85,0.12);color:#ff6b6b; }
  .sig-rsi-bear-badge { background:rgba(74,158,255,0.12);color:var(--blue); }

  /* 달력 인풋 개선 */
  input[type=date] {
    background:var(--bg3);border:0.5px solid var(--border2);
    border-radius:8px;padding:var(--pad-input);color:var(--text);
    font-family:'JetBrains Mono',monospace;font-size:var(--fs-md);
    width:100%;transition:border-color 0.15s;
    -webkit-appearance:none;
    color-scheme:dark;
  }
  input[type=date]:focus { outline:none;border-color:var(--gold); }
  input[type=date]::-webkit-calendar-picker-indicator {
    filter:invert(0.6);cursor:pointer;
  }

  /* 천단위 구분 힌트 */
  .amount-hint { font-size:11px;color:var(--gold);margin-top:3px;font-family:'JetBrains Mono',monospace; }
"""

if NEW_CSS.strip()[:20] not in content:
    content = content.replace('</style>', NEW_CSS + '\n</style>', 1)
    print('[1] CSS 추가 완료')
else:
    print('[1] CSS 이미 존재')

# ══════════════════════════════════════════════
# [2] 히어로 카드 설명 추가 (BTC/공포탐욕)
# ══════════════════════════════════════════════
old_btc_card = '<div class="mc-label">BTC / USDT</div>'
new_btc_card = '<div class="mc-label">BTC / USDT</div>'
# mc-change 뒤에 mc-desc 추가
old_btc_change = '<div class="mc-change" id="btc-change">연결 중...</div>\n  </div>'
new_btc_change = '<div class="mc-change" id="btc-change">연결 중...</div>\n    <div class="mc-desc">바이낸스 실시간 · USDT 기준</div>\n  </div>'
if old_btc_change in content:
    content = content.replace(old_btc_change, new_btc_change, 1)
    print('[2] BTC 카드 desc 추가')

old_fg_label = '<div class="fg-label" id="fg-label">로딩 중...</div>\n    </div>'
new_fg_label = '<div class="fg-label" id="fg-label">로딩 중...</div>\n      <div class="mc-desc">CNN Fear &amp; Greed · 0=극공포 100=극탐욕</div>\n    </div>'
if old_fg_label in content:
    content = content.replace(old_fg_label, new_fg_label, 1)
    print('[2] 공포탐욕 카드 desc 추가')

# ══════════════════════════════════════════════
# [3] RSI 다이버전스 - 전체 탭 블러 + 색상 구분
# ══════════════════════════════════════════════
# 필터 버튼 색상 변경
old_rsi_bull_btn = '<button class="filter-btn" id="af-rsi-bull" onclick="filterAltcoin(\'rsi_bull\')">📈 상승 다이버전스</button>'
new_rsi_bull_btn = '<button class="filter-btn" id="af-rsi-bull" onclick="filterAltcoin(\'rsi_bull\')" style="--active-color:var(--red2)">📈 상승 다이버전스</button>'

old_rsi_bear_btn = '<button class="filter-btn" id="af-rsi-bear" onclick="filterAltcoin(\'rsi_bear\')">📉 하락 다이버전스</button>'
new_rsi_bear_btn = '<button class="filter-btn" id="af-rsi-bear" onclick="filterAltcoin(\'rsi_bear\')" style="--active-color:var(--blue)">📉 하락 다이버전스</button>'

# sigMap 업데이트 - 상승/하락 다이버전스 색상 구분
old_sigmap = "  rsi_bull:{label:'상승 다이버전스',cls:'sig-rsi'},"
new_sigmap = "  rsi_bull:{label:'상승 다이버전스',cls:'sig-rsi-bull'},"
if old_sigmap in content:
    content = content.replace(old_sigmap, new_sigmap)
    print('[3] RSI 상승 다이버전스 색상 변경')

old_sigmap2 = "  rsi_bear:{label:'하락 다이버전스',cls:'sig-rsi-bear'},"
new_sigmap2 = "  rsi_bear:{label:'하락 다이버전스',cls:'sig-rsi-bear-badge'},"
if old_sigmap2 in content:
    content = content.replace(old_sigmap2, new_sigmap2)
    print('[3] RSI 하락 다이버전스 색상 변경')

# 전체 탭에서도 RSI 블러 처리 - filterAltcoin 함수 수정
old_filter = """function filterAltcoin(f){
  currentAltcoinFilter=f;
  var ids=['all','trend','ma','rsi-bull','rsi-bear','kiz','wyc'];
  ids.forEach(function(v){var btn=document.getElementById('af-'+v);if(btn)btn.classList.remove('active');});
  var activeId=f==='rsi_bull'?'rsi-bull':f==='rsi_bear'?'rsi-bear':f;
  var activeBtn=document.getElementById('af-'+activeId);
  if(activeBtn)activeBtn.classList.add('active');

  var isDivFilter=(f==='rsi_bull'||f==='rsi_bear');
  if(isDivFilter&&!rsiUnlocked){
    lockRsi();
  }else if(!isDivFilter){
    var content=document.getElementById('rsi-blur-content');
    var paywall=document.getElementById('rsi-paywall');
    if(content)content.classList.remove('blurred');
    if(paywall)paywall.classList.remove('show');
  }
  renderAltcoin();
}"""

new_filter = """function filterAltcoin(f){
  currentAltcoinFilter=f;
  var ids=['all','trend','ma','rsi-bull','rsi-bear','kiz','wyc'];
  ids.forEach(function(v){var btn=document.getElementById('af-'+v);if(btn)btn.classList.remove('active');});
  var activeId=f==='rsi_bull'?'rsi-bull':f==='rsi_bear'?'rsi-bear':f;
  var activeBtn=document.getElementById('af-'+activeId);
  if(activeBtn)activeBtn.classList.add('active');

  var isDivFilter=(f==='rsi_bull'||f==='rsi_bear');
  // 전체 탭에서도 RSI 포함된 경우 블러
  var hasRsi=(f==='all');
  if((isDivFilter||hasRsi)&&!rsiUnlocked){
    lockRsi();
  }else if(!isDivFilter&&!hasRsi){
    var bc=document.getElementById('rsi-blur-content');
    var bp=document.getElementById('rsi-paywall');
    if(bc)bc.classList.remove('blurred');
    if(bp)bp.classList.remove('show');
  }else if(rsiUnlocked){
    var bc2=document.getElementById('rsi-blur-content');
    var bp2=document.getElementById('rsi-paywall');
    if(bc2)bc2.classList.remove('blurred');
    if(bp2)bp2.classList.remove('show');
  }
  renderAltcoin();
}"""

if old_filter in content:
    content = content.replace(old_filter, new_filter)
    print('[3] RSI 전체 탭 블러 처리')

# ══════════════════════════════════════════════
# [4] 매매일지 통계 카드 UI 개선 (자산제곱 배지)
# ══════════════════════════════════════════════
old_stats_html = '''<div id="journal-stats">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
      <div style="background:var(--bg3);border:0.5px solid var(--border);border-radius:10px;padding:14px;">
        <div style="font-size:11px;color:var(--text3);margin-bottom:6px;">승률</div>
        <div class="jsc-val neu" id="jstat-wr">—</div>
        <div class="wr-gauge-bg" style="margin-top:8px;"><div class="wr-gauge-fill" id="jstat-wr-fill" style="width:0%"></div></div>
      </div>
      <div style="background:var(--bg3);border:0.5px solid var(--border);border-radius:10px;padding:14px;">
        <div style="font-size:11px;color:var(--text3);margin-bottom:6px;">총 손익</div>
        <div class="jsc-val neu" id="jstat-pnl">—</div>
      </div>
      <div style="background:var(--bg3);border:0.5px solid var(--border);border-radius:10px;padding:14px;">
        <div style="font-size:11px;color:var(--text3);margin-bottom:6px;">평균 수익률</div>
        <div class="jsc-val neu" id="jstat-avg">—</div>
      </div>
      <div style="background:var(--bg3);border:0.5px solid var(--border);border-radius:10px;padding:14px;">
        <div style="font-size:11px;color:var(--text3);margin-bottom:6px;">연속 승/패</div>
        <div class="jsc-val neu" id="jstat-streak">—</div>
      </div>
    </div>'''

new_stats_html = '''<div id="journal-stats">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
      <div class="jstat-card">
        <div class="jstat-label">승률</div>
        <div class="jstat-val-wrap">
          <div class="jsc-val neu" id="jstat-wr">—</div>
          <span class="stat-badge neu" id="jstat-wr-badge">—</span>
        </div>
        <div class="wr-gauge-wrap"><div class="wr-gauge-bg"><div class="wr-gauge-fill" id="jstat-wr-fill" style="width:0%"></div></div></div>
      </div>
      <div class="jstat-card">
        <div class="jstat-label">총 손익</div>
        <div class="jstat-val-wrap">
          <div class="jsc-val neu" id="jstat-pnl">—</div>
          <span class="stat-badge neu" id="jstat-pnl-badge">—</span>
        </div>
      </div>
      <div class="jstat-card">
        <div class="jstat-label">평균 수익률</div>
        <div class="jstat-val-wrap">
          <div class="jsc-val neu" id="jstat-avg">—</div>
        </div>
      </div>
      <div class="jstat-card">
        <div class="jstat-label">연속 승/패</div>
        <div class="jstat-val-wrap">
          <div class="jsc-val neu" id="jstat-streak">—</div>
        </div>
      </div>
    </div>'''

if old_stats_html in content:
    content = content.replace(old_stats_html, new_stats_html)
    print('[4] 통계 카드 UI 개선')

# ══════════════════════════════════════════════
# [5] 매매일지 로그인 폼 - 닫기버튼 + 회원가입
# ══════════════════════════════════════════════
old_login_box = '''<div id="journal-login-screen" style="max-width:400px;margin:40px auto;">
      <div style="background:var(--bg2);border:0.5px solid rgba(201,168,76,0.2);border-radius:20px;padding:32px 28px;text-align:center;">
        <div style="font-size:22px;margin-bottom:8px;">📒 매매일지</div>
        <div style="font-size:13px;color:var(--text2);margin-bottom:24px;">팬딩 아이디와<br>직접 설정한 비밀번호로 로그인하세요.</div>'''

new_login_box = '''<div id="journal-login-screen" style="max-width:400px;margin:40px auto;">
      <div style="background:var(--bg2);border:0.5px solid rgba(201,168,76,0.2);border-radius:20px;padding:32px 28px;text-align:center;position:relative;">
        <div style="font-size:22px;margin-bottom:8px;">📒 매매일지</div>
        <div style="font-size:13px;color:var(--text2);margin-bottom:24px;">팬딩 아이디와<br>직접 설정한 비밀번호로 로그인하세요.</div>'''

if old_login_box in content:
    content = content.replace(old_login_box, new_login_box)
    print('[5] 로그인 박스 position:relative 추가')

# 회원가입 버튼 추가 (로그인 버튼 아래)
old_login_btn = '''<button class="journal-btn" onclick="journalLogin()">로그인</button>
          <button class="journal-btn-sec" onclick="showJournalRegister()">처음 오셨나요? 가입하기</button>'''

# 이미 있으면 패스, 없으면 다른 패턴 찾기
if old_login_btn not in content:
    old_login_btn2 = '<button class="journal-btn" onclick="journalLogin()">로그인</button>'
    new_login_btn2 = '''<button class="journal-btn" onclick="journalLogin()">로그인</button>
          <button class="journal-btn-sec" onclick="showJournalRegister()" style="width:100%;background:transparent;border:0.5px solid var(--border2);border-radius:10px;padding:11px;color:var(--text3);font-size:13px;font-family:\'Noto Sans KR\',sans-serif;cursor:pointer;margin-top:8px;transition:all 0.15s;">처음 오셨나요? <span style="color:var(--gold);">회원가입</span></button>'''
    if old_login_btn2 in content:
        content = content.replace(old_login_btn2, new_login_btn2, 1)
        print('[5] 회원가입 버튼 추가')

# ══════════════════════════════════════════════
# [6] 매매일지 입력폼 - 필수 안내 + 배율 + 천단위
# ══════════════════════════════════════════════
old_form_open = '''<div id="journal-add-form" class="journal-add-form">
      <div class="journal-add-title">새 매매 기록</div>'''

new_form_open = '''<div id="journal-add-form" class="journal-add-form">
      <div class="journal-add-title">새 매매 기록</div>
      <div class="insight-box" style="margin-bottom:14px;">
        <strong>📌 필수 입력:</strong> 날짜 · 종목 · 방향 · 진입가<br>
        <span style="font-size:11px;color:var(--text3);">투자금액 입력 시 손익금액 자동계산 · 청산가 입력 시 수익률% 자동계산</span>
      </div>'''

if old_form_open in content:
    content = content.replace(old_form_open, new_form_open)
    print('[6] 필수 항목 안내 문구 추가')

# 종목 입력란 → 자동완성 래퍼로 교체
old_ticker_input = '''<input class="journal-input" id="jf-ticker" type="text" placeholder="종목 (예: BTC)" autocomplete="off">'''
new_ticker_input = '''<div class="ticker-input-wrap">
            <input class="journal-input" id="jf-ticker" type="text" placeholder="종목 검색 (예: BTC)" autocomplete="off" oninput="searchTicker(this.value)" onblur="setTimeout(hideTickerDrop,200)">
            <div class="ticker-autocomplete" id="ticker-drop" style="display:none;"></div>
          </div>'''
if old_ticker_input in content:
    content = content.replace(old_ticker_input, new_ticker_input)
    print('[6] 종목 자동완성 추가')

# 배율 입력란 추가 (투자금액 뒤에)
old_amount_field = '''<div class="journal-field">
            <label class="journal-label">투자금액 (USDT)<span style="color:var(--text3);font-size:10px;"> 선택</span></label>
            <input class="journal-input" id="jf-amount" type="number" placeholder="예: 1000" min="0" step="any">
            <div class="hint" style="font-size:11px;color:var(--blue);margin-top:2px;">💡 청산가까지 입력 시 손익금액 자동계산</div>
          </div>'''

new_amount_field = '''<div class="journal-field">
            <label class="journal-label">투자금액 (USDT)<span style="color:var(--text3);font-size:10px;"> 선택</span></label>
            <input class="journal-input" id="jf-amount" type="text" placeholder="예: 1,000" oninput="fmtJournalAmount(this)" autocomplete="off">
            <div id="jf-amount-hint" class="amount-hint"></div>
            <div class="hint" style="font-size:11px;color:var(--blue);margin-top:2px;">💡 청산가까지 입력 시 손익금액 자동계산</div>
          </div>
          <div class="journal-field">
            <label class="journal-label">배율<span style="color:var(--text3);font-size:10px;"> 선택</span></label>
            <input class="journal-input" id="jf-leverage" type="number" placeholder="예: 10" min="1" max="125" step="1">
          </div>'''

if old_amount_field in content:
    content = content.replace(old_amount_field, new_amount_field)
    print('[6] 배율 입력란 + 천단위 추가')

# ══════════════════════════════════════════════
# [7] 매매 수정 기능 - journalCloseModal 개선
# ══════════════════════════════════════════════
old_close_modal = """function journalCloseModal(id){
  var exitP=prompt('청산가를 입력하세요:');"""

new_close_modal = """function journalCloseModal(id){
  var exitP=prompt('청산가를 입력하세요 (숫자만):');"""

if old_close_modal in content:
    content = content.replace(old_close_modal, new_close_modal)
    print('[7] 청산 모달 개선')

# ══════════════════════════════════════════════
# [8] JS 추가 - 자동완성, 천단위, 배지 업데이트
# ══════════════════════════════════════════════
NEW_JS = """
// ══════════════════════════════════════════════
// [v2] 매매일지 개선 JS
// ══════════════════════════════════════════════

// 바이낸스 선물 주요 코인 목록
var BINANCE_FUTURES = [
  {s:'BTC',n:'비트코인'},  {s:'ETH',n:'이더리움'},  {s:'BNB',n:'바이낸스코인'},
  {s:'SOL',n:'솔라나'},    {s:'XRP',n:'리플'},       {s:'ADA',n:'에이다'},
  {s:'DOGE',n:'도지코인'}, {s:'AVAX',n:'아발란체'},  {s:'DOT',n:'폴카닷'},
  {s:'LINK',n:'체인링크'}, {s:'UNI',n:'유니스왑'},   {s:'LTC',n:'라이트코인'},
  {s:'BCH',n:'비트코인캐시'},{s:'ATOM',n:'코스모스'},{s:'NEAR',n:'니어'},
  {s:'APT',n:'앱토스'},    {s:'ARB',n:'아비트럼'},   {s:'OP',n:'옵티미즘'},
  {s:'SUI',n:'수이'},      {s:'INJ',n:'인젝티브'},   {s:'TIA',n:'셀레스티아'},
  {s:'SEI',n:'세이'},      {s:'JTO',n:'지토'},        {s:'WIF',n:'도그위프햇'},
  {s:'PEPE',n:'페페'},     {s:'BONK',n:'봉크'},       {s:'SHIB',n:'시바이누'},
  {s:'FIL',n:'파일코인'},  {s:'ICP',n:'인터넷컴퓨터'},{s:'RNDR',n:'렌더'},
  {s:'GRT',n:'더그래프'},  {s:'AAVE',n:'아베'},       {s:'MKR',n:'메이커'},
  {s:'SNX',n:'신세틱스'},  {s:'CRV',n:'커브'},        {s:'LDO',n:'리도'},
  {s:'RUNE',n:'토르체인'}, {s:'ALGO',n:'알고랜드'},   {s:'XLM',n:'스텔라루멘'},
  {s:'VET',n:'비체인'},    {s:'HBAR',n:'헤데라'},     {s:'EOS',n:'이오스'},
  {s:'ZIL',n:'질리카'},    {s:'MANA',n:'디센트럴랜드'},{s:'SAND',n:'샌드박스'},
  {s:'AXS',n:'엑시인피니티'},{s:'CHZ',n:'칠리즈'},    {s:'GMT',n:'스테핀'},
  {s:'BAT',n:'베이직어텐션'},{s:'ZBT',n:'제비트'},    {s:'KAVA',n:'카바'},
  {s:'FLOW',n:'플로우'},   {s:'ENJ',n:'엔진코인'},    {s:'1INCH',n:'1인치'},
  {s:'SUSHI',n:'스시스왑'},{s:'COMP',n:'컴파운드'},   {s:'YFI',n:'연파이낸스'},
  {s:'BAL',n:'밸런서'},    {s:'ZRX',n:'0x'},          {s:'MASK',n:'마스크네트워크'},
  {s:'DYDX',n:'디와이디엑스'},{s:'IMX',n:'이뮤터블'},  {s:'BLUR',n:'블러'},
  {s:'MAGIC',n:'매직'},    {s:'GMX',n:'지엠엑스'},    {s:'PENDLE',n:'펜들'},
  {s:'JUP',n:'주피터'},    {s:'PYTH',n:'파이스'},     {s:'W',n:'웜홀'},
  {s:'ZK',n:'지케이싱크'}, {s:'STRK',n:'스타크넷'},   {s:'MANTA',n:'만타'},
  {s:'ALT',n:'알트레이어'},{s:'PIXEL',n:'픽셀'},       {s:'PORTAL',n:'포털'},
  {s:'ETHFI',n:'이더파이'},{s:'ENA',n:'에나'},         {s:'EIGEN',n:'아이겐레이어'},
];

function searchTicker(val){
  var drop=document.getElementById('ticker-drop');
  if(!drop)return;
  if(!val||val.length<1){drop.style.display='none';return;}
  var q=val.toUpperCase();
  var results=BINANCE_FUTURES.filter(function(c){
    return c.s.startsWith(q)||c.n.includes(val);
  }).slice(0,8);
  if(!results.length){drop.style.display='none';return;}
  drop.innerHTML=results.map(function(c){
    return '<div class="ticker-autocomplete-item" onmousedown="selectTicker(\''+c.s+'\')">'
      +'<span class="tac-symbol">'+c.s+'</span>'
      +'<span class="tac-name">'+c.n+'</span>'
      +'</div>';
  }).join('');
  drop.style.display='block';
}

function selectTicker(sym){
  var inp=document.getElementById('jf-ticker');
  if(inp) inp.value=sym;
  hideTickerDrop();
}

function hideTickerDrop(){
  var drop=document.getElementById('ticker-drop');
  if(drop) drop.style.display='none';
}

// 투자금액 천단위 포맷
function fmtJournalAmount(el){
  var raw=el.value.replace(/[^0-9.]/g,'');
  var num=parseFloat(raw);
  var hint=document.getElementById('jf-amount-hint');
  if(!isNaN(num)&&num>0){
    el.setAttribute('data-raw', raw);
    if(hint) hint.textContent='≈ '+num.toLocaleString('ko-KR')+' USDT';
  }else{
    el.setAttribute('data-raw','');
    if(hint) hint.textContent='';
  }
}

// 통계 배지 업데이트
function updateStatBadges(wr, totalPnl){
  var wrBadge=document.getElementById('jstat-wr-badge');
  var pnlBadge=document.getElementById('jstat-pnl-badge');
  if(wrBadge){
    if(wr>=60){wrBadge.textContent='우수';wrBadge.className='stat-badge green';}
    else if(wr>=50){wrBadge.textContent='보통';wrBadge.className='stat-badge gold';}
    else{wrBadge.textContent='개선필요';wrBadge.className='stat-badge red';}
  }
  if(pnlBadge){
    if(totalPnl>0){pnlBadge.textContent='수익';pnlBadge.className='stat-badge green';}
    else if(totalPnl<0){pnlBadge.textContent='손실';pnlBadge.className='stat-badge red';}
    else{pnlBadge.textContent='중립';pnlBadge.className='stat-badge neu';}
  }
}
"""

if 'BINANCE_FUTURES' not in content:
    # </script> 바로 앞에 삽입
    content = content.replace('</script>\n<script>if("serviceWorker"', NEW_JS + '\n</script>\n<script>if("serviceWorker"', 1)
    print('[8] 자동완성/천단위/배지 JS 추가')

# ══════════════════════════════════════════════
# [9] renderJournalStats에 배지 업데이트 호출 추가
# ══════════════════════════════════════════════
old_stats_end = "  if(strkEl){strkEl.textContent=streak>0?(streakType==='win'?'✅ '+streak+'연승':'❌ '+streak+'연패'):'—';}"
new_stats_end = "  if(strkEl){strkEl.textContent=streak>0?(streakType==='win'?streak+'연승':streak+'연패'):'—';if(strkEl){strkEl.className='jsc-val '+(streak>0&&streakType==='win'?'up':'dn');}}\n  updateStatBadges(wr, totalPnl);"

if old_stats_end in content:
    content = content.replace(old_stats_end, new_stats_end)
    print('[9] 통계 배지 업데이트 + 연승 폰트 수정')

# ══════════════════════════════════════════════
# [10] 총손익 천단위 구분
# ══════════════════════════════════════════════
old_pnl_txt = "if(pnlEl){pnlEl.textContent=closed.length>0?(totalPnl>=0?'+':'')+totalPnl.toFixed(2)+' USDT':'—';"
new_pnl_txt = "if(pnlEl){var pnlFmt=totalPnl.toLocaleString('ko-KR',{minimumFractionDigits:2,maximumFractionDigits:2});pnlEl.textContent=closed.length>0?(totalPnl>=0?'+':'')+pnlFmt+' USDT':'—';"

if old_pnl_txt in content:
    content = content.replace(old_pnl_txt, new_pnl_txt)
    print('[10] 총손익 천단위 구분')

# ══════════════════════════════════════════════
# [11] journalAdd - amount raw값 읽기
# ══════════════════════════════════════════════
old_amount_read = "  var amount=document.getElementById('jf-amount').value;"
new_amount_read = "  var amountEl=document.getElementById('jf-amount');var amount=amountEl.getAttribute('data-raw')||amountEl.value.replace(/[^0-9.]/g,'');"

if old_amount_read in content:
    content = content.replace(old_amount_read, new_amount_read, 1)
    print('[11] 투자금액 raw값 읽기')

# ══════════════════════════════════════════════
# 최종 저장
# ══════════════════════════════════════════════
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

new_size = len(content)
print(f"\n최종 크기: {orig_size:,} → {new_size:,} (+{new_size-orig_size:,})")
print("✅ 패치 완료! push_to_github.sh 실행하세요.")

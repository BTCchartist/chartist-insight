#!/usr/bin/env python3
"""
차티스트 인사이트 index.html 패치 스크립트
VPS에서 실행: python3 patch_index.py
"""
import os, re

TARGET = '/home/ubuntu/chartist-insight/index.html'
BACKUP = TARGET + '.bak_patch'

with open(TARGET, 'r', encoding='utf-8') as f:
    html = f.read()

# 백업
with open(BACKUP, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"백업 완료: {BACKUP}")

original_len = len(html)

# ═══════════════════════════════════════════════════
# [1] CSS 추가 - </style> 바로 앞에 삽입
# ═══════════════════════════════════════════════════
NEW_CSS = """
  /* ══ BTC 탭 블러 ══ */
  .btc-blur-wrap{position:relative;}
  .btc-blur-content{transition:filter 0.3s;}
  .btc-blur-content.blurred{filter:blur(6px);pointer-events:none;user-select:none;}
  .btc-paywall-inline{display:none;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:10;width:300px;}
  .btc-paywall-inline.show{display:block;}

  /* ══ BTC 신호 팝업 (슬라이드인) ══ */
  .btc-popup{position:fixed;bottom:20px;right:16px;z-index:3000;width:260px;background:linear-gradient(135deg,#1a1a1a,#111);border:1px solid rgba(201,168,76,0.3);border-radius:16px;padding:16px;box-shadow:0 8px 32px rgba(0,0,0,0.7);transform:translateY(120px);opacity:0;transition:transform 0.35s cubic-bezier(0.34,1.56,0.64,1),opacity 0.3s ease;pointer-events:none;}
  .btc-popup.show{transform:translateY(0);opacity:1;pointer-events:auto;}
  .btc-popup-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
  .btc-popup-title{font-size:11px;color:var(--text3);letter-spacing:0.5px;}
  .btc-popup-close{width:22px;height:22px;border-radius:50%;background:rgba(255,255,255,0.06);border:none;color:var(--text3);font-size:11px;cursor:pointer;display:flex;align-items:center;justify-content:center;}
  .btc-popup-body{text-align:center;}
  .btc-popup-dir{font-size:13px;font-weight:700;padding:6px 14px;border-radius:8px;display:inline-block;margin-bottom:8px;}
  .btc-popup-dir.long{background:rgba(224,85,85,0.2);color:var(--red2);border:1px solid rgba(224,85,85,0.4);}
  .btc-popup-dir.short{background:rgba(74,158,255,0.15);color:var(--blue);border:1px solid rgba(74,158,255,0.35);}
  .btc-popup-entry{font-size:20px;font-weight:700;font-family:'JetBrains Mono',monospace;color:var(--gold);}
  .btc-popup-tf{font-size:10px;color:var(--text3);margin-top:4px;}
  .btc-popup-blur{filter:blur(5px);user-select:none;font-size:18px;font-weight:700;color:var(--gold);}
  .btc-popup-lock{font-size:12px;color:var(--text2);margin-top:6px;cursor:pointer;}
  .btc-popup-lock:hover{color:var(--gold);}

  /* ══ 소리 설정 팝업 ══ */
  .sound-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.7);backdrop-filter:blur(3px);z-index:2500;align-items:center;justify-content:center;padding:16px;}
  .sound-overlay.show{display:flex;}
  .sound-box{background:var(--bg2);border:0.5px solid rgba(201,168,76,0.2);border-radius:20px;width:100%;max-width:320px;padding:24px;box-shadow:0 20px 60px rgba(0,0,0,0.8);}
  .sound-box-title{font-size:14px;font-weight:700;color:var(--gold);margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;}
  .sound-toggle-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:16px;border-bottom:0.5px solid var(--border);}
  .sound-toggle-label{font-size:13px;color:var(--text);}
  .sound-switch{position:relative;width:44px;height:24px;cursor:pointer;}
  .sound-switch input{opacity:0;width:0;height:0;position:absolute;}
  .sound-slider{position:absolute;top:0;left:0;right:0;bottom:0;background:var(--bg3);border-radius:24px;transition:0.3s;border:0.5px solid var(--border2);}
  .sound-slider::before{content:'';position:absolute;width:18px;height:18px;border-radius:50%;background:#fff;top:3px;left:3px;transition:0.3s;}
  .sound-switch input:checked+.sound-slider{background:rgba(201,168,76,0.3);border-color:var(--gold);}
  .sound-switch input:checked+.sound-slider::before{transform:translateX(20px);background:var(--gold);}
  .sound-vol-row{margin-bottom:16px;}
  .sound-vol-label{font-size:11px;color:var(--text3);margin-bottom:8px;display:flex;justify-content:space-between;}
  .sound-vol-slider{width:100%;-webkit-appearance:none;height:4px;border-radius:4px;background:var(--bg3);outline:none;border:0.5px solid var(--border2);}
  .sound-vol-slider::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:var(--gold);cursor:pointer;}
  .sound-type-row{margin-bottom:20px;}
  .sound-type-label{font-size:11px;color:var(--text3);margin-bottom:8px;}
  .sound-type-btns{display:flex;gap:6px;}
  .sound-type-btn{flex:1;padding:8px 4px;border-radius:8px;border:0.5px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:11px;font-family:'Noto Sans KR',sans-serif;cursor:pointer;text-align:center;transition:all 0.15s;}
  .sound-type-btn.active{background:rgba(201,168,76,0.12);border-color:var(--gold);color:var(--gold);}
  .sound-preview-row{display:flex;gap:6px;margin-top:6px;}
  .sound-preview-btn{flex:1;padding:6px;border-radius:6px;border:0.5px solid var(--border);background:var(--bg3);color:var(--text3);font-size:10px;cursor:pointer;text-align:center;transition:all 0.15s;}
  .sound-preview-btn:hover{border-color:var(--gold);color:var(--gold);}
  .sound-close-btn{width:100%;padding:10px;border-radius:10px;border:0.5px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:13px;font-family:'Noto Sans KR',sans-serif;cursor:pointer;transition:all 0.15s;}
  .sound-close-btn:hover{border-color:var(--gold);color:var(--gold);}

  /* ══ 크립토 버블맵 ══ */
  .bubble-wrap{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;overflow:hidden;margin-top:20px;}
  .bubble-label{font-size:11px;color:var(--text3);padding:10px 14px;border-bottom:0.5px solid var(--border);}

  /* ══ 매매일지 ══ */
  .journal-login-wrap{display:flex;align-items:center;justify-content:center;min-height:200px;}
  .journal-login-box{background:var(--bg2);border:0.5px solid rgba(201,168,76,0.2);border-radius:20px;padding:32px 28px;width:100%;max-width:320px;text-align:center;}
  .journal-login-title{font-size:15px;font-weight:700;color:var(--gold);margin-bottom:6px;}
  .journal-login-desc{font-size:12px;color:var(--text2);margin-bottom:20px;line-height:1.7;}
  .journal-input{width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 14px;color:var(--text);font-size:13px;font-family:'JetBrains Mono',monospace;margin-bottom:8px;transition:border-color 0.15s;}
  .journal-input:focus{outline:none;border-color:rgba(201,168,76,0.5);}
  .journal-btn{width:100%;background:linear-gradient(135deg,rgba(201,168,76,0.2),rgba(201,168,76,0.1));border:1px solid rgba(201,168,76,0.4);border-radius:10px;padding:11px;color:var(--gold);font-size:13px;font-weight:700;cursor:pointer;font-family:'Noto Sans KR',sans-serif;transition:all 0.15s;margin-bottom:8px;}
  .journal-btn:hover{background:linear-gradient(135deg,rgba(201,168,76,0.3),rgba(201,168,76,0.15));}
  .journal-btn-sec{width:100%;background:transparent;border:0.5px solid var(--border2);border-radius:10px;padding:9px;color:var(--text3);font-size:12px;cursor:pointer;font-family:'Noto Sans KR',sans-serif;transition:all 0.15s;}
  .journal-btn-sec:hover{border-color:var(--gold);color:var(--gold);}
  .journal-error{font-size:11px;color:var(--red2);margin-top:6px;display:none;}
  .journal-error.show{display:block;}
  .journal-main{display:none;}
  .journal-main.show{display:block;}
  .journal-top-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;}
  .journal-user{font-size:12px;color:var(--text3);}
  .journal-user span{color:var(--gold);font-weight:700;}
  .journal-logout{font-size:11px;color:var(--text3);background:transparent;border:0.5px solid var(--border2);border-radius:6px;padding:4px 10px;cursor:pointer;transition:all 0.15s;}
  .journal-logout:hover{border-color:var(--red2);color:var(--red2);}
  .journal-stat-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:12px;}
  .journal-stat-card{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px 16px;}
  .jsc-label{font-size:10px;color:var(--text3);margin-bottom:6px;}
  .jsc-val{font-size:20px;font-weight:700;font-family:'JetBrains Mono',monospace;}
  .jsc-val.up{color:var(--green);}.jsc-val.dn{color:var(--red2);}.jsc-val.neu{color:var(--text);}
  .wr-gauge-wrap{display:flex;align-items:center;gap:10px;margin-top:4px;}
  .wr-gauge-bar{flex:1;height:6px;background:rgba(255,255,255,0.08);border-radius:6px;overflow:hidden;}
  .wr-gauge-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--green),#7bc67e);transition:width 0.5s;}
  .journal-chart-wrap{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:16px;margin-bottom:12px;}
  .jcw-title{font-size:11px;color:var(--text3);margin-bottom:12px;}
  .month-bars{display:flex;align-items:flex-end;gap:4px;height:60px;}
  .month-bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;}
  .month-bar{width:100%;border-radius:3px 3px 0 0;min-height:2px;transition:height 0.4s;}
  .month-bar.up{background:rgba(76,175,125,0.7);}
  .month-bar.dn{background:rgba(224,85,85,0.7);}
  .month-lbl{font-size:9px;color:var(--text3);}
  .journal-add-btn{width:100%;padding:11px;border-radius:10px;border:1px dashed rgba(201,168,76,0.3);background:rgba(201,168,76,0.04);color:var(--gold);font-size:13px;font-family:'Noto Sans KR',sans-serif;cursor:pointer;margin-bottom:12px;transition:all 0.15s;}
  .journal-add-btn:hover{background:rgba(201,168,76,0.08);border-color:var(--gold);}
  .journal-form{background:var(--bg2);border:0.5px solid rgba(201,168,76,0.2);border-radius:14px;padding:20px;margin-bottom:12px;display:none;}
  .journal-form.show{display:block;}
  .journal-form-title{font-size:13px;font-weight:700;color:var(--gold);margin-bottom:14px;}
  .jf-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;}
  .jf-field{display:flex;flex-direction:column;gap:4px;}
  .jf-label{font-size:11px;color:var(--text3);}
  .jf-req{color:var(--red);font-size:9px;margin-left:2px;}
  .jf-input{background:var(--bg3);border:0.5px solid var(--border2);border-radius:8px;padding:9px 11px;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:13px;width:100%;transition:border-color 0.15s;}
  .jf-input:focus{outline:none;border-color:var(--gold);}
  .jf-input::placeholder{color:var(--text3);font-size:11px;}
  .jf-dir-row{display:flex;gap:6px;margin-bottom:8px;}
  .jf-dir-btn{flex:1;padding:9px;border-radius:8px;border:0.5px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:12px;font-weight:700;cursor:pointer;text-align:center;transition:all 0.15s;}
  .jf-dir-btn.long.active{background:rgba(224,85,85,0.15);border-color:rgba(224,85,85,0.5);color:var(--red2);}
  .jf-dir-btn.short.active{background:rgba(74,158,255,0.12);border-color:rgba(74,158,255,0.4);color:var(--blue);}
  .jf-submit{width:100%;padding:11px;border-radius:10px;border:1px solid rgba(201,168,76,0.4);background:linear-gradient(135deg,rgba(201,168,76,0.2),rgba(201,168,76,0.1));color:var(--gold);font-size:13px;font-weight:700;cursor:pointer;font-family:'Noto Sans KR',sans-serif;margin-top:4px;transition:all 0.15s;}
  .jf-cancel{width:100%;padding:9px;border-radius:10px;border:0.5px solid var(--border2);background:transparent;color:var(--text3);font-size:12px;cursor:pointer;font-family:'Noto Sans KR',sans-serif;margin-top:6px;transition:all 0.15s;}
  .journal-list-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
  .journal-list-title{font-size:12px;color:var(--text3);}
  .journal-search{background:var(--bg3);border:0.5px solid var(--border2);border-radius:8px;padding:7px 11px;color:var(--text);font-size:12px;width:120px;transition:border-color 0.15s;}
  .journal-search:focus{outline:none;border-color:var(--gold);}
  .journal-filter-row{display:flex;gap:6px;margin-bottom:8px;}
  .journal-trade-list{display:flex;flex-direction:column;gap:8px;}
  .journal-trade-item{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px 16px;}
  .jti-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
  .jti-left{display:flex;align-items:center;gap:8px;}
  .jti-badge-long{font-size:10px;font-weight:700;padding:3px 8px;border-radius:5px;background:rgba(224,85,85,0.15);color:var(--red2);border:0.5px solid rgba(224,85,85,0.35);}
  .jti-badge-short{font-size:10px;font-weight:700;padding:3px 8px;border-radius:5px;background:rgba(74,158,255,0.12);color:var(--blue);border:0.5px solid rgba(74,158,255,0.3);}
  .jti-ticker{font-size:13px;font-weight:700;color:var(--text);}
  .jti-status{font-size:10px;padding:2px 7px;border-radius:4px;}
  .jti-status.running{background:rgba(201,168,76,0.1);color:var(--gold);}
  .jti-status.win{background:rgba(76,175,125,0.12);color:var(--green);}
  .jti-status.lose{background:rgba(224,85,85,0.1);color:var(--red2);}
  .jti-bottom{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:8px;}
  .jti-field{display:flex;flex-direction:column;gap:2px;}
  .jti-flabel{font-size:10px;color:var(--text3);}
  .jti-fval{font-size:12px;font-family:'JetBrains Mono',monospace;color:var(--text);}
  .jti-fval.up{color:var(--green);}.jti-fval.dn{color:var(--red2);}
  .jti-actions{display:flex;gap:6px;margin-top:10px;}
  .jti-close-btn{font-size:11px;padding:5px 10px;border-radius:6px;border:0.5px solid rgba(76,175,125,0.3);background:rgba(76,175,125,0.08);color:var(--green);cursor:pointer;transition:all 0.15s;}
  .jti-del-btn{font-size:11px;padding:5px 10px;border-radius:6px;border:0.5px solid var(--border2);background:var(--bg3);color:var(--text3);cursor:pointer;transition:all 0.15s;}
  .jti-del-btn:hover{border-color:var(--red2);color:var(--red2);}
  .journal-empty{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:32px;text-align:center;color:var(--text3);font-size:12px;}
  .ticker-wr-list{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:12px;}
  .ticker-wr-item{display:flex;align-items:center;padding:10px 14px;border-bottom:0.5px solid var(--border);gap:8px;}
  .ticker-wr-item:last-child{border-bottom:none;}
  .twr-name{font-size:12px;color:var(--text);font-weight:500;min-width:60px;}
  .twr-bar-wrap{flex:1;height:4px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;}
  .twr-bar-fill{height:100%;border-radius:4px;background:var(--green);}
  .twr-pct{font-size:11px;font-family:'JetBrains Mono',monospace;color:var(--text2);min-width:36px;text-align:right;}
"""

html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
print("[1] CSS 추가 완료")

# ═══════════════════════════════════════════════════
# [2] 탭 버튼 - 매매일지 추가
# ═══════════════════════════════════════════════════
html = html.replace(
    "onclick=\"switchTab('calc',this)\">🧮 계산기</button>",
    "onclick=\"switchTab('calc',this)\">🧮 계산기</button>\n  <button class=\"tab-btn\" id=\"tab-btn-journal\" onclick=\"switchTab('journal',this)\">📒 매매일지</button>"
)
print("[2] 탭 버튼 추가 완료")

# ═══════════════════════════════════════════════════
# [3] 소리 버튼 - toggleSound → showSoundPopup
# ═══════════════════════════════════════════════════
html = html.replace(
    'onclick="toggleSound()" title="알림음 ON/OFF"',
    'onclick="showSoundPopup()" title="알림음 설정"'
)
print("[3] 소리 버튼 변경 완료")

# ═══════════════════════════════════════════════════
# [4] BTC 탭 제목 변경 + 블러 래퍼 + 버블맵 추가
# ═══════════════════════════════════════════════════
html = html.replace(
    '<div class="screen-title">비트코인 롱/숏 신호</div>',
    '<div class="screen-title">비트코인 롱/숏 알림</div>'
)

OLD_BTC_CONTENT = '<div id="btc-signal-content"><div class="loading-box">신호를 불러오는 중입니다...</div></div>'
NEW_BTC_CONTENT = '''<div class="btc-blur-wrap" id="btc-blur-wrap">
    <div class="btc-blur-content" id="btc-blur-content">
      <div id="btc-signal-content"><div class="loading-box">신호를 불러오는 중입니다...</div></div>
    </div>
    <div class="btc-paywall-inline" id="btc-paywall-inline">
      <div class="paywall-box" onclick="event.stopPropagation()">
        <div class="paywall-icon">🔒</div>
        <div class="paywall-title">멤버십 전용 데이터</div>
        <div class="paywall-desc">팬딩 멤버십 가입 후<br>비트코인 신호를<br>열람할 수 있습니다.</div>
        <input class="paywall-input" id="btc-pw-input2" type="password" placeholder="••••" maxlength="10" onkeydown="if(event.key==='Enter')checkBtcPasswordInline()">
        <button class="paywall-btn" onclick="checkBtcPasswordInline()">비밀번호 입력</button>
        <div class="paywall-error" id="btc-pw-error2">비밀번호가 틀렸습니다.</div>
        <div class="paywall-sub"><a href="https://fanding.kr/@bzcLu6QCTdMe/membership/" target="_blank" onclick="event.stopPropagation()">팬딩 멤버십 구독하기 →</a></div>
      </div>
    </div>
  </div>
  <!-- 크립토 버블맵 -->
  <div class="bubble-wrap">
    <div class="bubble-label">🫧 크립토 버블맵 &nbsp;·&nbsp; 시총 기준 · 색상 = 등락률 · CryptoBubbles</div>
    <iframe src="https://cryptobubbles.net" style="width:100%;height:500px;border:none;display:block;" loading="lazy" title="크립토 버블맵"></iframe>
  </div>'''

html = html.replace(OLD_BTC_CONTENT, NEW_BTC_CONTENT)
print("[4] BTC 탭 블러 + 버블맵 추가 완료")

# ═══════════════════════════════════════════════════
# [5] 알트코인 RSI 필터 맨 마지막으로 이동
# ═══════════════════════════════════════════════════
OLD_FILTER = """    <button class="filter-btn" id="af-trend" onclick="filterAltcoin('trend')">🚀 추세전환</button>
    <button class="filter-btn" id="af-ma" onclick="filterAltcoin('ma')">🔀 이평선 수렴</button>
    <button class="filter-btn" id="af-rsi" onclick="filterAltcoin('rsi')">📈 RSI 다이버전스</button>
    <button class="filter-btn" id="af-kiz" onclick="filterAltcoin('kiz')">⚡ 기자모리</button>
    <button class="filter-btn" id="af-wyc" onclick="filterAltcoin('wyc')">🎯 와이코프</button>"""

NEW_FILTER = """    <button class="filter-btn" id="af-trend" onclick="filterAltcoin('trend')">🚀 추세전환</button>
    <button class="filter-btn" id="af-ma" onclick="filterAltcoin('ma')">🔀 이평선 수렴</button>
    <button class="filter-btn" id="af-kiz" onclick="filterAltcoin('kiz')">⚡ 기자모리</button>
    <button class="filter-btn" id="af-wyc" onclick="filterAltcoin('wyc')">🎯 와이코프</button>
    <button class="filter-btn" id="af-rsi" onclick="filterAltcoin('rsi')">📈 RSI 다이버전스</button>"""

html = html.replace(OLD_FILTER, NEW_FILTER)
print("[5] RSI 필터 순서 변경 완료")

# ═══════════════════════════════════════════════════
# [6] 매매일지 탭 HTML - 계산기 탭 뒤에 추가
# ═══════════════════════════════════════════════════
JOURNAL_TAB_HTML = """

<!-- ══ 매매일지 탭 ══ -->
<div class="tab-content" id="tab-journal">
<div class="container" style="padding-top:16px;">

  <!-- 로그인 영역 -->
  <div class="journal-login-wrap" id="journal-login-wrap">
    <div>
      <!-- 로그인 폼 -->
      <div id="journal-form-login">
        <div class="journal-login-box">
          <div class="journal-login-title">📒 매매일지</div>
          <div class="journal-login-desc">팬딩 아이디와<br>직접 설정한 비밀번호로 로그인하세요.</div>
          <input class="journal-input" id="jl-id" type="text" placeholder="팬딩 아이디" autocomplete="username">
          <input class="journal-input" id="jl-pw" type="password" placeholder="비밀번호" autocomplete="current-password" onkeydown="if(event.key==='Enter')journalLogin()">
          <button class="journal-btn" onclick="journalLogin()">로그인</button>
          <button class="journal-btn-sec" onclick="showJournalRegister()">처음 오셨나요? 가입하기</button>
          <div class="journal-error" id="journal-login-error"></div>
        </div>
      </div>

      <!-- 가입 폼 -->
      <div id="journal-form-register" style="display:none;">
        <div class="journal-login-box">
          <div class="journal-login-title">📒 매매일지 가입</div>
          <div class="journal-login-desc">팬딩 아이디 + 직접 설정할 비밀번호<br>비밀번호는 4자 이상</div>
          <input class="journal-input" id="jr-id" type="text" placeholder="팬딩 아이디" autocomplete="username">
          <input class="journal-input" id="jr-pw" type="password" placeholder="비밀번호 (4자 이상)" autocomplete="new-password">
          <input class="journal-input" id="jr-pw2" type="password" placeholder="비밀번호 확인" autocomplete="new-password" onkeydown="if(event.key==='Enter')journalRegister()">
          <button class="journal-btn" onclick="journalRegister()">가입하기</button>
          <button class="journal-btn-sec" onclick="showJournalLogin()">← 로그인으로</button>
          <div class="journal-error" id="journal-register-error"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- 메인 영역 (로그인 후) -->
  <div class="journal-main" id="journal-main">
    <div class="journal-top-bar">
      <div class="journal-user">안녕하세요, <span id="journal-username"></span></div>
      <button class="journal-logout" onclick="journalLogout()">로그아웃</button>
    </div>

    <!-- 통계 대시보드 -->
    <div class="journal-stat-grid" id="journal-stats">
      <div class="journal-stat-card">
        <div class="jsc-label">승률</div>
        <div class="jsc-val neu" id="jstat-wr">—</div>
        <div class="wr-gauge-wrap"><div class="wr-gauge-bar"><div class="wr-gauge-fill" id="jstat-wr-fill" style="width:0%"></div></div></div>
      </div>
      <div class="journal-stat-card">
        <div class="jsc-label">총 손익</div>
        <div class="jsc-val neu" id="jstat-pnl">—</div>
      </div>
      <div class="journal-stat-card">
        <div class="jsc-label">평균 수익률</div>
        <div class="jsc-val neu" id="jstat-avg">—</div>
      </div>
      <div class="journal-stat-card">
        <div class="jsc-label">연속 승/패</div>
        <div class="jsc-val neu" id="jstat-streak">—</div>
      </div>
    </div>

    <!-- 월별 손익 차트 -->
    <div class="journal-chart-wrap">
      <div class="jcw-title">📊 월별 손익</div>
      <div class="month-bars" id="journal-month-chart"></div>
    </div>

    <!-- 종목별 승률 -->
    <div id="journal-ticker-wr-wrap" style="display:none;">
      <div class="jsc-label" style="margin-bottom:8px;font-size:11px;color:var(--text3);">📈 종목별 승률</div>
      <div class="ticker-wr-list" id="journal-ticker-wr"></div>
    </div>

    <!-- 매매 입력 버튼 -->
    <button class="journal-add-btn" onclick="toggleJournalForm()">+ 매매 기록하기</button>

    <!-- 매매 입력 폼 -->
    <div class="journal-form" id="journal-add-form">
      <div class="journal-form-title">새 매매 기록</div>
      <div class="jf-grid">
        <div class="jf-field">
          <div class="jf-label">날짜 <span class="jf-req">●</span></div>
          <input class="jf-input" id="jf-date" type="date">
        </div>
        <div class="jf-field">
          <div class="jf-label">종목 <span class="jf-req">●</span></div>
          <input class="jf-input" id="jf-ticker" type="text" placeholder="BTCUSDT">
        </div>
      </div>
      <div class="jf-label" style="margin-bottom:6px;">방향 <span class="jf-req">●</span></div>
      <div class="jf-dir-row">
        <button class="jf-dir-btn long active" id="jf-long-btn" onclick="setJournalDir('long')">🔴 LONG</button>
        <button class="jf-dir-btn short" id="jf-short-btn" onclick="setJournalDir('short')">🔵 SHORT</button>
      </div>
      <div class="jf-grid">
        <div class="jf-field">
          <div class="jf-label">진입가 <span class="jf-req">●</span></div>
          <input class="jf-input" id="jf-entry" type="number" placeholder="필수">
        </div>
        <div class="jf-field">
          <div class="jf-label">투자금액 (USDT)</div>
          <input class="jf-input" id="jf-amount" type="number" placeholder="선택">
        </div>
      </div>
      <div class="jf-grid">
        <div class="jf-field">
          <div class="jf-label">청산가</div>
          <input class="jf-input" id="jf-exit" type="number" placeholder="청산 후 입력">
        </div>
        <div class="jf-field">
          <div class="jf-label">메모</div>
          <input class="jf-input" id="jf-memo" type="text" placeholder="진입 이유 (선택)">
        </div>
      </div>
      <div class="journal-error" id="journal-add-error"></div>
      <button class="jf-submit" onclick="journalAdd()">저장</button>
      <button class="jf-cancel" onclick="toggleJournalForm()">취소</button>
    </div>

    <!-- 매매 목록 -->
    <div class="journal-list-header">
      <div class="journal-list-title">매매 목록</div>
      <input class="journal-search" id="journal-search" type="text" placeholder="종목 검색" oninput="renderJournalList()">
    </div>
    <div class="journal-filter-row">
      <button class="filter-btn active" id="jf-all" onclick="setJournalFilter('all')">전체</button>
      <button class="filter-btn" id="jf-open" onclick="setJournalFilter('open')">진행중</button>
      <button class="filter-btn" id="jf-win" onclick="setJournalFilter('win')">✅ 수익</button>
      <button class="filter-btn" id="jf-lose" onclick="setJournalFilter('lose')">❌ 손실</button>
    </div>
    <div class="journal-trade-list" id="journal-trade-list">
      <div class="journal-empty">매매 기록이 없습니다.</div>
    </div>
  </div>

</div>
</div>"""

# 계산기 탭 닫는 태그 뒤에 삽입
html = html.replace('<!-- ══ 매뉴얼 팝업 ══ -->', JOURNAL_TAB_HTML + '\n\n<!-- ══ 매뉴얼 팝업 ══ -->', 1)
print("[6] 매매일지 탭 HTML 추가 완료")

# ═══════════════════════════════════════════════════
# [7] BTC 팝업 HTML + 소리 설정 팝업 HTML 추가
# ═══════════════════════════════════════════════════
POPUP_HTML = """
<!-- ══ BTC 신호 팝업 (슬라이드인) ══ -->
<div class="btc-popup" id="btc-slide-popup">
  <div class="btc-popup-header">
    <div class="btc-popup-title">🔔 비트코인 신호</div>
    <button class="btc-popup-close" onclick="closeBtcPopup()">✕</button>
  </div>
  <div class="btc-popup-body" id="btc-popup-body">
    <div class="btc-popup-dir long" id="btc-popup-dir">🔴 LONG</div>
    <div class="btc-popup-entry" id="btc-popup-entry">—</div>
    <div class="btc-popup-tf" id="btc-popup-tf">10M</div>
  </div>
</div>

<!-- ══ 소리 설정 팝업 ══ -->
<div class="sound-overlay" id="sound-overlay" onclick="hideSoundPopup(event)">
  <div class="sound-box" onclick="event.stopPropagation()">
    <div class="sound-box-title">
      🔔 알림음 설정
      <button class="paywall-close" onclick="hideSoundPopup(null)">✕</button>
    </div>
    <div class="sound-toggle-row">
      <div class="sound-toggle-label">알림음 ON/OFF</div>
      <label class="sound-switch">
        <input type="checkbox" id="sound-switch-cb" onchange="onSoundToggle(this.checked)">
        <span class="sound-slider"></span>
      </label>
    </div>
    <div class="sound-vol-row">
      <div class="sound-vol-label"><span>볼륨</span><span id="sound-vol-display">50%</span></div>
      <input class="sound-vol-slider" type="range" min="0" max="100" value="50" id="sound-vol-range" oninput="onVolumeChange(this.value)">
    </div>
    <div class="sound-type-row">
      <div class="sound-type-label">알림음 종류</div>
      <div class="sound-type-btns">
        <button class="sound-type-btn active" id="stype-chime" onclick="setSoundType('chime',this)">차임</button>
        <button class="sound-type-btn" id="stype-piano" onclick="setSoundType('piano',this)">피아노</button>
        <button class="sound-type-btn" id="stype-elec" onclick="setSoundType('elec',this)">전자음</button>
      </div>
      <div class="sound-preview-row">
        <button class="sound-preview-btn" onclick="previewSound('chime')">▶ 차임</button>
        <button class="sound-preview-btn" onclick="previewSound('piano')">▶ 피아노</button>
        <button class="sound-preview-btn" onclick="previewSound('elec')">▶ 전자음</button>
      </div>
    </div>
    <button class="sound-close-btn" onclick="hideSoundPopup(null)">확인</button>
  </div>
</div>
"""

html = html.replace('<footer class="site-footer">', POPUP_HTML + '\n<footer class="site-footer">', 1)
print("[7] 팝업 HTML 추가 완료")

# ═══════════════════════════════════════════════════
# [8] JS 추가 - </script> 바로 앞 (메인 스크립트 끝 부분)
# 기존 toggleSound 함수 교체 + 새 함수 추가
# ═══════════════════════════════════════════════════

# 기존 toggleSound 함수 교체
OLD_TOGGLE = """function toggleSound(){
  soundEnabled=!soundEnabled;
  localStorage.setItem('sound_enabled',soundEnabled?'1':'0');
  var btn=document.getElementById('sound-toggle-btn');
  if(btn){btn.textContent=soundEnabled?'🔔':'🔕';btn.style.color=soundEnabled?'var(--gold)':'var(--text3)';}
}"""

NEW_TOGGLE = """function toggleSound(){
  soundEnabled=!soundEnabled;
  localStorage.setItem('sound_enabled',soundEnabled?'1':'0');
  var btn=document.getElementById('sound-toggle-btn');
  if(btn){btn.textContent=soundEnabled?'🔔':'🔕';btn.style.color=soundEnabled?'var(--gold)':'var(--text3)';}
}
function showSoundPopup(){
  var cb=document.getElementById('sound-switch-cb');
  if(cb)cb.checked=soundEnabled;
  var vol=localStorage.getItem('sound_volume')||'50';
  var rng=document.getElementById('sound-vol-range');
  var disp=document.getElementById('sound-vol-display');
  if(rng)rng.value=vol;
  if(disp)disp.textContent=vol+'%';
  var stype=localStorage.getItem('sound_type')||'chime';
  ['chime','piano','elec'].forEach(function(t){
    var btn=document.getElementById('stype-'+t);
    if(btn)btn.classList.toggle('active',t===stype);
  });
  var overlay=document.getElementById('sound-overlay');
  if(overlay)overlay.classList.add('show');
}
function hideSoundPopup(e){
  if(e&&e.target!==document.getElementById('sound-overlay'))return;
  var overlay=document.getElementById('sound-overlay');
  if(overlay)overlay.classList.remove('show');
}
function onSoundToggle(checked){
  soundEnabled=checked;
  localStorage.setItem('sound_enabled',checked?'1':'0');
  var btn=document.getElementById('sound-toggle-btn');
  if(btn){btn.textContent=checked?'🔔':'🔕';btn.style.color=checked?'var(--gold)':'var(--text3)';}
}
function onVolumeChange(val){
  localStorage.setItem('sound_volume',val);
  var disp=document.getElementById('sound-vol-display');
  if(disp)disp.textContent=val+'%';
  soundVolume=parseInt(val)/100;
}
var soundVolume=parseFloat(localStorage.getItem('sound_volume')||'50')/100;
var currentSoundType=localStorage.getItem('sound_type')||'chime';
function setSoundType(type,btn){
  currentSoundType=type;
  localStorage.setItem('sound_type',type);
  ['chime','piano','elec'].forEach(function(t){
    var b=document.getElementById('stype-'+t);
    if(b)b.classList.toggle('active',t===type);
  });
}
function previewSound(type){
  var saved=currentSoundType;
  currentSoundType=type;
  playSound('newSignal');
  currentSoundType=saved;
}"""

html = html.replace(OLD_TOGGLE, NEW_TOGGLE)
print("[8a] toggleSound 교체 완료")

# playSound 함수에 볼륨/타입 반영
OLD_PLAY = """function playSound(key){
  if(!soundEnabled)return;
  try{
    var ctx=getAudioCtx();
    var cfg=SOUND_CONFIG[key];
    if(!cfg)return;
    var t=ctx.currentTime;
    cfg.notes.forEach(function(freq,i){
      var osc=ctx.createOscillator();
      var gain=ctx.createGain();
      osc.connect(gain);gain.connect(ctx.destination);
      osc.type=cfg.type;
      var st=t+i*(cfg.duration+cfg.gap);
      osc.frequency.setValueAtTime(freq,st);
      gain.gain.setValueAtTime(cfg.volume,st);
      gain.gain.exponentialRampToValueAtTime(0.001,st+cfg.duration);
      osc.start(st);osc.stop(st+cfg.duration);
    });
  }catch(e){console.log('sound:',e);}
}"""

NEW_PLAY = """function playSound(key){
  if(!soundEnabled)return;
  try{
    var ctx=getAudioCtx();
    var cfg=SOUND_CONFIG[key];
    if(!cfg)return;
    // 타입별 오실레이터 설정
    var oscType = currentSoundType==='elec'?'square':(currentSoundType==='piano'?'triangle':'sine');
    var vol = (soundVolume!==undefined?soundVolume:0.5)*cfg.volume;
    var t=ctx.currentTime;
    cfg.notes.forEach(function(freq,i){
      var osc=ctx.createOscillator();
      var gain=ctx.createGain();
      osc.connect(gain);gain.connect(ctx.destination);
      osc.type=oscType;
      var st=t+i*(cfg.duration+cfg.gap);
      osc.frequency.setValueAtTime(freq,st);
      gain.gain.setValueAtTime(vol,st);
      gain.gain.exponentialRampToValueAtTime(0.001,st+cfg.duration);
      osc.start(st);osc.stop(st+cfg.duration);
    });
  }catch(e){console.log('sound:',e);}
}"""

html = html.replace(OLD_PLAY, NEW_PLAY)
print("[8b] playSound 볼륨/타입 반영 완료")

# ═══════════════════════════════════════════════════
# [9] BTC 팝업 로직 + BTC 블러 + 매매일지 JS 추가
# ═══════════════════════════════════════════════════
NEW_JS = """
// ══════════════════════════════════════════════
// BTC 탭 블러 + 인라인 페이월
// ══════════════════════════════════════════════
function initBtcBlur(){
  var unlocked=localStorage.getItem('rsi_unlocked')==='1';
  if(!unlocked){
    var content=document.getElementById('btc-blur-content');
    var paywall=document.getElementById('btc-paywall-inline');
    if(content)content.classList.add('blurred');
    if(paywall)paywall.classList.add('show');
  }
}
function checkBtcPasswordInline(){
  var input=document.getElementById('btc-pw-input2');
  var error=document.getElementById('btc-pw-error2');
  if(!input)return;
  if(input.value===RSI_PW){
    rsiUnlocked=true;
    localStorage.setItem('rsi_unlocked','1');
    var content=document.getElementById('btc-blur-content');
    var paywall=document.getElementById('btc-paywall-inline');
    if(content)content.classList.remove('blurred');
    if(paywall)paywall.classList.remove('show');
    unlockRsi();
    loadBtcSignals();
    if(error)error.classList.remove('show');
  }else{
    input.value='';
    if(error)error.classList.add('show');
    setTimeout(function(){if(error)error.classList.remove('show');},2000);
  }
}

// ══════════════════════════════════════════════
// BTC 슬라이드 팝업
// ══════════════════════════════════════════════
var btcPopupTimer=null;
function showBtcSlidePopup(signal){
  var popup=document.getElementById('btc-slide-popup');
  var dirEl=document.getElementById('btc-popup-dir');
  var entryEl=document.getElementById('btc-popup-entry');
  var tfEl=document.getElementById('btc-popup-tf');
  if(!popup)return;
  var isLong=signal.type==='LONG';
  var isUnlocked=localStorage.getItem('rsi_unlocked')==='1';
  if(dirEl){dirEl.textContent=isLong?'🔴 LONG':'🔵 SHORT';dirEl.className='btc-popup-dir '+(isLong?'long':'short');}
  if(entryEl){
    if(isUnlocked){entryEl.textContent=signal.entry||'—';entryEl.className='btc-popup-entry';}
    else{entryEl.textContent='••••';entryEl.className='btc-popup-entry btc-popup-blur';}
  }
  if(tfEl)tfEl.textContent=signal.tf||'—';
  popup.classList.add('show');
  if(btcPopupTimer)clearTimeout(btcPopupTimer);
  btcPopupTimer=setTimeout(closeBtcPopup,3000);
}
function closeBtcPopup(){
  var popup=document.getElementById('btc-slide-popup');
  if(popup)popup.classList.remove('show');
  if(btcPopupTimer){clearTimeout(btcPopupTimer);btcPopupTimer=null;}
}

// checkNewBtcSignal 오버라이드 (팝업 포함)
var _origCheckNewBtcSignal=checkNewBtcSignal;
checkNewBtcSignal=function(signals){
  if(!signals||signals.length===0)return;
  var s=signals[0];
  var key=s.type+'_'+s.time+'_'+s.tf;
  if(lastBtcSignalKey===null){lastBtcSignalKey=key;return;}
  if(key!==lastBtcSignalKey){
    if(s.type==='LONG')playSound('btcLong');
    else if(s.type==='SHORT')playSound('btcShort');
    showBtcSlidePopup(s);
    lastBtcSignalKey=key;
  }
};

// ══════════════════════════════════════════════
// 다이버전스 통합 표시 (sig_type 통합)
// Bull+HiddenBull → 상승 다이버전스
// Bear+HiddenBear → 하락 다이버전스
// ══════════════════════════════════════════════
// sigMap에 rsi_bull/rsi_hidden_bull 매핑 추가
sigMap['rsi_bull']        = {label:'상승 다이버전스', cls:'sig-rsi'};
sigMap['rsi_hidden_bull'] = {label:'상승 다이버전스', cls:'sig-rsi'};
sigMap['rsi_bear']        = {label:'하락 다이버전스', cls:'sig-rsi'};
sigMap['rsi_hidden_bear'] = {label:'하락 다이버전스', cls:'sig-rsi'};

// ══════════════════════════════════════════════
// switchTab 확장 - 매매일지 탭
// ══════════════════════════════════════════════
var _origSwitchTab=switchTab;
switchTab=function(tab,btn){
  _origSwitchTab(tab,btn);
  if(tab==='btc'){initBtcBlur();}
  if(tab==='journal'){initJournal();}
};

// ══════════════════════════════════════════════
// 매매일지
// ══════════════════════════════════════════════
var TRADE_API='https://chartist-insight.com/trade';
var journalUser=null;
var journalPw=null;
var journalTrades=[];
var journalFilter='all';
var journalDir='long';
var journalFormOpen=false;

function initJournal(){
  var saved=localStorage.getItem('journal_user');
  var savedPw=localStorage.getItem('journal_pw');
  if(saved&&savedPw){
    journalUser=saved;journalPw=savedPw;
    loadJournalTrades();
    showJournalMain();
  }
}

function showJournalLogin(){
  document.getElementById('journal-form-login').style.display='block';
  document.getElementById('journal-form-register').style.display='none';
}
function showJournalRegister(){
  document.getElementById('journal-form-login').style.display='none';
  document.getElementById('journal-form-register').style.display='block';
}

function journalLogin(){
  var id=(document.getElementById('jl-id').value||'').trim();
  var pw=(document.getElementById('jl-pw').value||'').trim();
  var err=document.getElementById('journal-login-error');
  if(!id||!pw){if(err){err.textContent='아이디와 비번을 입력해주세요.';err.classList.add('show');}return;}
  fetch(TRADE_API+'/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fanding_id:id,password:pw})})
    .then(function(r){return r.json();})
    .then(function(d){
      if(d.ok){
        journalUser=id;journalPw=pw;
        localStorage.setItem('journal_user',id);
        localStorage.setItem('journal_pw',pw);
        loadJournalTrades();
        showJournalMain();
        if(err)err.classList.remove('show');
      }else{
        if(err){err.textContent=d.msg||'로그인 실패';err.classList.add('show');}
      }
    })
    .catch(function(){if(err){err.textContent='서버 연결 오류';err.classList.add('show');}});
}

function journalRegister(){
  var id=(document.getElementById('jr-id').value||'').trim();
  var pw=(document.getElementById('jr-pw').value||'').trim();
  var pw2=(document.getElementById('jr-pw2').value||'').trim();
  var err=document.getElementById('journal-register-error');
  if(!id||!pw){if(err){err.textContent='아이디와 비번을 입력해주세요.';err.classList.add('show');}return;}
  if(pw!==pw2){if(err){err.textContent='비밀번호가 일치하지 않습니다.';err.classList.add('show');}return;}
  if(pw.length<4){if(err){err.textContent='비밀번호는 4자 이상이어야 합니다.';err.classList.add('show');}return;}
  fetch(TRADE_API+'/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fanding_id:id,password:pw})})
    .then(function(r){return r.json();})
    .then(function(d){
      if(d.ok){
        journalUser=id;journalPw=pw;
        localStorage.setItem('journal_user',id);
        localStorage.setItem('journal_pw',pw);
        journalTrades=[];
        showJournalMain();
        if(err)err.classList.remove('show');
      }else{
        if(err){err.textContent=d.msg||'가입 실패';err.classList.add('show');}
      }
    })
    .catch(function(){if(err){err.textContent='서버 연결 오류';err.classList.add('show');}});
}

function journalLogout(){
  journalUser=null;journalPw=null;journalTrades=[];
  localStorage.removeItem('journal_user');
  localStorage.removeItem('journal_pw');
  var main=document.getElementById('journal-main');
  var loginWrap=document.getElementById('journal-login-wrap');
  if(main)main.classList.remove('show');
  if(loginWrap)loginWrap.style.display='flex';
  showJournalLogin();
}

function showJournalMain(){
  var loginWrap=document.getElementById('journal-login-wrap');
  var main=document.getElementById('journal-main');
  if(loginWrap)loginWrap.style.display='none';
  if(main)main.classList.add('show');
  var unEl=document.getElementById('journal-username');
  if(unEl)unEl.textContent=journalUser;
  // 오늘 날짜 기본값
  var dateEl=document.getElementById('jf-date');
  if(dateEl){
    var now=new Date();
    var y=now.getFullYear();
    var m=String(now.getMonth()+1).padStart(2,'0');
    var d=String(now.getDate()).padStart(2,'0');
    dateEl.value=y+'-'+m+'-'+d;
  }
}

function loadJournalTrades(){
  if(!journalUser||!journalPw)return;
  fetch(TRADE_API+'/list',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fanding_id:journalUser,password:journalPw})})
    .then(function(r){return r.json();})
    .then(function(d){
      if(d.ok){journalTrades=d.trades||[];renderJournalStats();renderJournalList();}
    })
    .catch(function(){});
}

function renderJournalStats(){
  var closed=journalTrades.filter(function(t){return t.status==='closed'&&t.pnl_pct!==null;});
  var wins=closed.filter(function(t){return t.pnl_pct>0;});
  var wr=closed.length>0?Math.round(wins.length/closed.length*100):0;
  var totalPnl=closed.reduce(function(s,t){return s+(t.pnl_amount||0);},0);
  var avgPct=closed.length>0?closed.reduce(function(s,t){return s+(t.pnl_pct||0);},0)/closed.length:0;
  // 연속 승패
  var streak=0,streakType='';
  for(var i=0;i<closed.length;i++){
    var w=closed[i].pnl_pct>0;
    if(i===0){streak=1;streakType=w?'win':'lose';}
    else if((w&&streakType==='win')||(!w&&streakType==='lose')){streak++;}
    else break;
  }
  var wrEl=document.getElementById('jstat-wr');
  var fillEl=document.getElementById('jstat-wr-fill');
  var pnlEl=document.getElementById('jstat-pnl');
  var avgEl=document.getElementById('jstat-avg');
  var strkEl=document.getElementById('jstat-streak');
  if(wrEl){wrEl.textContent=closed.length>0?wr+'%':'—';wrEl.className='jsc-val '+(wr>=50?'up':(closed.length>0?'dn':'neu'));}
  if(fillEl)fillEl.style.width=wr+'%';
  if(pnlEl){pnlEl.textContent=closed.length>0?(totalPnl>=0?'+':'')+totalPnl.toFixed(2)+' USDT':'—';pnlEl.className='jsc-val '+(totalPnl>0?'up':totalPnl<0?'dn':'neu');}
  if(avgEl){avgEl.textContent=closed.length>0?(avgPct>=0?'+':'')+avgPct.toFixed(2)+'%':'—';avgEl.className='jsc-val '+(avgPct>0?'up':avgPct<0?'dn':'neu');}
  if(strkEl){strkEl.textContent=streak>0?(streakType==='win'?'✅ '+streak+'연승':'❌ '+streak+'연패'):'—';}

  // 월별 차트
  renderMonthChart();

  // 종목별 승률
  renderTickerWr();
}

function renderMonthChart(){
  var el=document.getElementById('journal-month-chart');
  if(!el)return;
  var closed=journalTrades.filter(function(t){return t.status==='closed'&&t.pnl_amount!==null;});
  var monthMap={};
  closed.forEach(function(t){
    var d=t.date||'';
    if(d.length>=7){var m=d.substring(0,7);monthMap[m]=(monthMap[m]||0)+t.pnl_amount;}
  });
  var months=Object.keys(monthMap).sort().slice(-6);
  if(months.length===0){el.innerHTML='<div style="font-size:11px;color:var(--text3);padding:16px;">데이터 없음</div>';return;}
  var maxAbs=Math.max.apply(null,months.map(function(m){return Math.abs(monthMap[m]);}));
  if(maxAbs===0)maxAbs=1;
  var html='';
  months.forEach(function(m){
    var v=monthMap[m];
    var h=Math.max(4,Math.round(Math.abs(v)/maxAbs*56));
    var cls=v>=0?'up':'dn';
    var lbl=m.substring(5);
    html+='<div class="month-bar-wrap"><div class="month-bar '+cls+'" style="height:'+h+'px;"></div><div class="month-lbl">'+lbl+'</div></div>';
  });
  el.innerHTML=html;
}

function renderTickerWr(){
  var wrap=document.getElementById('journal-ticker-wr-wrap');
  var list=document.getElementById('journal-ticker-wr');
  if(!wrap||!list)return;
  var closed=journalTrades.filter(function(t){return t.status==='closed'&&t.pnl_pct!==null;});
  var tickerMap={};
  closed.forEach(function(t){
    var tk=t.ticker||'—';
    if(!tickerMap[tk])tickerMap[tk]={win:0,total:0};
    tickerMap[tk].total++;
    if(t.pnl_pct>0)tickerMap[tk].win++;
  });
  var tickers=Object.keys(tickerMap).filter(function(k){return tickerMap[k].total>=1;});
  if(tickers.length===0){wrap.style.display='none';return;}
  wrap.style.display='block';
  tickers.sort(function(a,b){return tickerMap[b].win/tickerMap[b].total-tickerMap[a].win/tickerMap[a].total;});
  var html='';
  tickers.slice(0,8).forEach(function(tk){
    var wr=Math.round(tickerMap[tk].win/tickerMap[tk].total*100);
    html+='<div class="ticker-wr-item"><div class="twr-name">'+tk+'</div><div class="twr-bar-wrap"><div class="twr-bar-fill" style="width:'+wr+'%"></div></div><div class="twr-pct">'+wr+'%</div></div>';
  });
  list.innerHTML=html;
}

function setJournalDir(dir){
  journalDir=dir;
  var longBtn=document.getElementById('jf-long-btn');
  var shortBtn=document.getElementById('jf-short-btn');
  if(longBtn)longBtn.className='jf-dir-btn long'+(dir==='long'?' active':'');
  if(shortBtn)shortBtn.className='jf-dir-btn short'+(dir==='short'?' active':'');
}

function toggleJournalForm(){
  journalFormOpen=!journalFormOpen;
  var form=document.getElementById('journal-add-form');
  if(form)form.classList.toggle('show',journalFormOpen);
}

function journalAdd(){
  var date=(document.getElementById('jf-date').value||'').trim();
  var ticker=(document.getElementById('jf-ticker').value||'').trim().toUpperCase();
  var entry=document.getElementById('jf-entry').value;
  var amount=document.getElementById('jf-amount').value;
  var exitP=document.getElementById('jf-exit').value;
  var memo=(document.getElementById('jf-memo').value||'').trim();
  var err=document.getElementById('journal-add-error');
  if(!date||!ticker||!entry){if(err){err.textContent='날짜, 종목, 진입가는 필수입니다.';err.classList.add('show');}return;}
  var body={fanding_id:journalUser,password:journalPw,date:date,ticker:ticker,direction:journalDir,entry:parseFloat(entry)};
  if(amount)body.amount=parseFloat(amount);
  if(exitP)body.exit=parseFloat(exitP);
  if(memo)body.memo=memo;
  fetch(TRADE_API+'/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
    .then(function(r){return r.json();})
    .then(function(d){
      if(d.ok){
        journalTrades.unshift(d.trade);
        renderJournalStats();renderJournalList();
        // 입력 초기화
        document.getElementById('jf-ticker').value='';
        document.getElementById('jf-entry').value='';
        document.getElementById('jf-amount').value='';
        document.getElementById('jf-exit').value='';
        document.getElementById('jf-memo').value='';
        toggleJournalForm();
        if(err)err.classList.remove('show');
      }else{if(err){err.textContent=d.msg||'저장 실패';err.classList.add('show');}}
    })
    .catch(function(){if(err){err.textContent='서버 연결 오류';err.classList.add('show');}});
}

function setJournalFilter(f){
  journalFilter=f;
  ['all','open','win','lose'].forEach(function(v){
    var btn=document.getElementById('jf-'+v);
    if(btn)btn.classList.toggle('active',v===f);
  });
  renderJournalList();
}

function renderJournalList(){
  var list=document.getElementById('journal-trade-list');
  if(!list)return;
  var search=(document.getElementById('journal-search').value||'').toLowerCase();
  var items=journalTrades.filter(function(t){
    if(search&&!(t.ticker||'').toLowerCase().includes(search))return false;
    if(journalFilter==='open')return t.status==='open';
    if(journalFilter==='win')return t.status==='closed'&&t.pnl_pct>0;
    if(journalFilter==='lose')return t.status==='closed'&&t.pnl_pct<=0;
    return true;
  });
  if(items.length===0){list.innerHTML='<div class="journal-empty">해당하는 매매 기록이 없습니다.</div>';return;}
  var html='';
  items.forEach(function(t){
    var isLong=t.direction==='long';
    var badge=isLong?'<span class="jti-badge-long">LONG</span>':'<span class="jti-badge-short">SHORT</span>';
    var statusCls=t.status==='open'?'running':(t.pnl_pct>0?'win':'lose');
    var statusTxt=t.status==='open'?'진행중':(t.pnl_pct>0?'✅ 수익':'❌ 손실');
    var pnlPct=t.pnl_pct!==null?(t.pnl_pct>=0?'+':'')+t.pnl_pct.toFixed(2)+'%':'—';
    var pnlPctCls=t.pnl_pct!==null?(t.pnl_pct>0?'up':t.pnl_pct<0?'dn':''):'';
    var pnlAmt=t.pnl_amount!==null?(t.pnl_amount>=0?'+':'')+t.pnl_amount.toFixed(2)+' USDT':'—';
    var exitStr=t.exit||'—';
    html+='<div class="journal-trade-item" id="jti-'+t.id+'">';
    html+='<div class="jti-top"><div class="jti-left">'+badge+'<div class="jti-ticker">'+(t.ticker||'—')+'</div></div><span class="jti-status '+statusCls+'">'+statusTxt+'</span></div>';
    html+='<div class="jti-bottom">';
    html+='<div class="jti-field"><div class="jti-flabel">진입가</div><div class="jti-fval">'+t.entry+'</div></div>';
    html+='<div class="jti-field"><div class="jti-flabel">청산가</div><div class="jti-fval">'+exitStr+'</div></div>';
    html+='<div class="jti-field"><div class="jti-flabel">수익률</div><div class="jti-fval '+pnlPctCls+'">'+pnlPct+'</div></div>';
    html+='</div>';
    html+='<div class="jti-actions">';
    if(t.status==='open'){
      html+='<button class="jti-close-btn" onclick="journalCloseModal(\''+t.id+'\')">청산 입력</button>';
    }
    html+='<button class="jti-del-btn" onclick="journalDelete(\''+t.id+'\')">삭제</button>';
    html+='</div>';
    if(t.memo){html+='<div style="font-size:11px;color:var(--text3);margin-top:6px;">📝 '+t.memo+'</div>';}
    html+='<div style="font-size:10px;color:var(--text3);margin-top:4px;">'+t.date+'</div>';
    html+='</div>';
  });
  list.innerHTML=html;
}

function journalCloseModal(id){
  var exitP=prompt('청산가를 입력하세요:');
  if(!exitP)return;
  fetch(TRADE_API+'/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fanding_id:journalUser,password:journalPw,id:id,exit:parseFloat(exitP)})})
    .then(function(r){return r.json();})
    .then(function(d){if(d.ok){loadJournalTrades();}});
}

function journalDelete(id){
  if(!confirm('삭제하시겠습니까?'))return;
  fetch(TRADE_API+'/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fanding_id:journalUser,password:journalPw,id:id})})
    .then(function(r){return r.json();})
    .then(function(d){if(d.ok){journalTrades=journalTrades.filter(function(t){return t.id!==id;});renderJournalStats();renderJournalList();}});
}
"""

# initSoundBtn 함수 뒤에 추가
html = html.replace(
    'if("serviceWorker" in navigator)',
    NEW_JS + '\n\n// ══ init ══\ninitBtcBlur();\n\nif("serviceWorker" in navigator)'
)
print("[9] 매매일지/팝업 JS 추가 완료")

# ═══════════════════════════════════════════════════
# [10] 스켈레톤 로딩 CSS 추가
# ═══════════════════════════════════════════════════
SKELETON_CSS = """
  /* ══ 스켈레톤 로딩 ══ */
  .skel{display:inline-block;height:1.2em;background:linear-gradient(90deg,#1a1a1a 25%,#252525 50%,#1a1a1a 75%);background-size:200% 100%;border-radius:4px;animation:skeleton-shimmer 1.5s infinite;}
  @keyframes skeleton-shimmer{0%{background-position:200% 0;}100%{background-position:-200% 0;}}
  .skel-price{width:80%;height:28px;margin-bottom:4px;}
  .skel-change{width:55%;height:12px;}
  .skel-text{width:70%;height:12px;}
"""

html = html.replace('</style>', SKELETON_CSS + '\n</style>', 1)
print("[10] 스켈레톤 CSS 추가 완료")

# ═══════════════════════════════════════════════════
# [11] 스크롤 탑 버튼 CSS + HTML 추가
# ═══════════════════════════════════════════════════
SCROLLTOP_CSS = """
  /* ══ 스크롤 탑 버튼 ══ */
  #scroll-top-btn{position:fixed;bottom:24px;right:20px;width:42px;height:42px;border-radius:50%;background:rgba(14,14,14,0.9);border:0.5px solid rgba(255,255,255,0.15);color:var(--text2);display:flex;align-items:center;justify-content:center;cursor:pointer;opacity:0;pointer-events:none;transition:opacity 0.25s,transform 0.25s,border-color 0.2s;z-index:999;box-shadow:0 4px 16px rgba(0,0,0,0.5);backdrop-filter:blur(4px);}
  #scroll-top-btn.show{opacity:1;pointer-events:auto;}
  #scroll-top-btn:hover{border-color:var(--gold);color:var(--gold);transform:translateY(-2px);}
  @media(max-width:520px){#scroll-top-btn{bottom:20px;right:16px;width:38px;height:38px;}}
"""

html = html.replace('</style>', SCROLLTOP_CSS + '\n</style>', 1)

SCROLLTOP_HTML = """
<!-- ══ 스크롤 탑 버튼 ══ -->
<button id="scroll-top-btn" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="맨 위로">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
</button>
"""

html = html.replace('<footer class="site-footer">', SCROLLTOP_HTML + '\n<footer class="site-footer">', 1)

# 스크롤 탑 JS - 기존 초기화 코드에 추가
SCROLLTOP_JS = """
// ══ 스크롤 탑 버튼 ══
(function(){
  var btn=document.getElementById('scroll-top-btn');
  if(!btn)return;
  window.addEventListener('scroll',function(){
    btn.classList.toggle('show',window.scrollY>400);
  },{passive:true});
})();
"""

html = html.replace(
    'if("serviceWorker" in navigator)',
    SCROLLTOP_JS + '\nif("serviceWorker" in navigator)'
)
print("[11] 스크롤 탑 버튼 추가 완료")

# ═══════════════════════════════════════════════════
# [12] 세션 캐시 + Lazy Loading JS 추가
# ═══════════════════════════════════════════════════
CACHE_LAZY_JS = """
// ══ 세션 캐시 (15분) ══
var CACHE_TTL = 15 * 60 * 1000;
function cKey(s){return 'chartist_cache_'+s;}
function cGet(s){
  try{
    var r=sessionStorage.getItem(cKey(s));
    if(!r)return null;
    var p=JSON.parse(r);
    if(Date.now()-p.t>CACHE_TTL)return null;
    return p.v;
  }catch(e){return null;}
}
function cSet(s,v){
  try{sessionStorage.setItem(cKey(s),JSON.stringify({t:Date.now(),v:v}));}
  catch(e){}
}

// ══ Lazy Loading (Intersection Observer) ══
function observeLazy(id, fn){
  var el=document.getElementById(id);
  if(!el){fn();return;}
  if('IntersectionObserver' in window){
    var obs=new IntersectionObserver(function(entries){
      if(entries[0].isIntersecting){obs.disconnect();fn();}
    },{rootMargin:'150px'});
    obs.observe(el);
  }else{
    fn(); // 미지원 브라우저 폴백
  }
}

// ══ 캐시 적용된 fetch ══
function fetchWithCache(url, cacheKey){
  var cached=cGet(cacheKey);
  if(cached)return Promise.resolve(cached);
  return fetch(url)
    .then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.json();})
    .then(function(d){cSet(cacheKey,d);return d;});
}
"""

# 기존 autoRefresh 함수 앞에 삽입
html = html.replace(
    'function autoRefresh(){',
    CACHE_LAZY_JS + '\nfunction autoRefresh(){'
)

# loadAltcoinData에 캐시 적용
OLD_LOAD = "function loadAltcoinData(){showSkeletonAltcoin();"
NEW_LOAD = """function loadAltcoinData(){
  var cached=cGet('altcoin_data');
  if(cached){
    altcoinData={short:Array.isArray(cached.short)?cached.short:[],ma:Array.isArray(cached.ma)?cached.ma:[],mid:Array.isArray(cached.mid)?cached.mid:[],kiz:(cached.kiz&&typeof cached.kiz==='object')?cached.kiz:{},wyc:(cached.wyc&&typeof cached.wyc==='object')?cached.wyc:{}};
    renderAltcoin();
    return;
  }
  showSkeletonAltcoin();"""

html = html.replace(OLD_LOAD, NEW_LOAD, 1)

# altcoinData 저장 시 캐시 세팅 추가
OLD_CACHE_SET = "altcoinData={short:Array.isArray(d.short)?d.short:[],ma:Array.isArray(d.ma)?d.ma:[],mid:Array.isArray(d.mid)?d.mid:[],kiz:(d.kiz&&typeof d.kiz==='object')?d.kiz:{},wyc:(d.wyc&&typeof d.wyc==='object')?d.wyc:{}};"
NEW_CACHE_SET = OLD_CACHE_SET + "\n    cSet('altcoin_data',d);"

html = html.replace(OLD_CACHE_SET, NEW_CACHE_SET, 1)

# 스켈레톤 로딩 함수에 실제 스켈레톤 HTML 개선
OLD_SKEL = """function showSkeletonAltcoin(){var headerEl=document.getElementById('altcoin-list-header');if(headerEl)headerEl.style.display='none';var skItems='';for(var i=0;i<5;i++){skItems+='<div class="ticker-item" style="opacity:0.4;"><div class="ticker-left"><div style="width:80px;height:13px;background:var(--bg3);border-radius:4px;margin-bottom:4px;"></div><div style="width:120px;height:11px;background:var(--bg3);border-radius:4px;"></div></div><div class="ticker-right"><div style="width:60px;height:13px;background:var(--bg3);border-radius:4px;margin-bottom:4px;"></div><div style="width:50px;height:11px;background:var(--bg3);border-radius:4px;"></div></div></div>';}document.getElementById('altcoin-content').innerHTML='<div class="ticker-list">'+skItems+'</div>';}"""
NEW_SKEL = """function showSkeletonAltcoin(){var headerEl=document.getElementById('altcoin-list-header');if(headerEl)headerEl.style.display='none';var skItems='';for(var i=0;i<6;i++){skItems+='<div class="ticker-item"><div class="ticker-left"><div class="skel" style="width:'+(70+Math.random()*40|0)+'px;height:13px;margin-bottom:5px;"></div><div class="skel" style="width:'+(90+Math.random()*50|0)+'px;height:11px;"></div></div><div class="ticker-right"><div class="skel" style="width:64px;height:13px;margin-bottom:5px;"></div><div class="skel" style="width:48px;height:11px;"></div></div></div>';}document.getElementById('altcoin-content').innerHTML='<div class="ticker-list">'+skItems+'</div>';}"""

html = html.replace(OLD_SKEL, NEW_SKEL, 1)

print("[12] 세션 캐시 + Lazy Loading + 스켈레톤 개선 완료")

# ═══════════════════════════════════════════════════
# [13] 최종 검증
# ═══════════════════════════════════════════════════
checks = [
    ('매매일지 탭 버튼', 'tab-btn-journal'),
    ('BTC 블러 래퍼', 'btc-blur-wrap'),
    ('크립토 버블맵', 'cryptobubbles.net'),
    ('소리 팝업', 'sound-overlay'),
    ('BTC 슬라이드 팝업', 'btc-slide-popup'),
    ('매매일지 로그인', 'journal-login-wrap'),
    ('통계 대시보드', 'jstat-wr'),
    ('월별 차트', 'journal-month-chart'),
    ('RSI 필터 순서', 'af-rsi'),
    ('trade_api', 'TRADE_API'),
]

all_ok = True
for name, key in checks:
    ok = key in html
    print(f"  {'✅' if ok else '❌'} {name}: {'found' if ok else 'MISSING'}")
    if not ok:
        all_ok = False

print(f"\n최종 크기: {original_len:,} → {len(html):,} ({len(html)-original_len:+,})")

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(html)

if all_ok:
    print("\n✅ 모든 패치 완료! push_to_github.sh 실행하세요.")
else:
    print("\n⚠️ 일부 항목 누락 확인 필요")

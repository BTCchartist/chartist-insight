#!/usr/bin/env python3
"""patch_v3 - 미완료 항목 추가 패치"""
import os, shutil

HTML = '/home/ubuntu/chartist-insight/index.html'
with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

orig = len(content)
patches_done = []

# ══════════════════════════════════════════════
# [3] RSI sigMap 색상 구분
# ══════════════════════════════════════════════
old1 = "sigMap['rsi_bull']        = {label:'상승 다이버전스', cls:'sig-rsi'};\nsigMap['rsi_hidden_bull'] = {label:'상승 다이버전스', cls:'sig-rsi'};\nsigMap['rsi_bear']        = {label:'하락 다이버전스', cls:'sig-rsi'};\nsigMap['rsi_hidden_bear'] = {label:'하락 다이버전스', cls:'sig-rsi'};"
new1 = "sigMap['rsi_bull']        = {label:'상승 다이버전스', cls:'sig-rsi-bull'};\nsigMap['rsi_hidden_bull'] = {label:'숨은 상승 다이버전스', cls:'sig-rsi-bull'};\nsigMap['rsi_bear']        = {label:'하락 다이버전스', cls:'sig-rsi-bear-badge'};\nsigMap['rsi_hidden_bear'] = {label:'숨은 하락 다이버전스', cls:'sig-rsi-bear-badge'};"
if old1 in content:
    content = content.replace(old1, new1)
    patches_done.append('[3] RSI 색상 구분')

# ══════════════════════════════════════════════
# [4] 통계 카드 HTML 개선 (jstat-card + stat-badge)
# ══════════════════════════════════════════════
old4 = '''      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
        <div style="background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px;">
          <div style="font-size:11px;color:var(--text3);margin-bottom:4px;font-weight:500;">승률</div>
          <div class="jsc-val neu" id="jstat-wr">—</div>
          <div class="wr-gauge-wrap"><div class="wr-gauge-bar"><div class="wr-gauge-fill" id="jstat-wr-fill" style="width:0%"></div></div></div>
        </div>
        <div style="background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px;">
          <div style="font-size:11px;color:var(--text3);margin-bottom:4px;font-weight:500;">총 손익</div>
          <div class="jsc-val neu" id="jstat-pnl">—</div>
        </div>
        <div style="background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px;">
          <div style="font-size:11px;color:var(--text3);margin-bottom:4px;font-weight:500;">평균 수익률</div>
          <div class="jsc-val neu" id="jstat-avg">—</div>
        </div>
        <div style="background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px;">
          <div style="font-size:11px;color:var(--text3);margin-bottom:4px;font-weight:500;">연속 승/패</div>
          <div class="jsc-val neu" id="jstat-streak">—</div>
        </div>
      </div>'''
new4 = '''      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
        <div class="jstat-card">
          <div class="jstat-label">승률</div>
          <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:6px;">
            <div class="jsc-val neu" id="jstat-wr">—</div>
            <span class="stat-badge neu" id="jstat-wr-badge">—</span>
          </div>
          <div class="wr-gauge-wrap"><div class="wr-gauge-bar"><div class="wr-gauge-fill" id="jstat-wr-fill" style="width:0%"></div></div></div>
        </div>
        <div class="jstat-card">
          <div class="jstat-label">총 손익</div>
          <div style="display:flex;align-items:flex-end;justify-content:space-between;">
            <div class="jsc-val neu" id="jstat-pnl">—</div>
            <span class="stat-badge neu" id="jstat-pnl-badge">—</span>
          </div>
        </div>
        <div class="jstat-card">
          <div class="jstat-label">평균 수익률</div>
          <div class="jsc-val neu" id="jstat-avg">—</div>
        </div>
        <div class="jstat-card">
          <div class="jstat-label">연속 승/패</div>
          <div class="jsc-val neu" id="jstat-streak">—</div>
        </div>
      </div>'''
if old4 in content:
    content = content.replace(old4, new4)
    patches_done.append('[4] 통계 카드 UI 개선')

# ══════════════════════════════════════════════
# [5] 로그인 화면 - 닫기버튼 + 회원가입 버튼
# ══════════════════════════════════════════════
# 회원가입 버튼 텍스트 개선
old5 = '''<button class="journal-btn-sec" onclick="showJournalRegister()">처음 오셨나요? 가입하기</button>'''
new5 = '''<button class="journal-btn-sec" onclick="showJournalRegister()" style="background:transparent;border:0.5px solid var(--border2);border-radius:10px;padding:11px;color:var(--text3);font-size:13px;font-family:'Noto Sans KR',sans-serif;cursor:pointer;margin-top:4px;transition:all 0.15s;width:100%;">처음 오셨나요? <span style="color:var(--gold);font-weight:600;">회원가입 →</span></button>'''
if old5 in content:
    content = content.replace(old5, new5)
    patches_done.append('[5] 회원가입 버튼 스타일')

# ══════════════════════════════════════════════
# [6] 입력폼 - 필수 안내 + 배율 + 날짜 스타일
# ══════════════════════════════════════════════
old6 = '''    <div class="journal-form" id="journal-add-form">'''
new6 = '''    <div class="journal-form" id="journal-add-form">
      <div style="background:#0d0d0d;border-left:3px solid var(--gold);border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:14px;font-size:12px;color:var(--text2);line-height:1.75;">
        <strong style="color:var(--text);">📌 필수 입력:</strong> 날짜 · 종목 · 방향 · 진입가<br>
        <span style="font-size:11px;color:var(--text3);">청산가 입력 시 수익률% 자동계산 · 투자금액 입력 시 손익금액 자동계산</span>
      </div>'''
if old6 in content:
    content = content.replace(old6, new6, 1)
    patches_done.append('[6] 필수 안내 문구')

# 종목 입력란 → 자동완성 래퍼
old6b = '''          <input class="jf-input" id="jf-ticker" type="text" placeholder="예: BTC" autocomplete="off">'''
new6b = '''          <div style="position:relative;">
            <input class="jf-input" id="jf-ticker" type="text" placeholder="종목 검색 (예: BTC)" autocomplete="off" oninput="searchTicker(this.value)" onblur="setTimeout(hideTickerDrop,200)">
            <div id="ticker-drop" style="display:none;position:absolute;top:100%;left:0;right:0;z-index:100;background:var(--bg2);border:0.5px solid var(--border2);border-radius:0 0 8px 8px;max-height:200px;overflow-y:auto;"></div>
          </div>'''
if old6b in content:
    content = content.replace(old6b, new6b)
    patches_done.append('[6] 종목 자동완성 래퍼')

# 투자금액 type=number → text + 배율 추가
old6c = '''          <input class="jf-input" id="jf-amount" type="number" placeholder="선택">'''
new6c = '''          <input class="jf-input" id="jf-amount" type="text" placeholder="예: 1,000" oninput="fmtJournalAmount(this)" autocomplete="off">
          <div id="jf-amount-hint" style="font-size:11px;color:var(--gold);margin-top:3px;font-family:'JetBrains Mono',monospace;min-height:16px;"></div>'''
if old6c in content:
    content = content.replace(old6c, new6c)
    patches_done.append('[6] 투자금액 천단위 입력')

# 배율 입력란 추가 - jf-exit 필드 뒤에
old6d = '''          <input class="jf-input" id="jf-exit" type="number" placeholder="청산 후 입력" step="any">'''
new6d = '''          <input class="jf-input" id="jf-exit" type="number" placeholder="청산 후 입력" step="any">'''

# jf-memo 앞에 배율 추가
old6e = '''        <div class="jf-field">
          <div class="jf-label">메모</div>
          <input class="jf-input" id="jf-memo" type="text" placeholder="진입 이유 (선택)">
        </div>'''
new6e = '''        <div class="jf-field">
          <div class="jf-label">배율 <span style="color:var(--text3);font-size:10px;">선택</span></div>
          <input class="jf-input" id="jf-leverage" type="number" placeholder="예: 10" min="1" max="125" step="1">
        </div>
        <div class="jf-field">
          <div class="jf-label">메모</div>
          <input class="jf-input" id="jf-memo" type="text" placeholder="진입 이유 (선택)">
        </div>'''
if old6e in content:
    content = content.replace(old6e, new6e)
    patches_done.append('[6] 배율 입력란 추가')

# ══════════════════════════════════════════════
# [CSS] jstat-card, stat-badge 추가
# ══════════════════════════════════════════════
add_css = """
  /* jstat-card */
  .jstat-card{background:var(--bg2);border:0.5px solid var(--border);border-radius:12px;padding:14px;transition:border-color 0.2s;}
  .jstat-card:hover{border-color:var(--border2);}
  .jstat-label{font-size:11px;color:var(--text3);margin-bottom:4px;font-weight:500;}
  /* stat-badge */
  .stat-badge{display:inline-flex;align-items:center;font-size:10px;font-family:'JetBrains Mono',monospace;font-weight:700;padding:3px 8px;border-radius:4px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;}
  .stat-badge.green{background:rgba(76,175,125,0.15);color:var(--green);border:1px solid rgba(76,175,125,0.3);}
  .stat-badge.red{background:rgba(224,85,85,0.15);color:var(--red2);border:1px solid rgba(224,85,85,0.3);}
  .stat-badge.gold{background:rgba(201,168,76,0.12);color:var(--gold);border:1px solid rgba(201,168,76,0.3);}
  .stat-badge.neu{background:rgba(255,255,255,0.05);color:var(--text3);border:1px solid rgba(255,255,255,0.1);}
"""
if '.jstat-card{' not in content and '.jstat-card' not in content:
    content = content.replace('</style>', add_css + '\n</style>', 1)
    patches_done.append('[CSS] jstat-card/stat-badge 추가')

# ══════════════════════════════════════════════
# 저장
# ══════════════════════════════════════════════
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n'.join(patches_done) if patches_done else '변경 없음')
print(f"\n크기: {orig:,} → {len(content):,} (+{len(content)-orig:,})")
print("✅ patch_v3 완료!")

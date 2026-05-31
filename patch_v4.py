#!/usr/bin/env python3
"""patch_v4 - 통계카드 + 종목 자동완성"""
import os

HTML = '/home/ubuntu/chartist-insight/index.html'
with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

orig = len(content)
done = []

# ══ [4] 통계 카드 UI 개선
old4 = '''    <div class="journal-stat-grid" id="journal-stats">
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
    </div>'''

new4 = '''    <div class="journal-stat-grid" id="journal-stats">
      <div class="journal-stat-card">
        <div class="jsc-label">승률</div>
        <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:6px;">
          <div class="jsc-val neu" id="jstat-wr">—</div>
          <span class="stat-badge neu" id="jstat-wr-badge">—</span>
        </div>
        <div class="wr-gauge-wrap"><div class="wr-gauge-bar"><div class="wr-gauge-fill" id="jstat-wr-fill" style="width:0%"></div></div></div>
      </div>
      <div class="journal-stat-card">
        <div class="jsc-label">총 손익</div>
        <div style="display:flex;align-items:flex-end;justify-content:space-between;">
          <div class="jsc-val neu" id="jstat-pnl">—</div>
          <span class="stat-badge neu" id="jstat-pnl-badge">—</span>
        </div>
      </div>
      <div class="journal-stat-card">
        <div class="jsc-label">평균 수익률</div>
        <div class="jsc-val neu" id="jstat-avg">—</div>
      </div>
      <div class="journal-stat-card">
        <div class="jsc-label">연속 승/패</div>
        <div class="jsc-val neu" id="jstat-streak">—</div>
      </div>
    </div>'''

if old4 in content:
    content = content.replace(old4, new4)
    done.append('[4] 통계카드 배지 추가')

# ══ [6] 종목 자동완성 래퍼
old6 = '''          <input class="jf-input" id="jf-ticker" type="text" placeholder="예: BTC" autocomplete="off">'''
new6 = '''          <div style="position:relative;">
            <input class="jf-input" id="jf-ticker" type="text" placeholder="종목 검색 (예: BTC)" autocomplete="off" oninput="searchTicker(this.value)" onblur="setTimeout(hideTickerDrop,200)">
            <div id="ticker-drop" style="display:none;position:absolute;top:100%;left:0;right:0;z-index:100;background:var(--bg2);border:0.5px solid var(--border2);border-radius:0 0 8px 8px;max-height:200px;overflow-y:auto;box-shadow:0 8px 24px rgba(0,0,0,0.4);"></div>
          </div>'''
if old6 in content:
    content = content.replace(old6, new6)
    done.append('[6] 종목 자동완성 래퍼')

# ══ CSS - journal-stat-card hover 개선
old_css = '.journal-stat-card{'
new_css_add = '''.journal-stat-card:hover{border-color:var(--border2);}
.journal-stat-card{'''
if '.journal-stat-card:hover' not in content and old_css in content:
    content = content.replace(old_css, new_css_add, 1)
    done.append('[CSS] stat-card hover')

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n'.join(done) if done else '변경 없음')
print(f"\n크기: {orig:,} → {len(content):,} (+{len(content)-orig:,})")
print("✅ patch_v4 완료!")

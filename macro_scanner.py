#!/usr/bin/env python3
# macro_scanner.py
# 매크로 지표 수집 → /home/ubuntu/chartist-insight/data/macro.json 저장
# 30분마다 자동 갱신

import requests
import json
import time
from datetime import datetime
import pytz

KST = pytz.timezone("Asia/Seoul")
DATA_PATH = "/home/ubuntu/chartist-insight/data/macro.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fetch_yahoo(symbol, range_="2y"):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range={range_}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None
        d = r.json()
        result = d.get("chart", {}).get("result", [])
        if not result:
            return None
        closes = result[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])
        closes = [c for c in closes if c is not None]
        return closes
    except Exception as e:
        print(f"오류 ({symbol}): {e}")
        return None

def fetch_fg():
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        d = r.json()
        val = int(d["data"][0]["value"])
        cls = d["data"][0]["value_classification"]
        return val, cls
    except:
        return None, None

def collect():
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    data = {"updated": now_kst}

    # 공포탐욕
    fg_val, fg_cls = fetch_fg()
    data["fear_greed"] = {"value": fg_val, "label": fg_cls}

    # VIX
    vix = fetch_yahoo("%5EVIX", "1mo")
    if vix:
        v = vix[-1]
        data["vix"] = {
            "value": round(v, 2),
            "status": "경계" if v >= 30 else "주의" if v >= 20 else "안정"
        }

    # S&P500 낙폭
    sp = fetch_yahoo("%5EGSPC", "2y")
    if sp:
        cur = sp[-1]
        ath = max(sp)
        dd = round((cur - ath) / ath * 100, 1)
        data["sp500"] = {"value": round(cur, 0), "drawdown": dd}

    # 나스닥 낙폭
    nas = fetch_yahoo("%5EIXIC", "2y")
    if nas:
        cur = nas[-1]
        ath = max(nas)
        dd = round((cur - ath) / ath * 100, 1)
        data["nasdaq"] = {"value": round(cur, 0), "drawdown": dd}

    # 달러인덱스
    dxy = fetch_yahoo("DX-Y.NYB", "1mo")
    if dxy and len(dxy) >= 2:
        v = dxy[-1]
        pv = dxy[-2]
        chg = round((v - pv) / pv * 100, 2)
        data["dxy"] = {"value": round(v, 2), "change": chg}

    # 10년물 금리
    t10 = fetch_yahoo("%5ETNX", "1mo")
    if t10:
        v = t10[-1]
        data["t10y"] = {"value": round(v, 2)}

    # 원달러 환율
    krw = fetch_yahoo("KRW%3DX", "1mo")
    if krw and len(krw) >= 2:
        v = krw[-1]
        pv = krw[-2]
        chg = round(v - pv, 0)
        data["krw"] = {"value": round(v, 0), "change": int(chg)}

    # 장단기 금리차 (10Y - 2Y)
    t2 = fetch_yahoo("%5ETNX", "1mo")
    irx = fetch_yahoo("%5EIRX", "1mo")
    if t2 and irx:
        spread = round(t2[-1] - irx[-1], 2)
        data["spread"] = {
            "value": spread,
            "status": "역전" if spread < 0 else "정상"
        }

    # JSON 저장
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        print(f"[{now_kst}] 저장 완료: {json.dumps(data, ensure_ascii=False)[:100]}...")
    except Exception as e:
        print(f"저장 오류: {e}")

def main():
    print("📊 매크로 스캐너 시작 (30분마다 갱신)")
    while True:
        try:
            collect()
        except Exception as e:
            print(f"오류: {e}")
        time.sleep(1800)  # 30분

if __name__ == "__main__":
    main()

import requests
import time
import os
from dataclasses import dataclass
from typing import List

# ---------------------- REAL URL (from DevTools) ----------------------
URL = "https://bcast.sundhagold.com:7768/VOTSBroadcastStreaming/Services/xml/GetLiveRateByTemplateID/sundhagold"
# ----------------------------------------------------------------------


@dataclass
class Instrument:
    index: int
    code: str
    name: str
    buy: str
    sell: str
    high: str
    low: str

    @classmethod
    def from_line(cls, idx: int, line: str):
        parts = line.split("\t")
        if len(parts) < 7:
            raise ValueError(f"Not enough fields: {line!r}")
        _, code, name, buy, sell, high, low, *rest = parts
        return cls(idx, code, name, buy, sell, high, low)


def fetch_raw_text() -> str:
    r = requests.get(URL, timeout=4)
    r.raise_for_status()
    return r.text


def parse_instruments(text: str) -> List[Instrument]:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    instruments: List[Instrument] = []
    for i, line in enumerate(lines):
        try:
            instruments.append(Instrument.from_line(i, line))
        except:
            continue
    return instruments


def display_live():
    while True:
        try:
            raw = fetch_raw_text()
            inst = parse_instruments(raw)

            os.system("cls" if os.name == "nt" else "clear")

            if len(inst) < 5:
                print(f"Not enough data received. Parsed: {len(inst)}")
                time.sleep(0.5)
                continue

            # Layout based on LiveRates4.js
            top_tiles = inst[:3]
            futures = inst[3:5]
            products = inst[5:]

            print("==== LIVE RATES (SundhaGold.com) ====\n")

            # -------- TOP TILES (SILVER / GOLD / USDINR) --------
            print("=== TOP (Silver / Gold / USDINR) ===")
            for x in top_tiles:
                print(f"{x.name:12} | Buy/LTP: {x.buy:>8} | Sell: {x.sell:>8} | High: {x.high:>8} | Low: {x.low:>8}")
            print()

            # -------- FUTURES TABLE --------
            print("=== FUTURES ===")
            print(f"{'PRODUCT':18} | {'BID':>8} | {'ASK':>8} | {'HIGH':>8} | {'LOW':>8}")
            for x in futures:
                print(f"{x.name:18} | {x.buy:>8} | {x.sell:>8} | {x.high:>8} | {x.low:>8}")
            print()

            # -------- PRODUCTS TABLE (RANI, CHORSA, Gold 999, etc.) --------
            print("=== PRODUCTS ===")
            print(f"{'PRODUCT':18} | {'BUY':>8} | {'SELL':>8} | {'HIGH':>8} | {'LOW':>8}")
            for x in products:
                print(f"{x.name:18} | {x.buy:>8} | {x.sell:>8} | {x.high:>8} | {x.low:>8}")

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nExiting.")
            return
        except Exception as e:
            os.system("cls" if os.name == "nt" else "clear")
            print("Error:", e)
            time.sleep(1)


if __name__ == "__main__":
    display_live()

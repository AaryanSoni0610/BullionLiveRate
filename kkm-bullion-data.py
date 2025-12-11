import socketio
import json
import os

sio = socketio.Client()

@sio.event
def connect():
    print("Connected.")

    # exactly what the browser does
    sio.emit("room", "kkmspot")
    sio.emit("Client", "kkmspot")
    print("Sent room + Client joins for 'kkmspot'")

@sio.event
def disconnect():
    print("Disconnected.")

# ---- 1) PRODUCT TABLE: GOLD 999 / 995 / RANI / RUPA / CHORSA, etc. ----
@sio.on("message")
def on_message(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- Product Table Update (message event) ---\n")

    # The JS uses `let rates = data;` directly, so `data` should already be a list of objects.
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            print("Could not decode message as JSON:", e)
            print("Raw:", data)
            return

    if not isinstance(data, list):
        print("Unexpected message payload type:", type(data))
        print(data)
        return

    for prod in data:
        name    = prod.get("Symbol")           # "GOLD 999 IMP/ KKM", "RANI", "RUPA", ...
        bid     = prod.get("Bid")
        ask     = prod.get("Ask")
        is_disp = prod.get("IsDisplay")

        if not is_disp:
            continue

        print(f"{name:22} | Buy: {bid:>8} | Sell: {ask:>8}")

    print("\n--- end product table ---\n")

# ---- 2) OPTIONAL: raw MCX/COMEX feed (what you already had) ----
@sio.on("Liverate")
def on_liverate(raw_list):
    print("--- Liverate (MCX/COMEX) snapshot ---")
    for item in raw_list:
        try:
            entry = json.loads(item)
        except Exception:
            continue
        sym = entry.get("symbol") or entry.get("Name")
        bid = entry.get("Bid")
        ask = entry.get("Ask")
        t   = entry.get("Time")
        print(f"{sym:10} | Buy: {bid:>8} | Sell: {ask:>8} | {t}")
    print()

# ---- 3) See the reference data, if you want ----
@sio.on("ClientData")
def on_clientdata(data):
    print("\n--- ClientData (reference/config) ---")
    print(str(data)[:500], "...\n")  # just to see shape; you can json.loads if it's a string

sio.connect(
    "https://starlinebullion.co.in:10001",
    socketio_path="socket.io",
    transports=["websocket", "polling"]
)

sio.wait()

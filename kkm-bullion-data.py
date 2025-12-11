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

    
    print("      Name         |    Buy   |   Sell   |   High   |    Low   ")
    print("-------------------|----------|----------|----------|----------")
    for prod in data[:5]:
        name    = prod.get("Symbol")
        bid     = prod.get("Bid")
        ask     = prod.get("Ask")
        is_disp = prod.get("IsDisplay")
        high    = prod.get("High")
        low     = prod.get("Low")
        
        if name == "98 CHORSA":
            name = "SILVER 98"
        elif name == "GOLD 999 IMP/ KKM":
            name = "GOLD 999 IMP"
        elif name == "GOLD  995 IMP":
            name = "GOLD 9920 Ketbary"

        if not is_disp:
            continue

        print(f"{name:18} | {bid:>8} | {ask:>8} | {high:>8} | {low:>8}")

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

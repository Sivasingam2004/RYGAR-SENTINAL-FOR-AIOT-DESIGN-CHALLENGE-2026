from flask import Flask, request, jsonify
import threading
import time
import json

app = Flask(__name__)

# ============================================================
# RYGAR SENTINEL - UNO Q CENTRAL SERVER
# ============================================================

PORT = 5000
LCD_ROTATION_SECONDS = 3

# ------------------------------------------------------------
# CENTRAL SYSTEM STATE
# ------------------------------------------------------------

state = {
    "system": {
        "status": "ONLINE",
        "controller": "Arduino UNO Q"
    },

    "entrance": {
        "status": "OFFLINE",
        "last_event": "NONE",
        "last_update": None
    },

    "node2": {
        "status": "OFFLINE",
        "temperature": None,
        "humidity": None,
        "mq2": None,
        "acs": None,
        "water": None,
        "mq135": None,
        "pir1": None,
        "pir2": None,
        "parking1": None,
        "parking2": None,
        "flame": None,
        "fire": 0,
        "buzzer": 0,
        "fan": 0,
        "light": 0,
        "last_update": None
    }
}

state_lock = threading.Lock()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def parse_node2_data(data):
    """
    Converts:

    NODE2,MQ2=123,ACS=517,WATER=400,...

    into a Python dictionary.
    """

    result = {}

    if not data:
        return result

    parts = data.split(",")

    for part in parts:

        if "=" not in part:
            continue

        key, value = part.split("=", 1)

        key = key.strip().upper()
        value = value.strip()

        try:
            result[key] = int(value)
        except ValueError:
            try:
                result[key] = float(value)
            except ValueError:
                result[key] = value

    return result


def update_node2_state(payload):
    """
    Updates the central Node 2 state.
    """

    with state_lock:

        state["node2"]["status"] = "ONLINE"
        state["node2"]["last_update"] = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if payload.get("temperature") is not None:
            state["node2"]["temperature"] = payload["temperature"]

        if payload.get("humidity") is not None:
            state["node2"]["humidity"] = payload["humidity"]

        uno_data = payload.get("uno_data", "")

        parsed = parse_node2_data(uno_data)

        if "MQ2" in parsed:
            state["node2"]["mq2"] = parsed["MQ2"]

        if "ACS" in parsed:
            state["node2"]["acs"] = parsed["ACS"]

        if "WATER" in parsed:
            state["node2"]["water"] = parsed["WATER"]

        if "MQ135" in parsed:
            state["node2"]["mq135"] = parsed["MQ135"]

        if "PIR1" in parsed:
            state["node2"]["pir1"] = parsed["PIR1"]

        if "PIR2" in parsed:
            state["node2"]["pir2"] = parsed["PIR2"]

        if "PARK1" in parsed:
            state["node2"]["parking1"] = parsed["PARK1"]

        if "PARK2" in parsed:
            state["node2"]["parking2"] = parsed["PARK2"]

        if "FLAME" in parsed:
            state["node2"]["flame"] = parsed["FLAME"]

        if "FIRE" in parsed:
            state["node2"]["fire"] = parsed["FIRE"]

        if "BUZZER" in parsed:
            state["node2"]["buzzer"] = parsed["BUZZER"]

        if "FAN" in parsed:
            state["node2"]["fan"] = parsed["FAN"]

        if "LIGHT" in parsed:
            state["node2"]["light"] = parsed["LIGHT"]


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rygar Sentinel UNO Q</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #111;
                color: white;
                text-align: center;
                padding-top: 80px;
            }

            .box {
                display: inline-block;
                padding: 30px 50px;
                border-radius: 15px;
                background: #1e1e1e;
                box-shadow: 0 0 20px #000;
            }

            h1 {
                margin-bottom: 10px;
            }

            .online {
                color: #00ff88;
                font-size: 20px;
            }
        </style>
    </head>

    <body>

        <div class="box">

            <h1>RYGAR SENTINEL</h1>

            <h2>UNO Q Central Controller</h2>

            <p class="online">
                ● SYSTEM ONLINE
            </p>

            <p>
                Flask API : PORT 5000
            </p>

            <p>
                LCD Bridge : ENABLED
            </p>

            <p>
                LCD Rotation : 3 seconds
            </p>

            <p>
                Node 2 : /node2
            </p>

            <p>
                Entrance : /entrance
            </p>

            <p>
                State : /state
            </p>

        </div>

    </body>
    </html>
    """


# ============================================================
# ENTRANCE ESP32
# ============================================================

@app.route("/entrance", methods=["POST"])
def entrance():

    try:

        data = request.get_json(force=True)

    except Exception:

        return jsonify({
            "status": "ERROR",
            "message": "Invalid JSON"
        }), 400

    if not data:

        return jsonify({
            "status": "ERROR",
            "message": "Empty request"
        }), 400

    event = data.get("event", "UNKNOWN")

    with state_lock:

        state["entrance"]["status"] = "ONLINE"

        state["entrance"]["last_event"] = event

        state["entrance"]["last_update"] = (
            time.strftime("%Y-%m-%d %H:%M:%S")
        )

    print()
    print("================================")
    print("ENTRANCE EVENT")
    print("================================")
    print("Node :", data.get("node", "unknown"))
    print("Event:", event)
    print("================================")

    return jsonify({
        "status": "OK",
        "received": event
    })


# ============================================================
# NODE 2 / HELTEC
# ============================================================

@app.route("/node2", methods=["POST"])
def node2():

    try:

        data = request.get_json(force=True)

    except Exception:

        return jsonify({
            "status": "ERROR",
            "message": "Invalid JSON"
        }), 400

    if not data:

        return jsonify({
            "status": "ERROR",
            "message": "Empty request"
        }), 400

    print()
    print("================================")
    print("NODE 2 DATA")
    print("================================")
    print(json.dumps(data, indent=2))
    print("================================")

    update_node2_state(data)

    return jsonify({
        "status": "OK",
        "node": "edge_02"
    })


# ============================================================
# CENTRAL STATE
# ============================================================

@app.route("/state", methods=["GET"])
def get_state():

    with state_lock:

        current_state = json.loads(
            json.dumps(state)
        )

    return jsonify(current_state)


# ============================================================
# SYSTEM STATUS
# ============================================================

@app.route("/status", methods=["GET"])
def status():

    return jsonify({
        "system": "RYGAR SENTINEL",
        "controller": "Arduino UNO Q",
        "status": "ONLINE",
        "timestamp": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })


# ============================================================
# LCD DISPLAY DATA
# ============================================================

def get_lcd_pages():

    with state_lock:

        entrance_event = state["entrance"]["last_event"]

        temperature = state["node2"]["temperature"]
        humidity = state["node2"]["humidity"]

        fire = state["node2"]["fire"]

        pir1 = state["node2"]["pir1"]
        pir2 = state["node2"]["pir2"]

        light = state["node2"]["light"]

        parking1 = state["node2"]["parking1"]
        parking2 = state["node2"]["parking2"]

    pages = []

    # PAGE 1
    pages.append([
        "RYGAR SENTINEL",
        "SYSTEM ONLINE"
    ])

    # PAGE 2
    if temperature is not None and humidity is not None:

        pages.append([
            f"Temp: {temperature:.1f} C",
            f"Hum : {humidity:.1f}%"
        ])

    # PAGE 3
    pages.append([
        f"Entrance:",
        str(entrance_event)[:16]
    ])

    # PAGE 4
    pages.append([
        f"Meeting:{pir1}",
        f"Work:{pir2}"
    ])

    # PAGE 5
    pages.append([
        f"Parking1:{parking1}",
        f"Parking2:{parking2}"
    ])

    # PAGE 6
    pages.append([
        f"Light:{light}",
        f"Fire:{fire}"
    ])

    return pages


# ============================================================
# LCD BRIDGE THREAD
# ============================================================

def lcd_bridge():

    print("LCD Bridge : ENABLED")

    while True:

        try:

            pages = get_lcd_pages()

            for page in pages:

                line1 = page[0][:16]
                line2 = page[1][:16]

                # LCD output is intentionally kept here
                # for the UNO Q Arduino bridge.

                print(
                    "[LCD]",
                    line1,
                    "|",
                    line2
                )

                time.sleep(LCD_ROTATION_SECONDS)

        except Exception as e:

            print("LCD ERROR:", e)

            time.sleep(2)


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("============================================")
    print(" RYGAR SENTINEL - UNO Q CENTRAL SERVER")
    print("============================================")
    print("Flask API : PORT", PORT)
    print("LCD Bridge : ENABLED")
    print("LCD Rotation :", LCD_ROTATION_SECONDS, "seconds")
    print("Node 2 : /node2")
    print("Entrance : /entrance")
    print("State : /state")
    print("============================================")
    print()

    lcd_thread = threading.Thread(
        target=lcd_bridge,
        daemon=True
    )

    lcd_thread.start()

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        threaded=True
    )
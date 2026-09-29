import json
import threading
import time

import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template_string

# ============================================================
# RYGAR SENTINEL - RASPBERRY PI DASHBOARD
# ============================================================

app = Flask(__name__)

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "rygar/state"

# CCTV laptop
CCTV_URL = "http://10.148.119.57:5001/video"

state = {
    "system": {
        "status": "WAITING"
    },
    "entrance": {
        "status": "OFFLINE",
        "last_event": "NONE"
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
        "light": 0
    }
}

state_lock = threading.Lock()


# ============================================================
# MQTT
# ============================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("MQTT CONNECTED")

        client.subscribe(MQTT_TOPIC)

        print("Subscribed:", MQTT_TOPIC)

    else:

        print("MQTT CONNECTION FAILED:", rc)


def on_message(client, userdata, msg):

    global state

    try:

        data = json.loads(
            msg.payload.decode()
        )

        with state_lock:
            state = data

        print("STATE RECEIVED")

    except Exception as e:

        print("MQTT DATA ERROR:", e)


def mqtt_worker():

    client = mqtt.Client(
        client_id="rygar_dashboard"
    )

    client.on_connect = on_connect
    client.on_message = on_message

    while True:

        try:

            print("Connecting to MQTT...")

            client.connect(
                MQTT_BROKER,
                MQTT_PORT,
                60
            )

            client.loop_forever()

        except Exception as e:

            print("MQTT ERROR:", e)

            time.sleep(3)


# ============================================================
# API
# ============================================================

@app.route("/api/state")
def api_state():

    with state_lock:

        return jsonify(state)


# ============================================================
# DASHBOARD
# ============================================================

HTML = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Rygar Sentinel</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #0b0f14;

    color: #ffffff;

}

header {

    padding: 20px 30px;

    background: #111820;

    border-bottom: 1px solid #26313d;

}

header h1 {

    margin: 0;

    font-size: 28px;

}

header p {

    margin: 5px 0 0;

    color: #9aa7b5;

}

.container {

    padding: 20px;

    max-width: 1500px;

    margin: auto;

}

.grid {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));

    gap: 15px;

}

.card {

    background: #151c24;

    border: 1px solid #26313d;

    border-radius: 12px;

    padding: 18px;

}

.card h2 {

    margin-top: 0;

    font-size: 17px;

    color: #b9c5d1;

}

.value {

    font-size: 28px;

    font-weight: bold;

    margin-top: 10px;

}

.small {

    color: #8795a3;

    font-size: 13px;

}

.status {

    font-size: 16px;

    font-weight: bold;

}

.online {

    color: #43e38b;

}

.offline {

    color: #ff6b6b;

}

.warning {

    color: #ffcc66;

}

.danger {

    color: #ff5c5c;

}

.ok {

    color: #43e38b;

}

.section {

    margin-top: 25px;

}

.section-title {

    font-size: 20px;

    margin-bottom: 12px;

}

.cctv {

    width: 100%;

    max-width: 1000px;

    display: block;

    margin: auto;

    border-radius: 10px;

    border: 1px solid #26313d;

    background: #000;

}

.footer {

    text-align: center;

    color: #66727e;

    padding: 30px;

}

</style>

</head>


<body>

<header>

<h1>RYGAR SENTINEL</h1>

<p>Unified Edge Appliance — Sentinel Core</p>

</header>


<div class="container">


<!-- SYSTEM -->

<div class="section">

<div class="section-title">
System Status
</div>

<div class="grid">

<div class="card">

<h2>System</h2>

<div id="systemStatus"
     class="value">
WAITING
</div>

<div class="small">
Raspberry Pi Sentinel Core
</div>

</div>


<div class="card">

<h2>Entrance Node</h2>

<div id="entranceStatus"
     class="status">
OFFLINE
</div>

<div id="entranceEvent"
     class="small">
No event
</div>

</div>


<div class="card">

<h2>Edge Sensor Node</h2>

<div id="nodeStatus"
     class="status">
OFFLINE
</div>

</div>

</div>

</div>


<!-- ENVIRONMENT -->

<div class="section">

<div class="section-title">
Environment
</div>

<div class="grid">


<div class="card">

<h2>Temperature</h2>

<div id="temperature"
     class="value">
--
</div>

<div class="small">
°C
</div>

</div>


<div class="card">

<h2>Humidity</h2>

<div id="humidity"
     class="value">
--
</div>

<div class="small">
%
</div>

</div>


<div class="card">

<h2>MQ-2 Gas</h2>

<div id="mq2"
     class="value">
--
</div>

</div>


<div class="card">

<h2>MQ-135 Air</h2>

<div id="mq135"
     class="value">
--
</div>

</div>


<div class="card">

<h2>Water</h2>

<div id="water"
     class="value">
--
</div>

</div>


<div class="card">

<h2>ACS712</h2>

<div id="acs"
     class="value">
--
</div>

<div class="small">
Raw ADC
</div>

</div>

</div>

</div>


<!-- SECURITY -->

<div class="section">

<div class="section-title">
Security & Safety
</div>

<div class="grid">


<div class="card">

<h2>Fire</h2>

<div id="fire"
     class="value">
NORMAL
</div>

</div>


<div class="card">

<h2>Buzzer</h2>

<div id="buzzer"
     class="value">
OFF
</div>

</div>


<div class="card">

<h2>Last Access Event</h2>

<div id="access"
     class="value"
     style="font-size:20px">
NONE
</div>

</div>


<div class="card">

<h2>Door</h2>

<div id="door"
     class="value"
     style="font-size:20px">
UNKNOWN
</div>

</div>

</div>

</div>


<!-- OCCUPANCY -->

<div class="section">

<div class="section-title">
Occupancy & Infrastructure
</div>

<div class="grid">


<div class="card">

<h2>Meeting Hall</h2>

<div id="pir1"
     class="value">
--
</div>

</div>


<div class="card">

<h2>Workspace</h2>

<div id="pir2"
     class="value">
--
</div>

</div>


<div class="card">

<h2>Parking 1</h2>

<div id="parking1"
     class="value">
--
</div>

</div>


<div class="card">

<h2>Parking 2</h2>

<div id="parking2"
     class="value">
--
</div>

</div>


<div class="card">

<h2>Room Light</h2>

<div id="light"
     class="value">
OFF
</div>

</div>


<div class="card">

<h2>Fan</h2>

<div id="fan"
     class="value">
OFF
</div>

</div>

</div>

</div>


<!-- CCTV -->

<div class="section">

<div class="section-title">
Live CCTV
</div>

<div class="card">

<img
    class="cctv"
    src="{{ cctv_url }}"
    alt="Rygar Sentinel CCTV">

</div>

</div>


</div>


<div class="footer">

Rygar Sentinel • Local Edge Monitoring

</div>


<script>

function text(id, value) {

    const element =
        document.getElementById(id);

    if (element) {
        element.innerText = value;
    }

}


function onOff(value) {

    return value == 1
        ? "ON"
        : "OFF";

}


function occupancy(value) {

    return value == 1
        ? "OCCUPIED"
        : "CLEAR";

}


async function updateDashboard() {

    try {

        const response =
            await fetch("/api/state");

        const data =
            await response.json();


        // SYSTEM

        text(
            "systemStatus",
            data.system?.status || "ONLINE"
        );


        // ENTRANCE

        text(
            "entranceStatus",
            data.entrance?.status || "OFFLINE"
        );

        text(
            "entranceEvent",
            data.entrance?.last_event || "NONE"
        );


        // NODE

        text(
            "nodeStatus",
            data.node2?.status || "OFFLINE"
        );


        // ENVIRONMENT

        text(
            "temperature",
            data.node2?.temperature ?? "--"
        );

        text(
            "humidity",
            data.node2?.humidity ?? "--"
        );

        text(
            "mq2",
            data.node2?.mq2 ?? "--"
        );

        text(
            "mq135",
            data.node2?.mq135 ?? "--"
        );

        text(
            "water",
            data.node2?.water ?? "--"
        );

        text(
            "acs",
            data.node2?.acs ?? "--"
        );


        // FIRE

        const fire =
            data.node2?.fire || 0;

        text(
            "fire",
            fire
                ? "DETECTED"
                : "NORMAL"
        );


        text(
            "buzzer",
            onOff(
                data.node2?.buzzer
            )
        );


        // ACCESS

        text(
            "access",
            data.entrance?.last_event || "NONE"
        );


        // DOOR

        const event =
            data.entrance?.last_event || "";

        if (event === "DOOR_OPEN") {

            text(
                "door",
                "OPEN"
            );

        } else if (event === "DOOR_CLOSED") {

            text(
                "door",
                "CLOSED"
            );

        } else {

            text(
                "door",
                "UNKNOWN"
            );

        }


        // OCCUPANCY

        text(
            "pir1",
            occupancy(
                data.node2?.pir1
            )
        );

        text(
            "pir2",
            occupancy(
                data.node2?.pir2
            )
        );


        text(
            "parking1",
            occupancy(
                data.node2?.parking1
            )
        );

        text(
            "parking2",
            occupancy(
                data.node2?.parking2
            )
        );


        // DEVICES

        text(
            "light",
            onOff(
                data.node2?.light
            )
        );

        text(
            "fan",
            onOff(
                data.node2?.fan
            )
        );


    } catch (error) {

        console.log(
            "Dashboard update error:",
            error
        );

    }

}


updateDashboard();

setInterval(
    updateDashboard,
    2000
);

</script>


</body>

</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def dashboard():

    return render_template_string(
        HTML,
        cctv_url=CCTV_URL
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    print("============================================")
    print(" RYGAR SENTINEL - DASHBOARD")
    print("============================================")
    print("MQTT Broker :", MQTT_BROKER)
    print("MQTT Topic  :", MQTT_TOPIC)
    print("CCTV        :", CCTV_URL)
    print("Dashboard   : PORT 8080")
    print("============================================")

    threading.Thread(
        target=mqtt_worker,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False,
        threaded=True
    )
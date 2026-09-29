import cv2
import threading
import time

from flask import Flask, Response

# ============================================================
# RYGAR SENTINEL - CCTV SERVER
# ============================================================

app = Flask(__name__)

CAMERA_INDEX = 0
PORT = 5001

camera = cv2.VideoCapture(
    CAMERA_INDEX,
    cv2.CAP_DSHOW
)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)

camera.set(
    cv2.CAP_PROP_FPS,
    20
)

frame = None
frame_lock = threading.Lock()


# ============================================================
# CAMERA CAPTURE
# ============================================================

def camera_loop():

    global frame

    print("Camera capture thread started")

    while True:

        success, captured = camera.read()

        if success:

            with frame_lock:

                frame = captured

        else:

            print("Camera frame failed")

            time.sleep(0.2)


# ============================================================
# MJPEG STREAM
# ============================================================

def generate_frames():

    while True:

        with frame_lock:

            if frame is None:

                current_frame = None

            else:

                current_frame = frame.copy()


        if current_frame is None:

            time.sleep(0.05)

            continue


        success, buffer = cv2.imencode(
            ".jpg",
            current_frame,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                80
            ]
        )


        if not success:

            continue


        jpg = buffer.tobytes()


        yield (

            b"--frame\r\n"

            b"Content-Type: image/jpeg\r\n"

            b"Content-Length: "

            + str(len(jpg)).encode()

            + b"\r\n\r\n"

            + jpg

            + b"\r\n"
        )


        time.sleep(0.03)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Rygar Sentinel CCTV</title>

        <style>

            body {

                margin: 0;

                background: #0b0f14;

                color: white;

                font-family: Arial;

                text-align: center;

            }

            h1 {

                margin-top: 30px;

            }

            img {

                width: 90%;

                max-width: 1280px;

                border-radius: 10px;

                border: 1px solid #333;

            }

        </style>

    </head>

    <body>

        <h1>RYGAR SENTINEL CCTV</h1>

        <p>Live Edge Camera Feed</p>

        <img src="/video">

    </body>

    </html>
    """


# ============================================================
# VIDEO
# ============================================================

@app.route("/video")
def video():

    return Response(

        generate_frames(),

        mimetype=
        "multipart/x-mixed-replace; boundary=frame"

    )


# ============================================================
# STATUS
# ============================================================

@app.route("/status")
def status():

    with frame_lock:

        camera_ready = frame is not None


    return {

        "camera": camera_ready,

        "status":
            "online"
            if camera_ready
            else "waiting"

    }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("============================================")
    print(" RYGAR SENTINEL - CCTV")
    print("============================================")
    print("Camera :", CAMERA_INDEX)
    print("Port   :", PORT)
    print("============================================")


    if not camera.isOpened():

        print(
            "ERROR: CAMERA COULD NOT BE OPENED"
        )

        raise SystemExit


    threading.Thread(
        target=camera_loop,
        daemon=True
    ).start()


    app.run(
        host="0.0.0.0",
        port=PORT,
        threaded=True,
        debug=False
    )
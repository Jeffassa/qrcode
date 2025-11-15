from flask import Flask, send_file, render_template_string
import qrcode
import io
import time
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Emargement ESATIC</title>
    <style>
        body { text-align:center; font-family:Arial; padding-top:40px; }
        #qr { width:250px; height:250px; margin:auto; }
        button { padding:10px 20px; font-size:16px; margin-top:10px; }
    </style>
</head>
<body>
    <h2>QR Code Emargement ESATIC</h2>
    <div id="qr-container">
        <img id="qr" src="/qr">
    </div>
    <p id="countdown">Prochain QR dans : 30s</p>
    <a id="download" href="/download" download="emargement_esatic.png">
        <button>Télécharger le QR Code</button>
    </a>

    <script>
        let countdownElem = document.getElementById("countdown");
        let timeLeft = 30;

        function updateCountdown() {
            countdownElem.textContent = "Prochain QR dans : " + timeLeft + "s";
            if(timeLeft <= 0){
                timeLeft = 30;
                document.getElementById("qr").src = "/qr?" + new Date().getTime(); // recharge QR
                document.getElementById("download").href = "/download?" + new Date().getTime(); // met à jour le download
            } else {
                timeLeft--;
            }
        }

        setInterval(updateCountdown, 1000);
    </script>
</body>
</html>
"""

def generate_qr_bytes():
    """Génère l'image du QR en bytes."""
    payload = {
        "action": "EMARGEMENT_ESATIC",
        "timestamp": int(time.time())  # rend chaque QR unique
    }
    data = json.dumps(payload)
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/qr")
def qr_image():
    return send_file(generate_qr_bytes(), mimetype="image/png")

@app.route("/download")
def download_qr():
    return send_file(
        generate_qr_bytes(),
        mimetype="image/png",
        as_attachment=True,
        download_name="emargement_esatic.png"
    )

if __name__ == "__main__":
    app.run(debug=True)

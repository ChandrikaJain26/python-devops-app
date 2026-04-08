from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify({"result": a + b}), 200

def main():
    # Bind on 0.0.0.0 so it works inside Docker also
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()

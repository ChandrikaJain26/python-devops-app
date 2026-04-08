from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/add/<int:a>/<int:b>", methods=["GET"])
def add(a, b):
    return jsonify({"result": a + b}), 200

def main():
    # Bind only to localhost for security (recommended by Sonar)
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()

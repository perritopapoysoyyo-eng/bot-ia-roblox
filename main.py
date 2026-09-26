from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/comando', methods=['POST'])
def procesar_comando():
    datos = request.get_json()
    if not datos or 'mensaje' not in datos:
        return jsonify({"error": "No se envió mensaje"}), 400

    mensaje = datos['mensaje'].lower()
    
    # Lógica de decisión de la IA / Bot
    if "ir a" in mensaje:
        usuario = mensaje.replace("ir a", "").strip()
        respuesta = {
            "accion": "mover",
            "objetivo": usuario
        }
    elif "teletransportar a" in mensaje or "tp a" in mensaje:
        usuario = mensaje.replace("teletransportar a", "").replace("tp a", "").strip()
        respuesta = {
            "accion": "teleport",
            "objetivo": usuario
        }
    else:
        respuesta = {
            "accion": "ninguna",
            "objetivo": None
        }

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

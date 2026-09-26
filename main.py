import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# La API Key se lee desde las variables de entorno de Render
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/comando', methods=['POST'])
def procesar_comando():
    datos = request.get_json()
    if not datos or 'mensaje' not in datos:
        return jsonify({"error": "No se envió mensaje"}), 400

    mensaje_usuario = datos['mensaje']

    system_prompt = """
    Eres el cerebro de un bot en Roblox. Tu trabajo es interpretar las órdenes del usuario y traducirlas a formato JSON estricto.
    
    Devuelve ÚNICAMENTE un objeto JSON con esta estructura (sin texto adicional ni formato Markdown):
    {
        "accion": "mover" | "teleport" | "ninguna",
        "objetivo": "nombre_del_jugador" | null
    }

    Reglas:
    - Si el usuario quiere ir caminando o seguir a alguien, usa "mover".
    - Si el usuario quiere aparecer instantáneamente o teletransportarse, usa "teleport".
    - Extrae solo el nombre del jugador objetivo.
    - Si el mensaje no es una orden válida de movimiento, usa "ninguna" y null.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje_usuario}
            ],
            temperature=0
        )

        respuesta_ia = response.choices[0].message.content.strip()
        
        # Limpiar posible formato Markdown
        if respuesta_ia.startswith("```"):
            respuesta_ia = respuesta_ia.replace("```json", "").replace("```", "").strip()

        json_respuesta = json.loads(respuesta_ia)
        return jsonify(json_respuesta)

    except Exception as e:
        return jsonify({"accion": "ninguna", "objetivo": None, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

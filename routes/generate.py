from flask import Blueprint, request, jsonify
from services.replicate import generate_image
from prompts.prompt_templates import prompt_templates
import re


generate_bp= Blueprint("generate", __name__)

@generate_bp.route("/generate", methods=["POST"])
def generate():
    try:
        # Obtenemos los datos JSON que el frontend nos envía
        data = request.get_json()

        # Extraemos la imagen, el estilo y el tipo de habitación del JSON
        image_url = data.get("image")  # URL de la imagen original
        style = data.get("style")      # Estilo seleccionado (ej: "Modern")
        room = data.get("room")        # Tipo de cuarto (ej: "Living Room")

        # Validamos que no falte ningún dato
        if not image_url or not style or not room:
            return jsonify({"error": "Faltan datos: imagen, estilo o tipo de cuarto"}), 400


        #Verificamos que la URL de la imagen sea valida de Cloudinary
        if not re.match(r'^https?://', image_url):
            return jsonify({"error": "La URL de la imagen no es válida"}), 400

        # Buscamos el template de texto para el estilo elegido
        template = prompt_templates.get(style)

        # Si el estilo no existe en nuestros templates, devolvemos error
        if not template:
            return jsonify({"error": f"El estilo '{style}' no está soportado"}), 400

        # Reemplazamos {room} en el prompt con el cuarto seleccionado
        # Por ejemplo: "Modern-style (living room) with furniture..." etc.
        prompt = template.format(room=room.lower())

        # Llamamos a nuestra función que envía todo a Replicate y genera la imagen
        result = generate_image(image_url, prompt)

        # Devolvemos la URL de la imagen generada al frontend
        return jsonify({ "result": result }), 200

    except Exception as e:
        # Si hay algún error inesperado, lo capturamos y lo mostramos
        print(f"Error en generate: {str(e)}")
        return jsonify({"error": str(e)}), 500
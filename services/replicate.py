from click import prompt
import replicate
import os

# Se eliminó la carga de .env ya que Railway usa variables de entorno del sistema

api_token = os.getenv("REPLICATE_API_TOKEN")
if not api_token:
    raise ValueError("REPLICATE_API_TOKEN not found in environment variables")

replicate_client = replicate.Client(api_token=api_token)

def generate_image(image_url: str, prompt: str):
    try:
        output = replicate_client.run(
            "adirik/interior-design:76604baddc85b1b4616e1c6475eca080da339c8875bd4996705440484a6eac38",
            input={
                "image": image_url,
                "prompt": prompt,
                "negative_prompt":  "lowres, watermark, banner, logo, watermark, contactinfo, text, deformed, blurry, blur, out of focus, out of frame, surreal, extra, ugly, upholstered walls, fabric walls, plush walls, mirror, mirrored, functional, realistic",
                "guidance_scale": 8.24,
                "num_inference_steps": 80,
                "prompt_strength": 0.6
            },
            timeout=300  # Aumentar a 5 minutos
        )
        
        return str(output)
    except Exception as e:
        print(f"Error in generate_image: {str(e)}")
        raise e

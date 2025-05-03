from click import prompt
import replicate
import os
from dotenv import load_dotenv

load_dotenv() #Cargar .env

api_token = os.getenv("REPLICATE_API_TOKEN")
if not api_token:
    raise ValueError("REPLICATE_API_TOKEN not found in .env")

replicate_client = replicate.Client(api_token=api_token)

def generate_image(image_url: str, prompt: str):
    try:
        output = replicate_client.run(
            "adirik/interior-design:76604baddc85b1b4616e1c6475eca080da339c8875bd4996705440484a6eac38",
            input={
                "image": image_url,
                "prompt": prompt,
                "negative_prompt": "lowres, watermark, banner, logo, contactinfo, text, blurry, surreal, ugly, mirror",
                "num_inference_steps": 50,
                "guidance_scale": 15,
                "prompt_strength": 0.8
            },
            timeout=300  # Aumentar a 5 minutos
        )
        
        return str(output)
    except Exception as e:
        print(f"Error in generate_image: {str(e)}")
        raise e


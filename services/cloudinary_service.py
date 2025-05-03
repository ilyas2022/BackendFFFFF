import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

#Carga las variables de entorno
load_dotenv()

#Configurar Cloudinary
cloudinary.config(
    cloud_name= os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def upload_image(file):
    try:
        #Subir la imagen a Cloudinary
        upload_result= cloudinary.uploader.upload(file)

        #Devolver la URL de la imagen
        return upload_result['secure_url']
    except Exception as e:
        print(f"Error al subir la imagen: {str(e)}")
        raise e
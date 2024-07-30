import requests
import os
import concurrent.futures
from tqdm import tqdm

# URL de la API
api_url = "https://fortnite-api.com/v2/cosmetics/br"

# Directorio donde se guardarán las imágenes
output_dir = "imagenes_png"
os.makedirs(output_dir, exist_ok=True)

def download_image(url_item):
    url, item_id = url_item
    image_name = f"{item_id}.png"
    image_path = os.path.join(output_dir, image_name)
    
    try:
        img_response = requests.get(url, timeout=10)
        if img_response.status_code == 200:
            with open(image_path, 'wb') as img_file:
                img_file.write(img_response.content)
            return f"Descargada: {image_name}"
        else:
            return f"Error al descargar: {image_name} (Status code: {img_response.status_code})"
    except Exception as e:
        return f"Error al descargar: {image_name} ({e})"

# Solicitar datos de la API
response = requests.get(api_url)
data = response.json()

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    items = data.get('data', [])
    png_urls = []

    # Filtrar URLs que terminan en .png
    for item in items:
        item_id = item.get('id')
        images = item.get('images', {})
        for image_type, url in images.items():
            if isinstance(url, str) and url.endswith('.png'):
                png_urls.append((url, item_id))

    # Descargar imágenes en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(tqdm(executor.map(download_image, png_urls), total=len(png_urls)))

    # Imprimir resultados
    for result in results:
        print(result)

    print("Descarga completada.")
else:
    print(f"Error en la solicitud a la API: {response.status_code}")

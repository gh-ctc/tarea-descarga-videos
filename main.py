import os
import requests
import time
from typing import Optional, Dict

def make_request(url: str, max_retries: int = 3, delay: int = 5) -> Optional[Dict]:
    """
    Realiza una solicitud HTTP GET con reintentos
    
    Args:
        url: URL para realizar la solicitud
        max_retries: Número máximo de intentos
        delay: Tiempo de espera entre intentos en segundos
    
    Returns:
        Dict con la respuesta JSON si es exitosa, None si fallan todos los intentos
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            return response.json()
        except requests.RequestException as e:
            print(f"Intento {attempt + 1}/{max_retries} falló: {str(e)}")
            if attempt < max_retries - 1:  # Si no es el último intento
                print(f"Esperando {delay} segundos antes del siguiente intento...")
                time.sleep(delay)
            else:
                print("Se agotaron todos los intentos")
                return None

def main():
    # Obtener la URL desde las variables de entorno
    url = os.getenv('MOODLE_URL')
    if not url:
        raise ValueError("La variable de entorno MOODLE_URL no está configurada")
    
    result = make_request(url)
    if result:
        print("Solicitud exitosa:")
        print(result)
    else:
        print("La solicitud falló después de todos los reintentos")
        # Opcional: hacer que la action falle si no se pudo completar la solicitud
        exit(1)

if __name__ == "__main__":
    main()

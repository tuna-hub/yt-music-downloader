import os
import re 
import requests
import yt_dlp
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, APIC, error

CARPETA_SALIDA="musica"

if not os.path.exists(CARPETA_SALIDA):
	os.makedirs(CARPETA_SALIDA)
def get_info(url):
	opciones = {"quiet": True, "extract_flat":True}

	with yt_dlp.YoutubeDL(opciones) as ydl:
		info = ydl.extract_info(url, download=False)

	if info.get("_type") == "playlist":
		entradas = info.get("entries", [])
		print(f"\nPlaylist detectada: {info.get('title', 'Sin titulo')}")
		print(f"Total de canciones: {len(entradas)}")
	
		return "playlist", entradas, None
	
	else:
		titulo = info.get("title", "Sin titulo")
		artista = info.get("artist") or info.get("uploader", "Desconocido")
		miniatura = info.get("thumbnail", "")

		return "video", titulo, artista, miniatura


def descargar(url, titulo, artista, miniatura):
	nombre_archivo = titulo.replace("/", "-")
	ruta_mp3 = os.path.join(CARPETA_SALIDA, f"{nombre_archivo}.mp3")

	opciones = {
		"format": "bestaudio/best",
		"outtmpl": os.path.join(CARPETA_SALIDA, f"{nombre_archivo}.%(ext)s"),
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "0",
		}],
		"quiet": True,
	}
	
	with yt_dlp.YoutubeDL(opciones) as ydl:
		ydl.download([url])

	agregar_metadatos(ruta_mp3, titulo, artista, miniatura)


def agregar_metadatos(ruta_mp3, titulo, artista, miniatura):
	audio= ID3(ruta_mp3)

	audio[TIT2] = TIT2(encoding=3, text=titulo)
	audio[TPE1] = TPE1(encoding=3, text=artista)

	if miniatura:
		respuesta = requests.get(miniatura)
		audio[APIC] = APIC(
			encoding=3,
			mime="image/jpeg",
			type=3,
			desc="Cover",
			data=respuesta.content
		)
	audio.save()


def main():
	print("\nDescargador mp3 youtube\n")
	url = input("Url:  ").strip()

	print("\n\nObteniendo informacion...\n")
	resultado = get_info(url)

	if resultado[0] == "playlist":
		_, entradas, _ = resultado
		confirmar = input("\nDescargar playlist? (s/n): ").strip().lower()
		if confirmar == "s":
			for i, entrada, in enumerate(entradas, 1):
				url_cancion = f"https://www.youtube.com/watch?v={entrada['id']}"
				print(f"\n[{i}/{len(entradas)}] {entrada.get('title', 'Sin titulo')}")
				info = get_info(url_cancion)
				_, titulo, artista, miniatura = info
				descargar(url_cancion, titulo, artista, miniatura)
				print(f"\nPlaylist guardada en '{CARPETA_SALIDA}'")
		else:
			print("\nCancelado.")
	else:
		_, titulo, artista, miniatura = resultado
		print(f"\nTitulo: {titulo}")
		print(f"Artista: {artista}")
		confirmar = input("Descargar? (s/n): ").strip().lower()
		if confirmar == "s":
			print("\nDescargando...")
			descargar(url, titulo, artista, miniatura)
			print(f"Guardado en '{CARPETA_SALIDA}'")
		else:
			print("\nCancelado.")


if __name__ == "__main__":
	main()
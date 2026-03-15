import csv
import re
from bs4 import BeautifulSoup
import os
import random
import time
from playwright.sync_api import sync_playwright
from pathlib import Path

def descargar_html_con_mi_brave(url_objetivo,pages=1):
    for  i in range(pages) :
        # Ruta al perfil de Brave  
        perfil_brave = rf'c:\Users\ffruc\AppData\Local\BraveSoftware\Brave-Browser\User Data'
        # Ruta al ejecutable de Brave
        ejecutable_brave = r'c:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
        

        with sync_playwright() as p:
            print("Iniciando Brave")
            
            # Abrimos el navegador con sesión iniciada
            context = p.chromium.launch_persistent_context(
                perfil_brave,
                executable_path=ejecutable_brave,
                headless=False, # Para que se vea el proceso
                args=["--disable-blink-features=AutomationControlled"] # Oculta que es un bot
            )

            page = context.new_page()
            
            # 2. Navegación  
            print(f"Entrando a: {url_objetivo}&page={i+1}")
            url_objetivo_page=url_objetivo+'&page='+str(i+1)
            page.goto(url_objetivo_page, wait_until="domcontentloaded")

            # Simulamos que un humano mira la página
            print("Simulando lectura humana...")
            time.sleep(random.uniform(3, 6)) # Pausa aleatoria
            
            # Hacemos un scroll suave hacia abajo para que carguen todos los elementos
            page.mouse.wheel(0, 800)
            time.sleep(2)
            # Sube un poco
            page.mouse.wheel(0, -300) 
            
            # Esperamos a que aparezcan los proyectos (el selector que vimos antes)
            try:
                page.wait_for_selector('.project-item', timeout=10000)
                
                # Obtenemos el HTML completo ya renderizado
                html_fuente = page.content()
                
                # Nombre de archivo con fecha para no sobrescribir
                link_work4=rf"c:\Users\ffruc\Desktop\html_pages"
                
                nombre_archivo = os.path.join(link_work4,str(i)+'_.hmtl')
                with open(nombre_archivo, "w", encoding="utf-8") as f:
                    f.write(html_fuente)
                
                # Contamos cuántos jobs hay en el código descargado 
                cantidad_jobs = html_fuente.count('class="project-item')
                print(f"Archivo guardado como: {nombre_archivo}")
                print(f"Se detectaron aproximadamente {cantidad_jobs} trabajos en el HTML.")
                
            except Exception as e:
                print(f"Error: No se encontraron los trabajos : {e}")

            # 4. Cerramos sesión de navegador
            print("Cerrando navegador...")
            time.sleep(random.uniform(2, 7))
            context.close()

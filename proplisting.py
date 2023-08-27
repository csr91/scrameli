import keyboard
import re
import pyautogui
import pyperclip
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import pygetwindow as gw 
import random  # Agrega esta línea para importar el módulo random

# Función para extraer el ID de la URL
def extract_id_from_url(url):
    match = re.search(r'MLA-(\d+)', url)
    if match:
        return match.group(1)
    else:
        return None

def paste_and_execute():
    # Pegar el código desde el portapapeles en la consola del navegador
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')

def authenticate_google_sheets():
    # Cargamos las credenciales desde el archivo auth.json
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    
    try:
        client = gspread.authorize(creds)
    except Exception as e:
        return None

    # Abrimos la hoja de cálculo por su URL
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1srVimvkcSl8Hh82y0x6lL-DXZhfDF4pEt20Le0NuhKw/edit#gid=0')
    return spreadsheet.worksheet('Proplisting')

def scroll_up():
    screen_height = pyautogui.size()[1]
    scroll_amount = -screen_height
    pyautogui.scroll(scroll_amount, x=pyautogui.position()[0], y=pyautogui.position()[1])

def scroll_down():
    screen_height = pyautogui.size()[1]
    scroll_amount = screen_height
    pyautogui.scroll(scroll_amount, x=pyautogui.position()[0], y=pyautogui.position()[1])

def main():
    # Intentar autenticarse con Google Sheets
    spreadsheet = authenticate_google_sheets()

    if spreadsheet is None:
        print("No se pudo autenticar con Google Sheets. El programa se detendrá.")
        return
    else:
        print("Autenticación con Google Sheets exitosa.")

    # Esperar 2 segundos
    time.sleep(2)

    # Obtener la ventana de Google Chrome por título
    chrome_windows = gw.getWindowsWithTitle("Google Chrome")

    if not chrome_windows:
        print("No se encontraron ventanas de Google Chrome abiertas.")
        return
    
    # Si hay ventanas de Chrome abiertas, activa la primera
    chrome_window = chrome_windows[0]
    chrome_window.activate()

    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.5)

    # Leer las URLs desde el archivo urls.txt
    with open('proplisting.txt', 'r') as file:
        urls = file.readlines()

    # Bucle para procesar cada URL
    for url in urls:
        url = url.strip()  # Eliminar espacios en blanco y saltos de línea
        if url:
            # Resto del código para procesar cada URL
            # Ctrl + L (seleccionar la barra de direcciones)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)

            # Ctrl + V (pega url)
            pyautogui.write(url)
            time.sleep(0.2)

            # Presionar Enter
            pyautogui.press('enter')
            time.sleep(4)

            scroll_down()
            scroll_up()
            scroll_down()
            scroll_up()

            # Presionar F12
            pyautogui.press('f12')
            time.sleep(2)

            # pyautogui.hotkey('shift', 'tab')
            # time.sleep(0.5)
            # pyautogui.hotkey('shift', 'tab')
            # time.sleep(0.5)
            # pyautogui.hotkey('shift', 'tab')
            # time.sleep(0.5)
            # pyautogui.hotkey('shift', 'tab')
            # time.sleep(0.5)

            # Copiar el primer código JavaScript al portapapeles
            js_code_1 = """
            // Selecciona el enlace "Ver teléfono"
            var verTelefonoLink = document.querySelector('.ui-seller-info__status-info-phones .ui-pdp-media__action');

            // Verifica si se encontró el enlace y si es visible
            if (verTelefonoLink && window.getComputedStyle(verTelefonoLink).display !== 'none') {
              // Simula un clic en el enlace
              verTelefonoLink.click();
            } else {
              console.log('El enlace "Ver teléfono" no fue encontrado o no es visible.');
            }
            """
            pyperclip.copy(js_code_1)
            paste_and_execute()

            time.sleep(2)
            pyautogui.press('f12')
            time.sleep(2)

            scroll_down()
            scroll_up()
            scroll_down()
            scroll_up()

            # Ctrl + F (buscar)
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)

            # Esperar antes de escribir
            time.sleep(0.2)

            # Escribir "no soy un robot" en la barra de búsqueda
            pyautogui.write("no soy un")
            time.sleep(0.3)

            # Presionar Esc para cerrar la barra de búsqueda
            pyautogui.press('esc')
            time.sleep(0.3)

            # Presionar Enter para realizar la búsqueda
            pyautogui.press('enter')
            time.sleep(20)

            # Presionar F12
            pyautogui.press('f12')
            time.sleep(2)

            scroll_down()
            scroll_up()
            scroll_down()
            scroll_up()

            # Copiar el tercer código JavaScript al portapapeles
            pyperclip.copy(js_code_1)
            paste_and_execute()

            time.sleep(2)
            pyautogui.press('f12')
            time.sleep(2)
            # Ctrl + F (buscar)
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)

            # Esperar antes de escribir
            time.sleep(0.5)

            pyautogui.write("Informacion")
            time.sleep(0.5)
            pyautogui.write(" del ")
            time.sleep(0.5)
            pyautogui.write("particula")
            time.sleep(2.5)

            # Presionar Esc para cerrar la barra de búsqueda
            pyautogui.press('esc')
            time.sleep(0.5)

            pyautogui.hotkey('shift', 'down')
            time.sleep(0.5)
            pyautogui.hotkey('shift', 'down')
            time.sleep(0.5)
            pyautogui.hotkey('shift', 'down')
            time.sleep(0.5)

            pyautogui.hotkey('ctrl', 'c')

            # Obtén el contenido del portapapeles
            tels = pyperclip.paste()

            texto = tels

            lineas = texto.split('\n')

            # Variables para almacenar las líneas con más de 4 números
            tel1 = ""
            tel2 = ""
            tel3 = ""

            ownername = ""  # Variable para almacenar el nombre del propietario

            for idx, linea in enumerate(lineas):
                if len(re.findall(r'\d', linea)) > 4:
                    if not tel1:
                        tel1 = linea
                    elif not tel2:
                        tel2 = linea
                    elif not tel3:
                        tel3 = linea
                    else:
                        break  # Ya tenemos tres líneas, podemos detener el bucle
                elif idx == 1:
                    ownername = linea

            # Imprimir los teléfonos y el nombre del propietario en pantalla
            if tel1:
                print("Teléfono 1:", tel1)
            if tel2:
                print("Teléfono 2:", tel2)
            if tel3:
                print("Teléfono 3:", tel3)
            if ownername:
                print("Nombre del propietario:", ownername)

            # Extraer el ID de la URL
            id_from_url = extract_id_from_url(url)
            
            if id_from_url:
                print("ID extraído:", id_from_url)
                
                # Agregar el ID a la hoja de cálculo
                row_values = [f"MLA-{id_from_url}", ownername, tel1, tel2, tel3]
                spreadsheet.append_row(row_values)
                
            else:
                print("No se pudo extraer el ID.")

if __name__ == "__main__":
    main()
import re
import pyautogui
import pyperclip
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import pygetwindow as gw 

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
    return spreadsheet.worksheet('Listings')

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

    # Leer las URLs desde el archivo listings.txt
    with open('listings.txt', 'r') as file:
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

            pyautogui.hotkey('ctrl', 'u')
            time.sleep(3.5)

            pyautogui.hotkey('ctrl', 'a')
            time.sleep(3.5)

            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.8)

            pyautogui.hotkey('ctrl', 'w')
            time.sleep(1.5)

            # Obtén el contenido del portapapeles
            html = pyperclip.paste()

            # Crear un objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Buscar todos los elementos 'div' con la clase 'ui-search-result__wrapper shops__result-wrapper'
            result_wrappers = soup.find_all('div', class_='ui-search-result__wrapper shops__result-wrapper')

            # Iterar sobre cada div encontrado y buscar el input con el nombre 'itemId'
            for result_wrapper in result_wrappers:
                input_element = result_wrapper.find('input', {'name': 'itemId'})

                if input_element:
                    item_id = input_element.get('value')
                    formatted_item_id = f"{item_id[:3]}-{item_id[3:]}"  # Agregar guión en el cuarto caracter
                    print("Item ID:", formatted_item_id)
                else:
                    print("No se encontró el elemento 'itemId' en el div")

                # Buscar los elementos li con la clase 'ui-search-card-attributes__attribute'
                attributes = result_wrapper.find_all('li', class_='ui-search-card-attributes__attribute')

                for attribute in attributes:
                    text = attribute.get_text()
                    if "m² cubiertos" in text:
                        m2_cubiertos = text
                        print("M² Cubiertos:", m2_cubiertos)
                    elif "ambs." in text:
                        ambs = text
                        print("Ambientes:", ambs)

                # Buscar el elemento span con la clase 'ui-search-item__group__element ui-search-item__location shops__items-group-details'
                location_element = result_wrapper.find('span', class_='ui-search-item__group__element ui-search-item__location shops__items-group-details')

                if location_element:
                    direccion = location_element.get_text(strip=True)
                    print("Dirección:", direccion)
                else:
                    print("No se encontró la dirección")

                # Obtener el título
                title_tag = result_wrapper.find('h2', class_='ui-search-item__title shops__item-title')
                if title_tag:
                    print("Title:", title_tag.get_text())

                # Obtener el contenido de la etiqueta de moneda
                currency_tag = result_wrapper.find('span', class_='andes-money-amount__currency-symbol')
                if currency_tag:
                    currency = currency_tag.get_text()
                
                # Obtener el contenido de la etiqueta de precio
                price_tag = result_wrapper.find('span', class_='andes-money-amount__fraction')
                if price_tag:
                    price = price_tag.get_text()
                
                # Concatenar moneda y precio
                full_price = f"{currency}{price}"
                
                print("Full Price:", full_price)

                # Buscar elementos 'a' con la clase 'ui-search-result__wrapper shops__result-wrapper'
                link = result_wrapper.find('a', class_='ui-search-link')
                
                if link:
                    href = link.get('href')  # Obtener el atributo href
                    print("URL:", href)
                else:
                    print("No se encontró enlace con la clase ui-search-link")
                
                # Agregar el ID a la hoja de cálculo
                row_values = [formatted_item_id, title_tag.get_text(), full_price, m2_cubiertos, ambs, link.get('href')]
                spreadsheet.append_row(row_values)

if __name__ == "__main__":
    main()
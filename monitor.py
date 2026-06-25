import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/2a397f33628a81ab1108859fd0a87a82#services"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

NO_CITAS_TEXTOS = [
    "No hay horas disponibles",
    "Inténtelo de nuevo dentro de unos días",
    "No hay agendas disponibles para este servicio",
]

def enviar_telegram(mensaje):
    if not BOT_TOKEN or not CHAT_ID:
        print("Falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "disable_web_page_preview": True,
    }

    r = requests.post(url, data=data, timeout=20)
    print("Telegram:", r.status_code, r.text)


def revisar_citas():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=30)
    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(" ", strip=True)

    print("Revisión:", datetime.now().isoformat())
    print(texto[:1000])

    if any(t in texto for t in NO_CITAS_TEXTOS):
        print("Resultado: no hay citas disponibles.")
        return

    mensaje = (
        "🚨 POSIBLE CITA DISPONIBLE 🚨\n\n"
        "La página del Consulado cambió y ya no aparece el mensaje normal de "
        "'No hay horas disponibles'.\n\n"
        f"Revisa ahora:\n{URL}"
    )

    enviar_telegram(mensaje)


if __name__ == "__main__":
    revisar_citas()

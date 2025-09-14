from tuya_iot import TuyaOpenAPI
import requests
import json
import time
from datetime import datetime
import hashlib
import hmac
from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, TB_ACCESS_TOKEN  # TB_ACCESS_TOKEN = token de tu Device en ThingsBoard

class TuyaRealtimeMonitor:
    def __init__(self):
        self.device_id = "eb7019cd9fe******bryvz"
        self.openapi = None
        self.access_token = None
        self.token_expire_time = None
        self.running = False
        self.update_interval = 2  # segundos
        self.previous_state = {}

    # ------------------------ Conexión Tuya ------------------------
    def connect(self):
        try:
            print("Conectando con Tuya IoT...")
            self.openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
            token_response = self.openapi.get('/v1.0/token', {'grant_type': 1})
            if token_response and token_response.get('success', False):
                self.access_token = token_response['result'].get('access_token')
                expire_time = token_response['result'].get('expire_time', 0)
                self.token_expire_time = time.time() + expire_time
                print(f"Conectado: token obtenido (expira en {expire_time}s)")
                return True
            else:
                print("Error al obtener token")
                return False
        except Exception as e:
            print(f"ERROR DE CONEXIÓN: {e}")
            return False

    def is_token_expired(self):
        buffer_time = 60
        return not self.token_expire_time or time.time() >= (self.token_expire_time - buffer_time)

    def refresh_token(self):
        try:
            token_response = self.openapi.get('/v1.0/token', {'grant_type': 1})
            if token_response and token_response.get('success', False):
                self.access_token = token_response['result'].get('access_token')
                expire_time = token_response['result'].get('expire_time', 0)
                self.token_expire_time = time.time() + expire_time
                print(f"Token renovado (expira en {expire_time}s)")
                return True
            return False
        except Exception as e:
            print(f"ERROR renovando token: {e}")
            return False

    def generate_signature(self, timestamp, method="GET", url_path=None):
        if not url_path:
            url_path = f"/v2.0/cloud/thing/{self.device_id}/shadow/properties"
        content_hash = hashlib.sha256("".encode('utf-8')).hexdigest()
        string_to_sign = f"{method}\n{content_hash}\n\n{url_path}"
        payload = ACCESS_ID + self.access_token + timestamp + string_to_sign
        signature = hmac.new(
            ACCESS_KEY.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
        return signature

    def get_device_status(self):
        if self.is_token_expired() and not self.refresh_token():
            print("No se pudo renovar token")
            return None
        url_path = f"/v2.0/cloud/thing/{self.device_id}/shadow/properties"
        url = f"https://openapi.tuyaus.com{url_path}"
        timestamp = str(int(time.time() * 1000))
        signature = self.generate_signature(timestamp, "GET", url_path)
        headers = {
            "sign_method": "HMAC-SHA256",
            "client_id": ACCESS_ID,
            "t": timestamp,
            "mode": "cors",
            "Content-Type": "application/json",
            "sign": signature,
            "access_token": self.access_token
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('result', {})
            return None
        except Exception as e:
            print(f"Error en solicitud: {e}")
            return None

    # ------------------------ Procesar datos para ThingsBoard ------------------------
    def process_for_thingsboard_individual(self, data):
        """Procesar datos y generar JSON con cada dato independiente en formato decimal"""
        if not data or 'properties' not in data:
            return None

        tb_json = {}
        for prop in data['properties']:
            code = prop.get('code')
            value = prop.get('value')

            # Convertir valores según tipo de dato esperado
            if code in ["cur_voltage1", "cur_voltage2"]:  # Voltaje en V
                tb_json[code] = round(float(value) / 10, 1)  
            elif code in ["cur_current1", "cur_current2"]:  # Corriente en A
                tb_json[code] = round(float(value) / 1000, 3)  
            elif code in ["cur_power1", "cur_power2"]:  # Potencia en W
                tb_json[code] = round(float(value) / 10, 1)  
            elif code in ["total_energy1", "total_energy2"]:  # Energía total en Wh
                tb_json[code] = round(float(value) / 1000, 3)  
            elif code in ["today_acc_energy1", "today_acc_energy2"]:  # Energía acumulada hoy
                tb_json[code] = round(float(value) / 1000, 3)  
            else:
                tb_json[code] = value  
        return tb_json

    # ------------------------ Enviar a ThingsBoard ------------------------
    def send_to_thingsboard(self, tb_json):
        url = f"https://thingsboard.cloud/api/v1/{TB_ACCESS_TOKEN}/telemetry"
        try:
            response = requests.post(url, json=tb_json, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print("Datos enviados a ThingsBoard correctamente")
            else:
                print(f"Error enviando datos: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Excepción enviando a ThingsBoard: {e}")

    # ------------------------ Bucle principal ------------------------
    def monitor_loop(self):
        while self.running:
            data = self.get_device_status()
            tb_json = self.process_for_thingsboard_individual(data)
            if tb_json:
                print(json.dumps(tb_json, indent=2))
                self.send_to_thingsboard(tb_json)
            time.sleep(self.update_interval)

    def start_monitoring(self):
        if not self.connect():
            print(" No se pudo conectar con Tuya")
            return
        self.running = True
        print(f"Iniciando monitoreo cada {self.update_interval}s...")
        try:
            self.monitor_loop()
        except KeyboardInterrupt:
            print("Monitoreo detenido por usuario")
        finally:
            self.running = False

# ------------------------ Ejecutar ------------------------
if __name__ == "__main__":
    monitor = TuyaRealtimeMonitor()
    monitor.start_monitoring()

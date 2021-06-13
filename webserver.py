from http import *
from time import *
from gpio import *
from email import *



#Variables de la lampara
# 0 = off, 1 = dim, 2 = on
lamp01=0
lamp01_on=2
lamp01_off=0
lamp01_dim=1

#Variables de la tv
# 0 = Off  1 = On
tv01=1
tv01_on=1
tv01_off=0

#Variables de la cafetera
# 0 = Off  1 = On
cafe01=2
cafe01_on=1
cafe01_off=0

#Variables para motion sensors
ms01=3
ms02=4

#Variables para puertas
#customWrite(0, "0,0");
#door: 0 = closed, 1 = open, -1 = don't care
#lock: 0 = unlock, 1 = lock, -1 = don't care
pt01=5
pt01_closed_locked="0,1"
pt01_open_unlocked="1,0"
pt02=6
pt02_closed_locked="0,1"
pt02_open_unlocked="1,0"
#Variables para Ventana
#state: 0 = closed, 1 = open
ven01=7
ven01_open=1
ven01_close=0

def setupPines():
	#Lamp01 pin mode
	pinMode(lamp01, OUT)
	#Tv01 pin mode
	pinMode(tv01, OUT)
	#Cafe01 pin mode
	pinMode(cafe01, OUT)
	#Sensores Modo IN
	pinMode(ms01,IN)
	pinMode(ms02,IN)
	#puertas
	pinMode(pt01,OUT)
	pinMode(pt02,OUT)
	#Ventana
	pinMode(ven01,OUT)


def onRouteRoot(url, response):
	print("Request for /");
	response.sendFile("/index.html")
	

def onRouteWildcard(url, response):
	print("Request for " + url)
	response.send("wildcard")
	
#Funciones http para lampara
def onLamp01Encender(url,response):
	print("/lamp01/encender")
	customWrite(lamp01, lamp01_on)
	print("Lamp01 encendido")
	
def onLamp01Apagar(url,response):
	print("/lamp01/apagar")
	customWrite(lamp01, lamp01_off)
	print("Lamp01 apagada")
	
def onLamp01MediaLuz(url,response):
	print("/lamp01/medialuz")
	customWrite(lamp01, lamp01_dim)
	print("Lamp01 Media luz")

#Funciones http para TV
def onTv01Encender(url,response):
	print("/tv01/encender")
	customWrite(tv01, tv01_on)
	print("Tv01 encendido")
	
def onTv01Apagar(url,response):
	print("/tv01/apagar")
	customWrite(tv01, tv01_off)
	print("Tv01 apagada")
	
#Funciones http para Cafetera
def onCafe01Encender(url,response):
	print("/cafe01/encender")
	customWrite(cafe01, cafe01_on)
	print("Cafe01 encendido")
	
def onCafe01Apagar(url,response):
	print("/cafe01/apagar")
	customWrite(cafe01, cafe01_off)
	print("Cafe01 apagada")


#Colocar llave a las puertas, cerrar la ventana y encender la lámpara de mesa
def onLlavePuertasCerrarVentanaYEncenderLampara(url,response):
	print("Cerrando y bloqueando puertas")
	customWrite(pt01,pt01_closed_locked)
	customWrite(pt02,pt02_closed_locked)
	print("Puertas cerradas y bloqueadas")
	print("Encendiendo la lampara")
	customWrite(lamp01, lamp01_on)
	print("Lampara encendida")
	print("Cerrando la ventana")
	customWrite(ven01, ven01_close)
	print("Ventana Cerrada")
#Quitar llave a las puertas, abrir la ventana y apagar la lámpara de mesa
def onQuitarLlavePuertasAbrirVentanaYApagarLampara(url,response):
	print("Abriendo puertas")
	customWrite(pt01,pt01_open_unlocked)
	customWrite(pt02,pt02_open_unlocked)
	print("Puertas Abiertas")
	print("Apagando la lampara")
	customWrite(lamp01, lamp01_off)
	print("Lampara apagada")
	print("Abriendo la ventana")
	customWrite(ven01, ven01_open)
	print("Ventana Abierta")
	
#Cliente de Correo
def onEmailReceive(sender, subject, body):
	print("Received from: " + sender)
	print("Subject: " + subject)
	print("Body: " + body)

def onEmailSend(status):
	print("send status: " + str(status))

#Setup del cliente
EmailClient
def setupCorreo():
	EmailClient.setup(
		"admin@empresay.com.sv",
		"empresay.com.sv",
		"admin",
		"123456"
	)
	EmailClient.onReceive(onEmailReceive)
	EmailClient.onSend(onEmailSend)

#Chequear Sensores ms01 y ms02
def crearTitulo(name):
	return "Movimiento en sensor: "+name
	
def crearCuerpo(name):
	return "Movimiento en sensor: "+name+" datetime: aca ira el datetime que no me lo quiere importar"

def chequearSensor(which,name):
	if digitalRead(which) == HIGH:
		print("Sending email to usu01 movement in sensor: "+name);
		EmailClient.send("usu01@empresay.com.sv",crearTitulo(name) , crearCuerpo(name))
	else:
		print("Everything ok on sensor: "+name)
	

def main():
	#Setup Pines
	setupPines()
	#Setup Correo
	setupCorreo()
	HTTPServer.route("/", onRouteRoot)
	HTTPServer.route("/*", onRouteWildcard)
	#Lamp01 handlers http
	HTTPServer.route("/lamp01/encender", onLamp01Encender)
	HTTPServer.route("/lamp01/apagar", onLamp01Apagar)
	HTTPServer.route("/lamp01/medialuz", onLamp01MediaLuz)
	#Tv01 handlers http
	HTTPServer.route("/tv01/encender", onTv01Encender)
	HTTPServer.route("/tv01/apagar", onTv01Apagar)
	#Cafe01 handlers http
	HTTPServer.route("/cafe01/encender", onCafe01Encender)
	HTTPServer.route("/cafe01/apagar", onCafe01Apagar)
	#Colocar llave a las puertas, cerrar la ventana y encender la lámpara de mesa
	HTTPServer.route("/all/closeandlock", onLlavePuertasCerrarVentanaYEncenderLampara)
	#Quitar llave a las puertas, abrir la ventana y apagar la lámpara de mesa
	HTTPServer.route("/all/openunlock", onQuitarLlavePuertasAbrirVentanaYApagarLampara)

	# start server on port 80
	print(HTTPServer.start(80))

	# don't let it finish
	while True:
		chequearSensor(ms01,"ms01")
		chequearSensor(ms02,"ms02")
		EmailClient.receive()
		sleep(5)

if __name__ == "__main__":
	main()
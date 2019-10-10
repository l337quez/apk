import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.config import Config

#Config.set('input','mouse','mouse')
import time
import threading
import socket
import sys
import os
from os import remove
import os.path as path
from decimal import Decimal

#NOTIFICACIONES
from plyer import notification

#VIBRADOR
from plyer import vibrator

#importamos libreria de JSON
import json
#libreria de tiempo para los delay
from time import sleep

global ban 
ban=False


#configuracion de pantalla  
Config.set('graphics', 'width', 320)
Config.set('graphics', 'height', 500)



#Poner toogle button para conectar y deconector
#http://pythonmobile.blogspot.com/2014/06/35-togglebutton.html


#Abrimos un archivo txt y la ip que se ingrese se va guardar en el arhivo
IP = open ('ip.txt','w+')
IP.write("192.168.1.1")
ESP_IP= IP.read()
print(ESP_IP)
IP.close()

PUERTO = open ('puerto.txt','w+')
PUERTO.write("8266")
PUERTO.close()
PUERTO = open ('puerto.txt','r')
line= PUERTO.read()
ESP_PORT=line[:-1]
ESP_PORT=int(ESP_PORT)
print(ESP_PORT)
PUERTO.close()

# AF_INET= Direcciones de internet para ipv4   
# SOCK_STREAM= tipo de socket para Protocolo TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("prueba esro se repite 12312")

class Box01(BoxLayout):
	
	def __init__(self):
		super(Box01,self).__init__()
		self.add_widget(BoxNegro())
		


class BoxNegro(BoxLayout):
	# id de los suiches s1,s2...
	s1= ObjectProperty()
	s2= ObjectProperty()
	s3= ObjectProperty()
	s4= ObjectProperty()

#s.send(msg)


#CHECKBOX
	#def checkbox_clicked(self, instance, value):
		#if value is True:
			#value_check_ip= True
			#print("Checked")
		#else:
			#print("Unchecked")
			#value_check_ip= False
        #return value_check_ip


#validar ip... si ingresa una ip mala
 #OSError: [Errno 113] No existe ninguna ruta hasta el `host'
#valñidar una exepcion


#AQUI LLEGAN TODOS LOS DATOS Y SE GUARDAN EN UN ARCHIVO TXT
#DETECCION DE CORRIENTE ALTA Y NOTIFICACION
	try: 
        
		print ("ENTRO AL TRY")
		data=s.recv(1024)
		with open('data.txt', "w") as f:
			f.write(data)
			sleep(0.1)
		with open('data.txt', "r") as f:  
			strin=str(data)
			global DATA
			DATA=f.read()
		
		Datas=data.decode()
		dato_rec=True

	except Exception:
		dato_rec=False

    
	if dato_rec== True:
		with open('alerta.txt', "w") as f:
			f.write(Datas)
			sleep(0.1)
		with open('alerta.txt', "r") as f:  
			strin=str(Datas)
			I_ALERTA=f.read()

        #verificamos que este la clave i_alerta
		if "i_alerta" in json_arreglo:
			json_arreglo = json.loads(I_ALERTA) 
			corrientem=eval(json_arreglo.get("i_alerta"))
			
			#NOTIFICACIONES
			#Generamos la notificacion con vibracion
			title = b"Alerta".decode('utf8')
			message = f" Alerta de corriente"
			ticker = "La corriente tiene un valor de:" + corrientem + "superando el valor maximo"
			app_name = "conexion"
			app_icon = "plyer-icon.png"
			toast = True
			notification.notify(title=title,
                                message=message,
                                app_name=app_name,
                                app_icon=app_icon,
                                timeout=10,
                                ticker=ticker,
                                toast=toast
                                )
			
			#ponemos a vibrar el telefono
			vibrator.vibrate(10)
        
		else:
			print("NO HAY ALERTA")          

            




# BOTON DESCONECTAR 

	def desconectar(self):
		self.img_conect.source= 'noconectado.png' 
		self.img_update.source= 'noupdate.png'
		#enviamos el dato c para que el servidor tambien cierre
		dato = str.encode("D")
		print("Enviando D")
		#s.send(dato)
		
#Agregamos una execpcion
		try:
			s.send(dato)
		except BrokenPipeError:
			print("Conexion Rota")
        #cambiamos el titulo de texto
		self.msg.text= 'Desconectado'
#Agregamos una execpcion
		try:
			s.shutdown(socket.SHUT_RDWR)
		except OSError:
			print("El otro extremo de la conexión no está conectado")
		s.close()





# BOTON ACTUALIZAR     
	def actualizar(self):
		dato = str.encode("B")
		print("Enviando B")
		s.send(dato)
		
		#cambiamos la imagen de actualizar
		self.img_update.source= 'update1.png'
		
		data= s.recv(1024)
		print(data)
		datas=data.decode()

		if data != b'A':
			with open('update.txt', "w") as f:
				f.write(datas)
			#for ch in data:
				#f.write(datas)
			sleep(0.5)
			with open('update.txt', "r") as f:
				strin=str(datas)
				dataa=f.read()
				
				
				
				
				
			print(dataa)
			print(type(dataa))
			JSON = json.loads(dataa)
			print(JSON)
			print(type(JSON))
			if "c1" in JSON:
				print("La corriente 1 es:", JSON["c1"])
				
				#convertimo esto en decimal para usar la libreria
				corriente1=eval(JSON.get("c1"))
				
				co_decimal=Decimal(corriente1)
				
				if co_decimal.compare(Decimal(0.1)) <= Decimal(0.1):
                    #NO hay corriente, por lo tanto no hay voltaje
                    #para solventar esto, hayq eu colocar un sensor de voltaje
					corriente1=0
				else:
					print ("Si Hay corriente")
				
				#print(corriente1)
				potencia1= str(float(corriente1)*120)
				#setiamos la potencia
				self.p1.text=potencia1
				print(type(corriente1))
				#setiamos la corriente
				self.i1.text=str(corriente1)
				#setiamos la corriente IRMS
				corrienteRMS=str(float(corriente1)*.707) #corriente*sqrt(2)
				self.i1rms.text=corrienteRMS
				
			elif "i_alerta" in JSON:
				print("Corriente ALERTA:", JSON["i_alerta"])
				corrientem=str(eval(JSON.get("i_alerta")))
				
				
################################################################################################    NOTIFICACIONES
			#Generamos la notificacion con vibracion
				title = b"Alerta".decode('utf8')
				message = f" Alerta de corriente"
				ticker = "La corriente tiene un valor de:" + corrientem + "superando el valor maximo"
				app_name = "conexion"
				app_icon = "plyer-icon.png"
				toast = True
				notification.notify(title=title,
                                message=message,
                                app_name=app_name,
                                app_icon=app_icon,
                                timeout=10,
                                ticker=ticker,
                                toast=toast
                                )
			
				#ponemos a vibrar el telefono
				vibrator.vibrate(10)
				
				
				
				
				
				
				
				
				
				
				
				
			else:
				print ("No se encuentra")


		return corriente1
		
		
		#cliente = s.makefile("rwb", buffering=0)
		#cliente.write(b"Hello World!")
		#cliente.flush()
		#print(cliente)
		#print(server)
		#line = server.readline()
		#print (repr(line))
		#line = server.readline()
		#print (repr(line))
		
		#print(data)
		#datas= data.decode()
		#print(datas)
		#sleep(0.9)
		#with open("update.tx", 'w') as datas:
			#datas.write(datas)
			


# BOTON CONECTAR     
	def conectar(self):
		#Enviamos una letra A, para que no se confunda con otro dato
		#Enviamos un  A  como ping
		dato = str.encode("A")
		print("Enviando data")
		
        #Agregamos una execpcion
		try:
			s.send(dato)
		except BrokenPipeError:
			print("Conexion Rota")
		# variable que recibimos del servidor (nodemcu)

		except OSError:
			print("Archivo incorrupto en el Socket")
		# variable que recibimos del servidor (nodemcu)
		data = ""



		#recibimos la data con un while
		while True:
			data= s.recv(1024)
			print("Recibiendo data")
			print(data)
			data=data.decode("utf-8")
			print("Decodificando data")
			print(data)
			#cambiamos el titulo de texto
			self.msg.text= 'Conetando'
			
			if data=="A" :
 				print ("Conetado")   
 				print(data)
 				#salto de linea
 				print("")
 				#cambiamos el titulo de texto
 				self.msg.text= 'Conetado'	
 				
 				#cambiamos la imagen a enchufe conectado
 				self.img_conect.source= 'conectado.png'
 				


#llega un JSON con los estados de los suiches guardados en la EEPROM                  
			elif data != 'A': 
 				#datas=data.decode()
 				print("entrooo al if")
 				print(data)
 				suiches = open ('suiches.txt','w+')
 				suiches.write(data)
 				suiches.close()
# si no queremos guardar en txt ver https://stackoverflow.com/questions/26247353/issues-with-tcp-on-arduino-reading-strings-from-a-python-tcp-socket-server
 				with open('suiches.txt', "r") as suiches:
 					 dataa=suiches.read()
 				json_suiches = json.loads(dataa)    
 				print("El Suiche 1 es:", json_suiches["l1"])
 				print(type(json_suiches["l1"]))
 				suiche1=json_suiches["l1"]
 				if suiche1=="false":
 					self.s1.active= True 

 				else:
 					self.s1.active= False 
 				
 				#El shiel rele trabaja con los estados invertidos, invertimos el valor
 				#print("El Suiche 1 negado es:", json_suiches["l1"])
 				#suiche1= not json_suiches["l1"]
 				#print(type(suiche1))
 				#print(suiche1)
 				
 				
 				#Suichamos los estados guardados en la EEPROM del nodemcu
 				#if suiche1 == False:
  					#self.s1.active= False              
 				#else:
  					#self.s1.active= False 


 				#self.s4.disabled= True

 				#salimos del ciclo while con break
 				break

		print("salio del while")
		#if data=="AA" :
		

		
# RELE 1	
	def server1(self, instance, value) :
		#Llamamo a la funcion conectar para que valiede el estado del 
		#servidor
		#BoxNegro.conectar(self)
		#if bandera== True:
		if value is True:
            #creamos un diccionario en python
            #l = load   c=current
            #Negamos el valor porque el shield rele trabaja al reves
			mensaje = {"l1": not value}
			#convertimos el diccionario en json
			msg = json.dumps(mensaje)
			#convertiendo JSON a bytes
			msg =str.encode(msg)
			print(msg)
			s.send(msg)
			#print("encendido")
			#dato = str.encode("A")
			#s.send(dato)
			#s.close()
		elif value is False:
			#print("NO encendido")
			#dato = str.encode("B")
			#s.send(dato)
			#probamos enviando JSON
			#creamos un diccionario en python
			estado= value
			mensaje = {"l1": not estado}
			#convertimos el diccionario en json
			msg = json.dumps(mensaje)
			#convertiendo JSON a bytes
			msg =str.encode(msg)
			print(msg)
			s.send(msg)
			#s.close()		


			


    
    
    


# PESTAÑA CONFIG
	def guardar_current(self,i_maxima):
		#Aqui se enviaran los valores de corrientes al servidor
		#creamos el diccionario
		msg = {"lm1": 2}
		#le asignamos el valor ingresado por la input al diccionario
		msg["lm1"]=float(i_maxima)
		#convertimos el diccionario en json
		msg = json.dumps(msg)
		#convertiendo JSON a bytes
		msg =str.encode(msg)
		print(msg)
		#enviamos el JSON
		s.send(msg)



		
#PESTAÑA LOGIN
	def guardar_login(self, input_puerto, input_ip):
        
		#Si existe algun dato guardado anteriormente lo eliminamos
		if path.exists("puerto.txt"):
			remove("puerto.txt")
			
		elif path.exists("ip.txt"):
			remove("ip.txt") 
		
		elif path.exists("suiches.txt"):
			remove("suiches.txt")
			
		elif path.exists("update.txt"):
			remove("update.txt")
			
		
		if self.check_ip.active:
			# Esta es la ip ESTATICA o ip defaul
			with open('ip.txt', "w") as IP:
				IP.write("192.168.11.9")
			PUERTO= open('puerto.txt', 'w+')
			PUERTO.write(input_puerto)
			PUERTO.close()
			with open('ip.txt', "r") as IP:
				ESP_IP=IP.read()
			ESP_PORT = int(input_puerto)
			print(ESP_IP)
			print(ESP_PORT)
			#s.connect((ESP_IP , ESP_PORT))
			#elimnamos mensaje
			self.msg_error.text= 'Espere un momento'
			            
		else:
			with open('ip.txt', "w") as IP:
				IP.write(input_ip)
			with open('ip.txt', "w") as PUERTO:
				PUERTO.write(input_puerto)
			ESP_IP = str(input_ip)
			ESP_PORT = int(input_puerto)
			print(ESP_IP)
			print(ESP_PORT)
			#s.connect((ESP_IP , ESP_PORT))
			#elimnamos mensaje
			self.msg_error.text= 'Espere un momento'
			
			
		#return ESP_IP
# Agregamos una exepcion en el caso de que la ip o el puerto este mal
		try:
			#Connect se usa para conexion remota
			s.connect((ESP_IP , ESP_PORT))
			self.msg_error.text= 'Conexion Exitosa'
		except OSError:
			#pass
			print("IP incorrecta")
			self.msg_error.text= 'Error: IP Incorrecta'
			s.close() #cerramos socket
		#finally:
			#s.close()


class BoxRed(BoxLayout):
	None
	
class BoxGreen(BoxLayout):
	None
	
class BoxBlue(BoxLayout):
	None


class MainApp(App):

	#Titulo de la ventana
	title = "Conexion al servidor"
	
	#Eliminar el menu de opciones de kivy en el telefono
	def open_settings(*args):
		pass
	
	
	def build(self):
		#Hacemos una instancia de la clase para enviar la IP ingresada
		#port_and_ip=BoxNegro()
		#port_and_ip.guardar_login.ESP_IP=
		

		print("prueba esro se repite 888888")	
		try:
			#Connect se usa para conexion remota
			s.connect((ESP_IP , ESP_PORT))
		except OSError:
			print("IP incorrecta")
			
			




		return Box01()
		
if __name__ == "__main__":
	MainApp().run()

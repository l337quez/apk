import kivy
kivy.require("1.9.2")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import time
import threading
import socket
import sys
import os

from kivy.config import Config

#NOTIFICACIONES
from plyer import notification


#importamos libreria de JSON
import json
#libreria de tiempo para los delay
from time import sleep

global ban 
ban=False

#configuracion de pantalla  primera
#Config.set('graphics', 'width', 300)
#Config.set('graphics', 'height', 400)

#configuracion de pantalla  segunda
Config.set('graphics', 'width', 330)
Config.set('graphics', 'height', 400)



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



#NOTIFICACIONES
	def do_notify(self):
		title = b"titulo".decode('utf8')
		message = f" Mensaje "
		ticker = "Alarma"
		app_name = "app"
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

		#toast = True
		#notification.notify(title=title,
                                #message=message,
                                #app_name=app_name,
                                #app_icon=app_icon,
                                #timeout=10,
                                #ticker=ticker,
                                #toast=toast
                                #)





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
		self.msg_nc.text= 'Desconectado'
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
			y = json.loads(dataa)
			print(type(y))
			print("La corriente 1 es:", y["c1"])
			corriente1=eval(y.get("c1"))
			#print(corriente1)
			potencia1= str(float(corriente1)*120)
			self.p1.text=potencia1
			print(type(corriente1))
			self.i1.text=y.get("c1")
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
 				#El shiel rele trabaja con los estados invertidos, invertimos el valor
 				print("El Suiche 1 negado es:", json_suiches["l1"])
 				suiche1= not json_suiches["l1"]

 				
 				#Suichamos los estados guardados en la EEPROM del nodemcu
 				self.s1.active= suiche1
 				#self.s2.active= suiche2
 				#self.s3.active= suiche3
 				#self.s4.active= suiche4
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
	def guardar_current(self,input_i1, input_i2, input_i3, input_i4):
		#Aqui se enviaran los valores de corrientes al servidor
		#creamos el diccionario
		msg = {"lm1": 2,"lm2": 2,"lm3": 2,"lm4": 2}
		#le asignamos el valor ingresado por la input al diccionario
		msg["lm1"]=input_i1
		msg["lm2"]=input_i2
		msg["lm3"]=input_i3
		msg["lm4"]=input_i4
		#convertimos el diccionario en json
		msg = json.dumps(msg)
		#convertiendo JSON a bytes
		msg =str.encode(msg)
		print(msg)
		print("DESCONMENTAR LINEA PARA ENVIRA SOCKET")
		#enviamos el JSON
		#s.send(msg)



		
#PESTAÑA LOGIN
	def guardar_login(self, input_puerto, input_ip):
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
	
	
	def build(self):
		#Hacemos una instancia de la clase para enviar la IP ingresada
		#port_and_ip=BoxNegro()
		#port_and_ip.guardar_login.ESP_IP=
		

			
		try:
			#Connect se usa para conexion remota
			s.connect((ESP_IP , ESP_PORT))
		except OSError:
			print("IP incorrecta")
			
			




		return Box01()
		
if __name__ == "__main__":
	MainApp().run()

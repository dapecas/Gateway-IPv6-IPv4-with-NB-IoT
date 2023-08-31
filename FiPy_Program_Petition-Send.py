import pycom
from network import WLAN, LTE
import urequests
import time
pycom.pybytes_on_boot(True)

# ------ Funciones para la conexión WiFi ------

def connect_wifi(ssid, password):
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(ssid, auth=(WLAN.WPA2, password), timeout=5000)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Conectado a WiFi:", ssid)

def disconnect_wifi():
    wlan = WLAN()
    if wlan.isconnected():
        wlan.disconnect()
        wlan.deinit()
    print("Desconectado de WiFi")

def fetch_data_from_server(url):
    pycom.rgbled(0x0000FF)  #azul
    response = urequests.get(url)
    if response.status_code == 200:
        print(response.text)
        return response.text
    else:
        print("Error:", response.status_code)
        return None

# ------ Funciones para la conexión LTE ------

def connect_lte():
    lte = LTE()
    lte.init()
    lte.attach(band=20, apn="-------")  # APN of the operator

    while not lte.isattached():
        time.sleep(0.5)
        pycom.rgbled(0xff0000)  #red
        print(lte.send_at_cmd('AT!="fsm"'))

    print('attached')
    lte.connect()
    while not lte.isconnected():
        time.sleep(0.5)
    print("Conectado a LTE")

def disconnect_lte():
    lte = LTE()
    if lte.isconnected():
        lte.disconnect()
    #if lte.isattached():
     #   lte.dettach()
    print("Desconectado de LTE")

def send_to_pybytes(data):
    if(pybytes.isconnected()):
        print("Mandando")
        pybytes.send_signal(1, data)
        pycom.rgbled(0x7f7f00)  #yellow
    time.sleep(60)
    pycom.rgbled(0xff00) #green
    time.sleep(5)
    pass

# ------ Script principal ------
while True:
	disconnect_wifi()
	disconnect_lte()
	# Conexión WiFi y petición REST
	print("Comienzo")
	connect_wifi("------", "-----")  # Local wifi network, user and password
	ruta = '/bsn/all'
	url = 'http://192.168.0.204:5000' + ruta
	response = fetch_data_from_server(url)
	print(response)
	data = response
	print("Datos guardados")
	disconnect_wifi()

	# Conexión LTE y envío a Pybytes
	connect_lte()
	send_to_pybytes(data)
	disconnect_lte()

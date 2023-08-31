from flask import Flask
from coapthon.client.helperclient import HelperClient
from datetime import datetime

DEVICE_PORT = 5683

def create_client(device_ip):
	return HelperClient(server=(device_ip, DEVICE_PORT))

def name(deviceIP):
	deviceType = deviceIP[16:19]
	ip_short = deviceIP[-2:]
	if(deviceType=='201'):
		ip_short = 'BSN01_' + ip_short
	return ip_short

def prefixID(deviceIP):
	host = deviceIP
	prefixID = host.split("::")[0]
	return prefixID

def readDevices():
	with open('/root/udp-server-linux/responding-devices.txt', 'r') as f:
		devices = [line.split(',')[0].strip() for line in f.readlines()]
	return devices

def fetch_resource(device_ip, resource_name):
	client = create_client(device_ip)
	response = client.get('/' + resource_name)
	client.stop()
	return response.payload

app = Flask(__name__)

#Ruta 1
@app.route('/')
def index():
	msg = """
	<a href="http://192.168.0.204:5000/bsn/<recurso>/<deviceIP>">http://192.168.0.204:5000/bsn/<recurso>/<deviceIP></a> -> Info por recurso<br>
	<a href="http://192.168.0.204:5000/bsn/all/<deviceIP>">http://192.168.0.204:5000/bsn/all/<deviceIP></a> -> Toda info de un solo sensor<br>
	<a href="http://192.168.0.204:5000/bsn/all">http://192.168.0.204:5000/bsn/all</a> -> Toda la info de los dispositivos conectados al BatLink<br>
	"""
	return msg

@app.route('/bsn/<recurso>/<deviceIP>', methods=['GET'])
def senseRecurso(deviceIP, recurso):
	payload = fetch_resource(deviceIP, recurso)

	if(recurso=='rssi'):
		return "{},{}".format(deviceIP, payload), 200
		
	if(recurso=='values'):
		return "{},{}".format(deviceIP, payload), 200
		
	if(recurso=='event_values'):
		values = payload.split(';')
		return "{},{},{},{},{},{},{}".format(device_ip, device_name(deviceIP), payload, *values), 200
	return "Recurso no reconocido", 404
		
@app.route('/bsn/all/<deviceIP>', methods=['GET'])
def senseAll(deviceIP):
	timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
	prefix = prefixID(deviceIP)
	responseR = fetch_resource(deviceIP, 'rssi')
	responseEV = fetch_resource(deviceIP, 'event_values')
	name_short = name(deviceIP)
	values = responseEV.split(';')

	response_body = "{},{},{},{},{},{},{},{},{}, {}".format(prefix, name_short, "unknown", timestamp, values[0], values[1], values[2], values[3], values[4], responseR)
	return response_body, 200


@app.route('/bsn/all', methods=['GET'])
def allSenses():
	listDevice = readDevices()
	responses = []
	for device in listDevice:
		response_body = senseAll(device)
		responses.append(response_body[0])

	return ",".join(responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

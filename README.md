# Gateway-IPv6-IPv4-with-NB-IoT
Gateway IPv6 to IPv4 with NB-IoT

Development of an IPv6/IPv4 communication gateway with NB-IoT for IoT network. IoT devices with IEEE 802.15.4 communication with 6LoWPAN adaptation (IPv6) to the public Internet (IPv4) have been exposed.

For this purpose, a hub and two environmental sensors with IEEE 802.15.4 connection with 6LoWPAN adaptation, a FiPy module with an Expansion Board and a Raspberry Pi to host a Home Assistant service have been used.

The IoT network hub runs an API created with the Flask microframework in Python language. On the FiPy, it runs a program created in MicroPython. The API is able to make CoAP requests from the hub to the environmental sensors. The FiPy module makes requests to the API via WiFi connection and sends the data via NB-IoT to Pybytes, the integration platform of Pycom (developer of FiPy). From there, Pybytes will send the data to Home Assistant thanks to a Web Hook integration.

At Home Asisstant, data arrives, is processed and stored in an InfluxDB database. This database has been connected to Grafana to create dynamic and customisable control panels.

import requests
import time
import json 

url = 'http://localhost:8082/'
pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'

ids = []

i=0

urls = {

"qft5" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Victima/Qft5Qu.py",
"Espia4" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Espia/circuito_espia_4.py"
}

for elem in urls:
    data = {"url":urls[elem] ,"shots" : 10000, "policy":"time"}
    print(elem+":"+requests.post(url+pathCircuit, json = data).text)



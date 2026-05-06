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
"CargaMedia1" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia2" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia3" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia4" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia5" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia6" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia7" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia8" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia9" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia10" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia11" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia12" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia13" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia14" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia15" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia16" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia17" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia18" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia19" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia20" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia21" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia22" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia23" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia24" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia25" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia26" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia27" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia28" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia29" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",
"CargaMedia30" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil1/Carga_MediaP1.py",

}

for elem in urls:
    data = {"url":urls[elem] ,"shots" : 10000, "policy":"time"}
    print(elem+":"+requests.post(url+pathCircuit, json = data).text)



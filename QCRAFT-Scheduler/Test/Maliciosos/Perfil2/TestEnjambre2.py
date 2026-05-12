import aiohttp
import asyncio
url = 'http://localhost:8082/'

pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'


urls = {

"qft5" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Victima/Qft5Qu.py",
"CargaMedia1" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia2" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia3" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia4" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia5" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia6" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia7" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia8" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia9" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia10" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia11" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia12" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia13" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia14" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia15" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia16" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia17" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia18" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia19" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia20" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia21" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia22" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia23" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia24" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia25" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia26" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia27" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia28" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
"CargaMedia29" : "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Enjambre/Carga_MediaP2.py",
}

async def post_request(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()

async def main():
    data_template = {
        "url": "",
        "shots": 10000,
        "provider": ['ibm'],
        "policy": "time"
    }
    async with aiohttp.ClientSession() as session:
        tasks = []
        for name, url_value in urls.items():
            data = data_template.copy()
            data["url"] = url_value
            task = post_request(session, url + pathCircuit, data)
            tasks.append(task)
            
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)

asyncio.run(main())



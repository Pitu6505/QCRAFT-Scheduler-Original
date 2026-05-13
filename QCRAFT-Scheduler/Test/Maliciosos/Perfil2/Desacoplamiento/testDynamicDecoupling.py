import aiohttp
import asyncio

url = 'http://localhost:8082/'
pathCircuit = 'circuit'


urls = {
    "qft5": "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Victima/Qft5Qu.py",
    "CargaAlta": "https://raw.githubusercontent.com/Pitu6505/QCRAFT-Scheduler-Original/refs/heads/Comprobacion-de-Circuitos-Malware/CircuitosGenerados/Agresores/Perfil2/Carga_AltaP2.py"
}


async def post_request(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()


async def main():
    data_template = {
        "url": "",
        "shots": 10000,
        "provider": ['ibm'],
        "policy": "time",
        "mitigation": ""
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        for name, url_value in urls.items():
            data = data_template.copy()
            data["url"] = url_value
            # Solo habilitar DD para la víctima (qft5)
            data["mitigation"] = "dynamic_decoupling" if name == "qft5" else ""
            task = post_request(session, url + pathCircuit, data)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)


if __name__ == '__main__':
    asyncio.run(main())

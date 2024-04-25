import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
    token = "token.json"
    credentials = None
    if os.path.exists(token):
        credentials = Credentials.from_authorized_user_file(token, SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(token, "w") as token:
            token.write(credentials.to_json())
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        data = open("secrets.json")
        secrets = json.load(data)

        result = sheets.values().get(spreadsheetId=secrets["spreadsheetId"], range="encuesta!A2:E").execute()
        values = result.get("values", [])

        # Los valores de los vectores representan importancia del proyecto en: 
        # [ia, programacion, infraestructura, analisis, diseño] 
        # (es a modo de ejemplo para ver si funciona)
        proyectos = {
            "BOTCIA":[5,5,2,2,2],
            "INFRAIT":[1,3,5,2,2],
            "TABI":[1,1,1,5,5]
        }

        proyectos_vectores = np.array(list(proyectos.values()))

        i = 2 # El valor de la primer fila donde quiero guardar el proyecto recomendado (La fila 1 son los titulos de las columnas)

        # Determino el mejor proyeto para cada fila de datos de la hoja de calculos
        for row in values:
            print(row)
            postulante = np.array(row)
            similitudes = cosine_similarity(postulante.reshape(1,-1), proyectos_vectores)[0]
            for proyecto, similitud in zip(proyectos.keys(), similitudes):
                print(f"Calculo de {proyecto}: {similitud}")
            proyecto_recomendado = list(proyectos.keys())[np.argmax(similitudes)]
            print(f"El proyecto recomendado es {proyecto_recomendado}")

            # Guardo el proyecto recomendado en la hoja de calculos
            sheets.values().update(spreadsheetId=secrets["spreadsheetId"], range=f"encuesta!H{i}", valueInputOption="USER_ENTERED", body={"values": [[f"{proyecto_recomendado}"]]}).execute()

            i = i+1 #Incremento el valor de la fila para que en la proxima iteracion se almacene el proyecto recomendado en la celda correcta

    except HttpError as error:
        print(error)
        
if __name__ == "__main__":
    main()
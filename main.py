import requests
import os
import shutil
from io import StringIO
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup


years = list(range(2021,2025))
equipos=['teams']
#teams = ['alpine','aston-martin']
url_equipos="https://www.formula1.com/en/{}.html" # 
url_team ="https://www.formula1.com/en/teams/{}.html" #De todos los equipos

def extraccion(informacion,url,info):

    #Creacion de la carpeta con el nombre de información
    carpeta = os.path.join(os.getcwd(), informacion)
    os.makedirs(carpeta, exist_ok=True)

    for f in info:
        url_f = url.format(f)
        data = requests.get(url_f)

        # Creación de la ruta de archivo 
        file_path = os.path.join(carpeta, f"{f}.html")

        # Guarda el archivo en la carpeta creada
        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(data.text)
            print(f"Escribió {informacion} : {f}")

def lectura_teams(informacion, years, tipo, clase):

    dfs = []

    #Carpeta donde se encuentran los archivos
    carpeta = os.path.join(os.getcwd(), informacion)

    for year in years:

        file_path = os.path.join(carpeta, f"{year}.html")

        with open(file_path.format(year), "r", encoding="utf-8") as f:
            page = f.read()
            print(f"Leyo {informacion}: {year}")

        soup = BeautifulSoup(page, 'html.parser')
        #soup.find(tipo, class_=clase).decompose()
        teams_table = soup.find_all(tipo, class_=clase)

        if teams_table:
            for t in teams_table:
                team = t.get_text(strip=True)  # Obtener texto limpio
                dfs.append({"Equipo": team})
        else:
            print(f"No se encontró información en {file_path}")

    df = pd.DataFrame(dfs)
    df.to_csv(f"{informacion}.csv", index=False)
    print(f"Datos guardados en {informacion}.csv")

    columnas = list(df.columns)
    

    teams = df.values.tolist()
    
    teams.insert(0, columnas)
    teams = [fila[0] if len(fila) == 1 else fila for fila in teams]

    return teams


def lectura(informacion, years, tipo, clase):

    dfs = []

    #Carpeta donde se encuentran los archivos
    carpeta = os.path.join(os.getcwd(), informacion)

    for year in years:

        file_path = os.path.join(carpeta, f"{year}.html")

        with open(file_path.format(year), "r", encoding="utf-8") as f:
            page = f.read()
            print(f"Leyo {informacion}: {year}")

        soup = BeautifulSoup(page, 'html.parser')
        #soup.find(tipo, class_=clase).decompose()
        pilot_table = soup.find_all(tipo, class_=clase)

        if pilot_table:
            for p in pilot_table:
                piloto = p.get_text(strip=True)  # Obtener texto limpio
                dfs.append({"Equipo": year, "Piloto": piloto})
        else:
            print(f"No se encontró información en {file_path}")

    df = pd.DataFrame(dfs)
    df.to_csv(f"{informacion}.csv", index=False)
    print(f"Datos guardados en {informacion}.csv")



##############
extraccion("team",url_equipos,equipos)
clase_teams='f1-heading tracking-normal text-fs-20px tablet:text-fs-25px leading-tight normal-case font-bold non-italic f1-heading__body font-formulaOne'
teams= lectura_teams("team",equipos,'span',clase_teams)
clase='f1-heading tracking-normal text-fs-18px leading-tight normal-case font-normal non-italic f1-heading__body font-formulaOne mt-xs'
extraccion("pilotos",url_team,teams)
lectura("pilotos", teams,'p',clase)
x_path='/html/body/main/div/div/div/div[1]/div[2]/figure[2]/a/figcaption/div/p[1]'

#lectura("aws", years,'tr',"over_header")
#extraccion("player",player_stats_url,years)
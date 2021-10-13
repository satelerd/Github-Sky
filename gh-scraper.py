"""
Lo siguiente es el codigo para un proyecto que se llama Github Sky, en el cual dado un usuario de github, hace un scrape con bs4 para sacar los datos de contribucion (o usar una api si existe) y desp generar una foto del cielo con estrellas representando el patron de contribuciones del usuario. 
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt


def get_user_contributions(user):
    """
    Funcion que dado un usuario de github, devuelve la cantidad de contribuciones que ha hecho.
    """

    url = f"https://github.com/{user}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Busca todas los tags llamadss 'rect'
    contributions = soup.find_all("rect")
    # print(contributions)

    dates = []
    data_count = []
    data_level = []
    for i in range(len(contributions)):
        # Se elimina los que no sirven
        if "data-count" not in contributions[i].attrs:
            continue
        else:
            # Se agrega los datos al dictionario segun su fecha
            dates.append(contributions[i]["data-date"])
            data_count.append(contributions[i]["data-count"])
            data_level.append(contributions[i]["data-level"])

    return dates, data_count, data_level


# Crea una funcion que dado los datos de contribuciones genera un grafico que los muestra.
def generate_plot(dates, data):
    """
    Funcion que dado un diccionario de contribuciones, genera un grafico con ellas.
    """

    plt.figure(figsize=(10, 5))
    plt.scatter(dates, data)
    plt.show()


dates, data_count, data_level = get_user_contributions("satelerd")
print(dates)
print(data_count)
print(data_level)
generate_plot(dates, data_level)

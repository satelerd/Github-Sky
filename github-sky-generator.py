"""
Lo siguiente es el codigo para un proyecto que se llama Github Sky, en el cual dado un usuario de github, hace un scrape con bs4 para sacar los datos de contribucion (o usar una api si existe) y desp generar una foto del cielo con estrellas representando el patron de contribuciones del usuario. 
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import random
import matplotlib.pyplot as plt

# SCRAPER
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


# GRAPH GENERATOR
def star_generator(data):
    # Se crea una matriz de ceros de tamaño len(data_level)/7 x 7
    data_matrix = np.zeros((int(len(data) / 7), 7))
    data_matrix = data_matrix.T

    # data_matrix[0, 0] = 5
    # data_matrix[2, 2] = 5
    # data_matrix[2, 5] = 5
    # print(data_matrix)

    # Se llena la matriz con los datos de data_count
    for i in range(len(data)):
        try:
            data_matrix[int(i / 7), i % 7] = data[i]

        except:  # NO SE LLENA LA MATRIZ COMPLETA, OJO!!!!!
            break

    # Generamos la matriz principal que sera graficada   (matriz y desp pasarlo a lista para graficarlo mejor... en volaa)
    stars = []
    weeks = 52
    days = 7
    rows_day = 50
    cols_day = 50
    for week in range(weeks):
        for day in range(days):

            # aca definimos el valor de cuantas estrellas generar en ese dia, y las agregamos a una lista en orden random
            level = int(data[day + days * week])
            stars_cuantity = rows_day * cols_day / 6 * (level + 1)
            day_stars = []
            for i in range(rows_day * cols_day):
                if i <= stars_cuantity:
                    day_stars.append(1)
                else:
                    day_stars.append(0)
            random.shuffle(day_stars)

            day_matrix = []
            for row in range(rows_day):
                row_matrix = []

                for col in range(cols_day):
                    # aqui vamos agregando un valor binario si hay o no estrella
                    row_matrix.append(day_stars[row * cols_day + col])

                day_matrix.append(row_matrix)

            stars.append(day_matrix)

    return stars


def grafica(star_matrix):
    star_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    cont = 0
    while True:

        cont += 1
    print(star_matrix)


def generate_plot(dates, data):
    """
    Funcion que dado un diccionario de contribuciones, genera un grafico con ellas.
    """

    # Se crea una matriz de ceros de tamaño len(data_level)/7 x 7
    data_matrix = np.zeros((int(len(data_level) / 7), 7))
    # Se llena la matriz con los datos de data_count
    for i in range(len(data_level)):
        try:
            data_matrix[int(i / 7), i % 7] = data_level[i]

        except:  # NO SE LLENA LA MATRIZ COMPLETA, OJO!!!!!
            break

    # Se crea una figura y una subfigura
    fig, ax = plt.subplots()
    # Se grafica la matriz
    ax.imshow(data_matrix)
    ax.set_title("Contribuciones")
    ax.set_xlabel("Dias")
    ax.set_ylabel("Semana")
    # Se agrega el label a cada celda
    for i in range(len(data)):
        ax.text(i % 7, int(i / 7), data[i], ha="center", va="center", color="w")
    plt.show()


# FUNCTION CALL
dates, data_count, data_level = get_user_contributions("satelerd")
stars_matrix = star_generator(data_level)
print(stars_matrix)
# grafica(stars_list)

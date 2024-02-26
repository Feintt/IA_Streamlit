.. Street Map documentation master file, created by
   sphinx-quickstart on Mon May 24 22:37:07 2024.


Welcome to Street Map's documentation!
======================================

Universidad Panamericana - Inteligencia Artificial

AUTORES
------------
- **Bruno Galli Hambleton**
- **Mauricio Fernando Chavarría Reyes**
- **Sofía Husny Tuachi**

Introduction
------------

Street Map Pathfinding

Este programa permite al usuario seleccionar un lugar
y un par de nodos para encontrar la ruta entre ellos, utilizando
algoritmos de búsqueda y graficando los resultados.

Este proyecto utiliza como base la librería OSMnx para obtener
los datos de la red de calles de OpenStreetMap, y Streamlit para
la interfaz de usuario.

Cabe mencionar que OSMnx es una libreria que utiliza OpenStreetMap
para obtener datos de redes de calles, por lo que puede que no
tenga información de todas las calles del mundo.

Para ejecutar este programa, es necesario tener instaladas las
librerías OSMnx, Streamlit, pandas, entre otras. Se recomienda
utilizar un entorno virtual para instalar las dependencias.

Para instalar las dependencias, se puede utilizar el siguiente comando:

    pip install -r requirements.txt

Para ejecutar el programa, se puede utilizar el siguiente comando:

        streamlit run main.py

Una vez que el programa esté corriendo, se puede acceder a la interfaz

    http://localhost:8501

y se podrá seleccionar el lugar y los nodos para encontrar la ruta.

Estrictamente, se recomienda utilizar docket para correr el programa
debido a que se utilizan una gran cantidad de librerías y dependencias
que pueden ocasionar problemas al correr el programa.

Igualmente, se requiere del plugin Compose de Docker para correr el
programa con docker, se recomienda instalar docker desktop para
obtener el plugin Compose.
Busque en la documentación oficial de Docker para más información
sobre cómo instalar Docker Desktop y el plugin Compose.

Url de la documentación oficial de Docker:
https://docs.docker.com/desktop/

Para correr el programa con docker, se puede utilizar el siguiente comando:

    docker compose up --build

Una vez que el programa esté corriendo, se puede acceder a la interfaz

        http://localhost:8501

y se podrá seleccionar el lugar y los nodos para encontrar la ruta.

Para detener el programa, se puede utilizar el siguiente comando:

    docker compose down

Para más información sobre el uso de Streamlit, se puede consultar la
documentación oficial en https://docs.streamlit.io/en/stable/

Para más información sobre el uso de OSMnx, se puede consultar la
documentación oficial en https://osmnx.readthedocs.io/en/stable/

Para más información sobre el uso de pandas, se puede consultar la
documentación oficial en https://pandas.pydata.org/docs/

Para más información sobre el uso de OpenStreetMap, se puede consultar
la página oficial en https://www.openstreetmap.org/


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   main
   helpers
   helpers.algorithms


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

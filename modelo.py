#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Autor: Emilio García Gutiérrez
# Modelo del programa
# Importación de librerías
import subprocess
import sqlite3
import json
import os

# Clase Model que contiene las funciones necesarias para realizar las operaciones relacionadas con la base de datos y la manipulación de los datos
class Model:

    # Método constructor
    def __init__(self):
        pass
    
    # Función que inicializa la base de datos
    def databaseInit(self):
        # Conexión con la base de datos (si no existe, la crea)
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Creación de la tabla Project
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Project(
                id_project INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                path TEXT UNIQUE,
                n_analysis INTEGER DEFAULT 0,
                date TIMESTAMP DEFAULT (datetime('now', 'localtime'))
            )
        '''
        )
        # Creación de la tabla Analysis y sus relaciones con la tabla Project
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Analysis(
                id_analysis INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                dir_file TEXT,
                n_vulns INTEGER,
                date TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                file JSON,
                FOREIGN KEY (project_id) REFERENCES Project(id_project) ON DELETE CASCADE
            )
        '''
        )
        # Creación de la tabla Vulnerability y sus relaciones con la tabla Analysis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Vulnerability(
                id_vuln INTEGER PRIMARY KEY AUTOINCREMENT,
                id_osv TEXT,
                analysis_id INTEGER,
                package TEXT,
                ecosystem TEXT,
                summary TEXT,
                details TEXT,
                affected_range TEXT,
                introduced_version TEXT,
                fixed_version TEXT,
                FOREIGN KEY (analysis_id) REFERENCES analysis(id_analysis) ON DELETE CASCADE
            )
        '''
        )

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

    ''' %%%%%%%%%%%%%% DATOS DE LOS PROYECTOS %%%%%%%%%%%%%% '''
    # Función que devuelve los datos de todos los proyectos existentes en la base de datos
    def returnAllProjects(self):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Selección de todos los datos de la tabla Project
        cursor.execute("SELECT * FROM Project")
        rows=cursor.fetchall()

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Devolver los datos obtenidos
        return rows
    
    # Función que devuelve los datos de un proyecto dado por su id
    def returnProject(self, project_id):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Selección de todos los datos de la tabla Project de un proyecto con el id dado
        cursor.execute("SELECT * FROM Project WHERE id_project=?", (project_id,))
        row=cursor.fetchone()

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Devolver los datos obtenidos
        return row
    
    # Función para crear un nuevo proyecto dados su título, descripción y ruta
    def createProject(self, title, description, path):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Inserción de los datos en la tabla Project creando un nuevo proyecto
        cursor.execute("INSERT INTO Project (title, description, path) VALUES (?, ?, ?)", (title, description, path))

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()
    
    # Función para eliminar un proyecto dado su id
    def deleteProject(self, project_id):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Activar las claves foráneas para que se eliminen los datos relacionados (análisis y vulnerabilidades)
        cursor.execute("PRAGMA foreign_keys = ON")

        # Borrado de los datos en la tabla Project de un proyecto con el id dado
        cursor.execute("DELETE FROM Project WHERE id_project=?", (project_id,))

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()
    
    # Función para comprobar la existencia de un proyecto dado su ruta
    def projectExists(self, project):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Buscar un proyecto con la misma ruta en la tabla Project
        cursor.execute("SELECT * FROM Project WHERE path=?", (project,))
        row=cursor.fetchone()
        # Si existe, devolver su id
        if row:
            project_id=row[0]
        # Si no existe, devolver un string vacío
        else:
            project_id=""

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Devolver el valor obtenido
        return project_id
        
    ''' %%%%%%%%%%%%%% DATOS DE LOS ANÁLISIS %%%%%%%%%%%%%% '''
    # Función que devuelve los datos de todos los análisis realizados en un proyecto dado su id
    def returnAllAnalysis(self, project_id):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()
        
        # Selección de todos los análisis de un proyecto en la tabla Analysis dado su id de proyecto
        cursor.execute("SELECT id_analysis, dir_file, n_vulns, date FROM Analysis WHERE project_id=?", (project_id,))
        rows=cursor.fetchall()
        
        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Devolver los datos obtenidos
        return rows
    
    # Función para crear un nuevo análisis dados su id de proyecto, ruta, número de vulnerabilidades y datos en formato JSON
    def createAnalysis(self, project_id, path, vulns, json):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()
        
        # Inserción de los datos en la tabla Analysis creando un nuevo análisis
        cursor.execute("INSERT INTO Analysis (project_id, dir_file, n_vulns, file) VALUES (?, ?, ?, ?)", (project_id, path, vulns, json))

        # Guardamos el id del análisis creado
        analysis_id=cursor.lastrowid

        # Aumentamos el número de análisis realizados en el proyecto en la tabla Project
        cursor.execute("UPDATE Project SET n_analysis=n_analysis+1 WHERE id_project=?", (project_id,))

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Devolver el id del análisis
        return analysis_id
    
    # Función para eliminar un análisis dado su id
    def deleteAnalysis(self, analysis_id):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Activar las claves foráneas para que se eliminen los datos relacionados (vulnerabilidades)
        cursor.execute("PRAGMA foreign_keys = ON")

        # Decrementamos el número de análisis realizados en el proyecto en la tabla Project
        cursor.execute("UPDATE Project SET n_analysis=n_analysis-1 WHERE id_project=(SELECT project_id FROM Analysis WHERE id_analysis=?)", (analysis_id,))

        # Borrado del análisis con el id dado en la tabla Análisis 
        cursor.execute("DELETE FROM Analysis WHERE id_analysis=?", (analysis_id,))

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()
        
    # Función para el guardado de los datos de un análisis en formato JSON e guardar las vulnerabilidades detectadas en el análisis en la base de datos
    def saveVulns(self, command, project_id, path):
        # Comprobar si el path es un directorio o un fichero
        # Si es un directorio, se guardará el nombre del directorio como nombre del fichero JSON
        if os.path.isdir(path):
            dirname=os.path.basename(path)
            route=dirname+'.json'

        # Si es un fichero, se guardará el nombre del directorio y el nombre del fichero como nombre del fichero JSON para referenciar mejor el análisis
        else:
            dirname=os.path.basename(os.path.dirname(path))
            filename=os.path.basename(path)
            route=dirname+'~'+filename+'.json'

        # Ejecutar el comando para realizar el análisis y obtener la salida
        process=subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Obtener la salida y el error(además de filtrar la información que no nos interesa)
        output, error=process.communicate()
        
        # Decodificar la salida
        output=output.decode("utf-8")

        # Intentar cargar la salida como objeto JSON
        try:
            json_data=json.loads(output)
        except json.JSONDecodeError:
            return

        # Verificar si el resultado no es nulo
        if json_data.get("results") is None:
            # Crear el análisis con 0 vulnerabilidades
            self.createAnalysis(project_id, route, 0, "")
            return
        
        # Filtrar los resultados que no nos interesan
        else:
            # Filtramos los resultados
            results=json_data["results"]

            # Obtenemos el número total de vulnerabilidades
            total_vulnerabilities=sum(len(package.get("vulnerabilities", [])) for result in results for package in result["packages"])
            
            # Creamos el análisis y obtenemos su id
            a_id=self.createAnalysis(project_id, route, total_vulnerabilities, output)
            
            # Recorremos los resultados
            for result in results:
                # Obtenemos los paquetes
                packages=result["packages"]

                # Recorremos los paquetes
                for package in packages:

                    # Obtenemos la información del paquete
                    package_info=package["package"]

                    # Obtenemos las vulnerabilidades
                    vulnerabilities_list=package.get("vulnerabilities", [])

                    # Recorremos las vulnerabilidades
                    for vuln in vulnerabilities_list:
                        # Guardamos el id de la vulnerabilidad
                        vuln_id=vuln["id"]

                        # Guardamos el nombre del paquete
                        package_name=package_info["name"]

                        # Guardamos el ecosistema del paquete
                        ecosystem=package_info["ecosystem"]

                        # Guardamos el resumen de la vulnerabilidad
                        summary=vuln["summary"]

                        # Guardamos los detalles de la vulnerabilidad
                        details=vuln["details"]

                        # Guardamos el rango de versiones afectadas
                        affected_ranges=vuln["affected"][0]["ranges"]

                        # Guardamos la versión introducida
                        introduced_version=affected_ranges[0]["events"][0]["introduced"]

                        # Guardamos el rango de versiones para saber si existe la información que buscamos
                        events=affected_ranges[0]["events"]

                        # Por defecto, la versión arreglada es N/A
                        fixed_version="N/A"

                        # Si hay más de un evento, indican si está arreglado o no
                        if len(events)>1:
                            last_affected=None
                            # Guardamos la versión arreglada dependiendo de si está arreglado o no, buscando el evento que lo indica
                            for event in events:
                                if "fixed" in event:
                                    fixed_version=event["fixed"]
                                if "last_affected" in event:
                                    last_affected=event["last_affected"]
        
                            # Si tiene la última versión afectada, guardarlo como la última versión afectada
                            if last_affected:
                                affected_range=f"{introduced_version}-{last_affected}"

                            # Si no, guardarlo como la versión actual
                            else:
                                affected_range=f"{introduced_version}-Before Actual Version"
                        # Si solo hay un evento, significa que no está arreglado y que no lo indica
                        else:
                            # Si la versión introducida es la última versión, significa que no está arreglado y que no tiene rango de versiones afectadas
                            introduced_version=introduced_version[:-2]
                            affected_range=introduced_version

                        # Creación de una vulnerabilidad
                        self.createVulnerability(a_id, vuln_id, package_name, ecosystem, summary, details, affected_range, introduced_version, fixed_version)

    # Descarga de un fichero JSON con los datos de un análisis            
    def saveJSON(self, analysis_id):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Seleccionar la ruta y los datos json de la tabla Analysis con el id del análisis indicado
        cursor.execute("SELECT dir_file, file FROM Analysis WHERE id_analysis=?", (analysis_id,))
        data_json=cursor.fetchone()

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Cargar el JSON y volcarlo en un archivo
        if data_json[1]:
            datos=json.loads(data_json[1])
        else:
            datos=""
        # Nombre del fichero JSON por la ruta obtenida y volcado de datos
        with open(data_json[0], 'w') as outfile:
            json.dump(datos, outfile, indent=4)        

    ''' %%%%%%%%%%%%%% FUNCIONES DE LAS VULNERABILIDADES %%%%%%%%%%%%%% '''  
    # Función que devuelve los datos de las vulnerabilidades detectadas en un análisis
    def returnVulnerabilities(self, analysis_id):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Devolver los datos de las vulnerabilidades de la tabla Vulnerability con el id del análisis indicado
        cursor.execute("SELECT id_osv, package, ecosystem, summary, details, affected_range, introduced_version, fixed_version FROM Vulnerability WHERE analysis_id=?", (analysis_id,))
        rows=cursor.fetchall()
        
        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Devolver los datos obtenidos
        return rows

    # Función que guarda los datos de una vulnerabilidad en la base de datos
    def createVulnerability(self, analysis_id, id_osv, package, ecosystem, summary, details, affected_range, introduced_version, fixed_version):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Inserción de los datos en la tabla Vulnerability para crear una vulnerabilidad
        cursor.execute("INSERT INTO Vulnerability (id_osv, analysis_id, package, ecosystem, summary, details, affected_range, introduced_version, fixed_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (id_osv, analysis_id, package, ecosystem, summary, details, affected_range, introduced_version, fixed_version))
  
        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()
    
    # Función que realiza una comparación entre dos análisis, devolviendo las vulnerabilidades que se han mantenido, corregido o añadido
    def analysisComparison(self, analysis_id_1, analysis_id_2):
        # Conexión con la base de datos 
        connection=sqlite3.connect("DependencyEval.db")

        # Creación de un cursor para realizar operaciones en la base de datos
        cursor=connection.cursor()

        # Guardar los ids de las vulnerabilidades dados por OSV del primer análisis
        cursor.execute("SELECT id_osv FROM Vulnerability WHERE analysis_id=?", (analysis_id_1,))
        vulns_1=cursor.fetchall()

        # Guardar los ids de las vulnerabilidades dados por OSV del segundo análisis
        cursor.execute("SELECT id_osv FROM Vulnerability WHERE analysis_id=?", (analysis_id_2,))
        vulns_2=cursor.fetchall()

        # Guardar los cambios y cerrar la conexión
        connection.commit()
        connection.close()

        # Crear un conjunto de los ids de las vulnerabilidades del primer análisis
        analysis_1=set(row[0] for row in vulns_1)

        # Crear un conjunto de los ids de las vulnerabilidades del segundo análisis
        analysis_2=set(row[0] for row in vulns_2)

        # Obtener los elementos comunes entre los conjuntos analysis_1 y analysis_2 (vulnerabilidades que se han mantenido)
        common=analysis_1 & analysis_2 if analysis_1 & analysis_2 else ""

        # Encontrar los valores que están en analysis_2 pero no en analysis_1 (vulnerabilidades nuevas)
        new=analysis_2-analysis_1 if analysis_2-analysis_1 else ""

        # Encontrar los valores que están en analysis_1 pero no en analysis_2 (vulnerabilidades corregidas)
        corrected=analysis_1-analysis_2 if analysis_1-analysis_2 else ""


        # Guardamos los datos en una lista
        results=[
            len(new) if len(new)<25 else "25 o más", # Número de vulnerabilidades nuevas, si hay más de 25, se muestra "25 o más"
            new, # ID de las vulnerabilidades nuevas
            len(corrected) if len(corrected)<25 else "25 o más", # Número de vulnerabilidades corregidas, si hay más de 25, se muestra "25 o más"
            corrected, # ID de las vulnerabilidades corregidas
            len(common) if len(common)<25 else "25 o más", # Número de vulnerabilidades que se han mantenido, si hay más de 25, se muestra "25 o más"
            common # ID de las vulnerabilidades que se han mantenido
        ]
        
        # Pasamos los datos a string y eliminamos los caracteres innecesarios
        for i in range(1, len(results), 2):
            text=str(results[i])[1:-1]
            results[i]=text.replace("'", "")

        # Devolvemos los resultados
        return results
    




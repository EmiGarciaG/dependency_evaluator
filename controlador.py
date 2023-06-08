#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Autor: Emilio García Gutiérrez
# Controlador del programa
# Importación de librerías
import tkinter as tk
from tkinter import ttk
from modelo import Model
from vista import View

# Clase Controller que controla el programa
class Controller:

    # Método constructor
    def __init__(self):
        self.modelo=Model()
        # Pasar el controlador a la vista para que pueda acceder a sus funciones
        self.vista=View(self)

    # Main, inicializar la base de datos y muestra la vista
    def main(self):
        self.modelo.databaseInit()
        self.vista.main()

    ''' %%%%%%%%%%%%%% FUNCIONES DE LOS PROYECTOS %%%%%%%%%%%%%% '''
    # Función para comprobar si existe un proyecto dada su ruta (única para cada proyecto)
    def chckProject(self, project):
        # Comprobar si existe el proyecto
        id_project=self.modelo.projectExists(project.get())

        # Si existe, mostrar el listado de análisis realizados en ese proyecto
        if id_project:
            # Limpiar los widgets de la vista
            self.vista.clearWidgets()

            # Asignar el id del proyecto a la variable de control
            self.vista.var_project_id.set(id_project)

            # Mostar el listado de análisis del proyecto seleccionado
            self.vista.analysisTable(id_project, project.get())

        # Si no existe, mostrar el formulario para crear un nuevo proyecto con su ruta
        else:
            self.vista.createProject(project)
            self.vista.errorMessage(3)

    # Función para crear un nuevo proyecto si se ha rellenado el formulario correctamente
    def addProject(self, title, description, path, table, window):
        # Comprobar que los campos no están vacíos
        if title=="" or description=="" or path=="Proyecto No Seleccionado":
            self.vista.errorMessage(0)
            return
        
        # Comprobar que no existe un proyecto con la misma ruta
        if self.modelo.projectExists(path):
            self.vista.errorMessage(1)
            return
        
        # Si todo es correcto, crear el proyecto
        else:
            self.modelo.createProject(title, description, path)
            window.destroy()
            self.listProjects(table)

    # Función para mostrar el listado de proyectos registrados
    def listProjects(self, table):
        # Limpiar la tabla si ya hay datos
        table.delete(*table.get_children())

        # Obtener los datos de la base de datos
        rows=self.modelo.returnAllProjects()

        # Insertar los datos en la tabla
        for data in rows:
            table.insert("", tk.END, values=data)

    # Función para mostrar los datos de un proyecto en su lista de análisis
    def projectData(self, project):
        # Obtener los datos del proyecto
        data=self.modelo.returnProject(project)
        
        # Devolver los datos del proyecto
        return data
    
    # Función para eliminar un proyecto y todos sus análisis
    def removeProject(self, project, table):
        # Llamar a la función del modelo para eliminar el proyecto de la base de datos 
        self.modelo.deleteProject(project)

        # Actualizar el listado de proyectos
        self.listProjects(table)

    ''' %%%%%%%%%%%%%% FUNCIONES DE LOS ANALISIS %%%%%%%%%%%%%% ''' 
    # Guardar el resultado de un análisis en la base de datos
    def addAnalysis(self, command, project, path, table):
        # Añadir al comando la ruta del análisis
        command+=' '+path
        
        # Guardar el resultado del análisis (vulnerabilidades) en la base de datos
        self.modelo.saveVulns(command, project, path)

        # Actualizar el listado de análisis
        self.listAnalysis(table, project)

        # Actualizar los datos del proyecto
        self.vista.projectInfo(project)

    # Función para mostrar el listado de análisis de un proyecto
    def listAnalysis(self, table, project):
        # Limpiar la tabla si ya hay datos
        table.delete(*table.get_children())

        # Obtener los datos de la base de datos
        rows=self.modelo.returnAllAnalysis(project)

        # Insertar los datos en la tabla y asignarles un valor y color de peligrosidad según el número de vulnerabilidades
        for data in rows:
            # Comprobar el número de vulnerabilidades
            num_vulnerabilities=data[2]
            
            # Si no hay vulnerabilidades, la peligrosidad es nula (Blanco)
            if num_vulnerabilities==0:
                danger="Nula"
                color="#92af99"

            # Si hay entre 1 y 5 vulnerabilidades, la peligrosidad es baja (Verde)
            elif num_vulnerabilities<=5:
                danger="Baja"
                color="#06c230"

            # Si hay entre 6 y 10 vulnerabilidades, la peligrosidad es media (Amarillo)
            elif num_vulnerabilities <= 15:
                danger="Media"
                color="#e9b800"

            # Si hay más de 15 vulnerabilidades, la peligrosidad es alta (Rojo)
            else:
                danger="Alta"
                color="#e71500"
            
            # Listado de datos y añadir la peligrosidad
            datap=list(data)
            datap.append(danger)

            # Insertar los datos en la tabla
            table.insert("", tk.END, tags=(color,), values=datap)

            # Asignar el color de fondo a la fila según la peligrosidad
            table.tag_configure(color, background=color)

    # Función para eliminar un análisis y sus vulnerabilidades
    def removeAnalysis(self, analysis):
        # Llamar a la función del modelo para eliminar el análisis de la base de datos
        self.modelo.deleteAnalysis(analysis)

    # Función para descargar el resultado de un análisis en formato JSON
    def downloadJSON(self, analysis):
        # Si no se ha seleccionado ningún análisis, no hacer nada
        if analysis==0:
            return
        
        # Si se ha seleccionado un análisis, descargar el resultado en formato JSON
        else:
            self.modelo.saveJSON(analysis)
            
    ''' %%%%%%%%%%%%%% FUNCIONES DE LAS VULNERABILIDADES %%%%%%%%%%%%%% '''
    # Función para mostrar el listado de vulnerabilidades de un análisis
    def listVulnerabilities(self, table, analysis):
        # Limpiar la tabla si ya hay datos
        table.delete(*table.get_children())

        # Obtener los datos de la base de datos
        rows=self.modelo.returnVulnerabilities(analysis)

        # Insertar los datos en la tabla
        for data in rows:
            table.insert("", tk.END, values=data)
            
    # Función para comparar dos análisis
    def compVulnerabilities(self, analysis_1, analysis_2):
        # Obtener los resultados de la comparación
        results=self.modelo.analysisComparison(analysis_1, analysis_2)

        # Devolver los resultados
        return results
    
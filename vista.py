#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Autor: Emilio García Gutiérrez
# Vista del programa
# Importación de librerías
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
import textwrap
import webbrowser
import io
from PIL import Image
#from PIL import ImageTk


MENU="#2c9ea9"
BG="#000c26"
FG="white"
FG2="black"

# Clase View que devuelve la visualización del programa y se inicia la ventana
class View(tk.Tk):

    # Método constructor
    def __init__(self, controlador):
        super().__init__()

        # Llamada al controlador para utilizar sus funciones    
        self.controlador=controlador

        # Listado de widgets utilizados en la vista para su posterior eliminación
        self.widgets_list=[]

        # Establecer el título de la ventana
        self.title("Evaluación de la Seguridad de Dependencias")
        
        # Establecer el icono del programa
        icono=Image.open("img/icon.ico")
        #self.icon=ImageTk.PhotoImage(icono)
        
        # Convertir la imagen en bytes
        with io.BytesIO() as buffer:
            icono.save(buffer, format='PNG')
            img_bytes = buffer.getvalue()

        # Crear un objeto PhotoImage a partir de los bytes
        self.icon = tk.PhotoImage(data=img_bytes)

        self.tk.call('wm', 'iconphoto', self._w, self.icon)
        
        # Establecer el tamaño de la ventana
        self.geometry("1650x750")

        # Establecer el color de fondo de la ventana
        self.configure(background=BG)

        # Centrar la ventana en la pantalla
        self.open_w(self)

        # Llama a la función para crear el menú superior
        self.menu()

        # Imagen de fondo
        self.init=False
        self.home()

        # Configuración de los estilos de los widgets
        self.style=ttk.Style()

        # Estilos personalizados
        # Estilo de los frames
        self.style.configure("Custom.TFrame",
            background=BG
        )
        # Estilo de los botones
        self.style.configure("Custom.TButton",
            background=BG,
            foreground=FG,
            font=("Times New Roman", 12),
        )
        # Estilo de los botones activos
        self.style.map("Custom.TButton",
          background=[("active", MENU)],
          foreground=[("active", FG2)]
        )
        # Estilo de las etiquetas
        self.style.configure("Custom.TLabel",
            background=BG,
            foreground=FG,
            font=("Times New Roman", 12)
        )
        # Estilo de las tablas
        self.style.configure("Treeview", 
            background=BG,
            foreground=FG,
            fieldbackground=BG,
            font=("Times New Roman", 12),
            rowheight=20
        )
        # Estilo de las cabeceras de las tablas
        self.style.configure("Treeview.Heading", 
            background=MENU,
            foreground=FG2,
            font=("Times New Roman", 12)
        )
        # Estilo de selección de la tabla
        self.style.map("Treeview",
            background=[("selected", MENU)],
            foreground=[("selected", FG2)]
        )
        # Estilo de caja de selección
        self.style.configure("Custom.TCombobox", 
            fieldbackground=BG, 
            foreground=FG,
            background="blue",
            selectbackground=MENU,
            selectforeground="black"
        )
        # Estilo de la barra de desplazamiento vertical
        self.style.configure("Vertical.TScrollbar",
            background=BG,
            troughcolor=BG,
            gripcolor=BG,
            gripcount=0
        )

        # Variables para almacenar valores de control-entrada-salida
        self.var_project_id=tk.IntVar(value=0)
        self.var_project_path=tk.StringVar(value="Proyecto No Seleccionado")
        self.var_analysis=tk.IntVar(value=0)
        self.var_sec_analysis=tk.IntVar(value=0)
        self.var_vuln=tk.StringVar()

    # Bucle para mantener la ventana abierta
    def main(self):
        self.mainloop()

    # Menú superior de la ventana
    def menu(self):
        # Creación del menú
        self.menu=tk.Menu(self, background=MENU, font=("Times New Roman", 12))

        # Submenú Archivo
        self.sub_arch=tk.Menu(self.menu, tearoff=0, background=MENU, font=("Times New Roman", 12))
        # Añadir la opción de crear un nuevo proyecto
        self.sub_arch.add_command(label="Nuevo Proyecto", underline=0, command=lambda: self.createProject(self.var_project_path), accelerator="Ctrl+N")
        # Añadir la opción de abrir un proyecto existente
        self.sub_arch.add_command(label="Abrir proyecto", underline=0, command=lambda: self.openProject(self.var_project_path), accelerator="Ctrl+O")
        # Añadir la opción de cerrar un proyecto y volver al listado de proyectos
        self.sub_arch.add_command(label="Cerrar Proyecto", underline=0, command=lambda:  self.projectsTable() if self.init==False else None, accelerator="Ctrl+W")
        self.sub_arch.add_separator()
        # Añadir la opción de salir del programa
        self.sub_arch.add_command(label="Salir", underline=0, command=self.quit, accelerator="Alt+F4")
        self.menu.add_cascade(label="Archivo", menu=self.sub_arch)

        # Submenú Ver
        self.sub_view=tk.Menu(self.menu, tearoff=0, background=MENU, font=("Times New Roman", 12))
        # Añadir la opción de volver a la pantalla de inicio
        self.sub_view.add_command(label="Inicio", underline=0, command=lambda: self.home())
        # Añadir la opción de ver los proyectos registrados
        self.sub_view.add_command(label="Proyectos", underline=0, command=lambda: self.projectsTable())
        self.menu.add_cascade(label="Ver", menu=self.sub_view)
        
        # Submenú Ayuda
        self.sub_help=tk.Menu(self.menu, tearoff=0, background=MENU, font=("Times New Roman", 12))

        # Submenú Enlaces
        self.sub_links=tk.Menu(self.sub_help, tearoff=0, background=MENU, font=("Times New Roman", 12))
        # Añadir el enlace a la página web del proyecto OSV
        self.sub_links.add_command(label="Proyecto OSV", underline=0, command=lambda: webbrowser.open("https://google.github.io/osv-scanner/"))
        # Añadir el enlace a la página web de la base de datos de vulnerabilidades de OSV
        self.sub_links.add_command(label="Base de Datos Vulnerabilidades", underline=0, command=lambda: webbrowser.open("https://osv.dev/list"))
        # Añadir el enlace al repositorio de Github del proyecto OSV
        self.sub_links.add_command(label="Github OSV", underline=0, command=lambda: webbrowser.open("https://github.com/google/osv-scanner"))
        self.sub_help.add_cascade(label="Enlaces", menu=self.sub_links)
        
        # Submenú Acerca de
        self.sub_about=tk.Menu(self.sub_help, tearoff=0, background=MENU, font=("Times New Roman", 12))
        # Añadir la opción de ver la información sobre el proyecto
        self.sub_about.add_command(label="Propiedad Intelectual", underline=0, command=lambda: self.about())
        # Añadir la opción de ver el manual de usuario
        self.sub_about.add_command(label="Manual de Usuario", underline=0, command=lambda: webbrowser.open("https://github.com/EmiGarciaG/tfg_code"))
        self.sub_help.add_cascade(label="Acerca de", menu=self.sub_about)

        self.menu.add_cascade(label="Ayuda", menu=self.sub_help)

        # Funciones más comunes
        self.menu.add_command(label="⟰", command=lambda: self.home()) # Inicio
        self.menu.add_command(label="▤", command=lambda: self.projectsTable()) # Proyectos
        self.menu.add_command(label="➕", command=lambda: self.createProject(self.var_project_path)) # Nuevo Proyecto
        self.menu.add_command(label="❓", command=lambda: self.about()) # Propiedad Intelectual
        
        # Establecer el menú en la ventana
        self.config(menu=self.menu)

        # Atajos de teclado
        self.bind_all("<Control-n>", lambda event: self.createProject(self.var_project_path)) # Nuevo Proyecto (Ctrl+N)
        self.bind_all("<Control-o>", lambda event: self.openProject(self.var_project_path)) # Abrir Proyecto (Ctrl+O)
        self.bind_all("<Control-w>", lambda event: self.projectsTable() if self.init==False else None) # Cerrar Proyecto (Ctrl+W)


    '''%%%%%%%%%%%%%% INICIO %%%%%%%%%%%%%%'''
    # Ventana de inicio
    def home(self):
        # Si no se ha inicializado la ventana o se ha cambiado de ventana
        if not self.init:
            self.clearWidgets()
            # Cargar la imagen de fondo
            self.image=Image.open("img/background.jpg")

            # Convertir la imagen en bytes
            with io.BytesIO() as buffer:
                self.image.save(buffer, format='PNG')
                img_bytes = buffer.getvalue()

            # Crear un objeto PhotoImage a partir de los bytes
            self.scale = tk.PhotoImage(data=img_bytes)

            #self.scale=ImageTk.PhotoImage(self.image)

            # Añadir la imagen de fondo como Label
            self.backg=tk.Label(self, image=self.scale)
            self.backg.pack(fill=tk.BOTH, expand=True)

            # Redimensionar la imagen de fondo al tamaño de la ventana
            self.bind("<Configure>", lambda event: self.resize_img(event, self.image, self.backg))

            # Establecer la ventana como inicializada
            self.init=True
            self.widgets_list.append(self.backg)

    # Redimensionar la imagen de fondo
    def resize_img(self, event, img, backg):
        # Obtener el nuevo ancho y alto de la ventana
        self.new_width=event.width
        self.new_height=event.height

        # Redimensionar la imagen de fondo
        self.nwimg=img.resize((self.new_width, self.new_height))

        # Actualizar la imagen de fondo
        # Convertir la imagen en bytes
        with io.BytesIO() as buffer:
            self.nwimg.save(buffer, format='PNG')
            img_bytes = buffer.getvalue()

        # Crear un objeto PhotoImage a partir de los bytes
        self.nwscale = tk.PhotoImage(data=img_bytes)
        #self.nwscale=ImageTk.PhotoImage(self.nwimg)
        backg.configure(image=self.nwscale)
        backg.image=self.nwscale

    # Ventana de información del proyecto
    def about(self):
        # Ventana secundaria y su configuración
        self.sec_windows=tk.Toplevel(self, background=BG)
        self.sec_windows.title("Acerca de")
        self.sec_windows.geometry("575x225")
        self.open_w(self.sec_windows)

        # Información del trabajo
        self.auxFrame1()
        self.info=ttk.Label(self.aux_f1, 
            text="CopyRight © 2023, Emilio García Gutiérrez \n Este software está licenciado bajo la Licencia Pública General Affero de GNU (AGPL)\n Versión 3.0, 19 Noviembre 2007 \n\nTrabajo dirigido por:\n Juan Antonio Romero del Castillo", 
            style="Custom.TLabel"
        )
        self.info.pack(padx=5, pady=5)

    '''%%%%%%%%%%%%%% FUNCIONES DE LOS PROYECTOS %%%%%%%%%%%%%%'''
    # Representación de los proyectos registrados en la base de datos
    def projectsTable(self):
        # Limpieza de widgets y desactivación de la redimensión
        self.clearWidgets()
        self.unbind("<Configure>")
        self.title("Registro de Proyectos")

        # Frame de la ventana
        self.mainFrame()

        # Título
        self.title_label("Registro de Proyectos", self.main_frame)

        # Frame primario
        self.firstFrame(self.main_frame)
        self.first_frame.pack_forget()
        self.first_frame.pack(fill="x")

        # Tabla de proyectos
        self.projects=self.table_widget(self.first_frame, ("ID", "Título", "Descripción", "Ruta", "Nº Análisis", "Fecha Creación"), "browse")

        # Scrollbar de la tabla
        self.scrollbar_widget(self.first_frame, self.projects)
        self.projects.configure(yscrollcommand=self.scrollbar.set)

        # Volcar los proyectos de la base de datos en la tabla
        self.controlador.listProjects(self.projects)

        # Recoger eventos de la tabla
        self.projects.bind("<<TreeviewSelect>>", self.selectProject) # Selección
        self.bind("<Button-1>", lambda event: self.clearSelection(event, self.projects, None)) # Click izquierdo
        self.projects.bind("<Double-1>", self.viewAnalysis) # Doble click
        self.projects.bind("<Button-3>", lambda event: self.menu_table(event, 1)) # Click derecho
        
        # Frame primario
        self.secondaryFrame(self.main_frame)

        # Crear proyecto
        self.button_widget(self.sec_frame, "Añadir", lambda: self.createProject(self.var_project_path))

        # Eliminar proyecto
        self.button_widget(self.sec_frame, "Eliminar", lambda: self.deleteProject(self.var_project_id.get(), self.projects))

        # Ver análisis
        self.button_widget(self.sec_frame, "Ver Análisis", lambda: self.viewAnalysis(self.var_project_id.get()))

        # Volver al inicio
        self.backButton(0)

    # Evento de selección de un proyecto con doble click
    def viewAnalysis(self, event):
        # Si se ha seleccionado un proyecto válido
        if self.var_project_id.get():
            # Limpieza de widgets
            self.clearWidgets()

            # Cambio a la ventana de análisis
            self.analysisTable(self.var_project_id.get(), self.var_project_path.get())

    # Evento de selección de un proyecto
    def selectProject(self, event):
        # Recoger la selección de la tabla
        item=self.projects.item(self.projects.selection())

        # Comprobar que se ha seleccionado un proyecto y que no está vacío
        if item["values"]!="":
            # Guardar el ID y la ruta del proyecto seleccionado en las variables
            self.var_project_id.set(item["values"][0])
            self.var_project_path.set(item["values"][3])

    # Borrado de un proyecto de la base de datos
    def deleteProject(self, project_id, table):
        self.controlador.removeProject(project_id, table)

    # Ventana secundaria para crear el proyecto
    def createProject(self, var):
        # Ventana secundaria y su configuración
        self.sec_windows=tk.Toplevel(self, background=BG)
        self.sec_windows.title("Nuevo Proyecto")
        self.sec_windows.geometry("800x300")
        self.open_w(self.sec_windows)

        # Introducción de los datos del proyecto
        # Título del proyecto
        self.auxFrame1()
        self.label_widget(self.aux_f1, "Título del Proyecto:")
        self.widgets_list.pop()
        self.title_e=tk.Entry(self.aux_f1, font=("Times New Roman", 12))
        self.title_e.pack(side="left", padx=5, fill="x", expand=True)
        
        
        # Descripción del proyecto
        self.auxFrame2()
        self.label_widget(self.aux_f2, "Descripción:")
        self.widgets_list.pop()
        self.des_e=tk.Entry(self.aux_f2, font=("Times New Roman", 12))
        self.des_e.pack(side="left", padx=5, fill="x", expand=True)

        # Ruta del proyecto
        self.auxFrame3()
        self.label_widget(self.aux_f3, "Ruta del Proyecto:")
        self.widgets_list.pop()
        self.directory=ttk.Label(self.aux_f3, text=var.get(), style="Custom.TLabel")
        self.directory.pack(side="left", padx=5, fill="x", expand=True)
        self.button=ttk.Button(self.aux_f3, text="Seleccionar", command=lambda: self.fileBrowser(self.directory, self.var_project_path), style="Custom.TButton")
        self.button.pack(side="left", padx=5)

        # Botón para confirmar la adición del proyecto
        self.btn_create=ttk.Button(
            self.sec_windows,
            text="Añadir Proyecto",
            command=lambda: 
                (   
                    self.clearWidgets(),
                    self.projectsTable(),
                    self.controlador.addProject(self.title_e.get(), self.des_e.get(), self.directory.cget("text"), self.projects, self.sec_windows),
                ),
            style="Custom.TButton"
        )
        self.btn_create.pack()
                
    ''' %%%%%%%%%%%%%% FUNCIONES DE LOS ANÁLISIS %%%%%%%%%%%%%% '''
    # Tabla de análisis de un proyecto
    def analysisTable(self, project, path):
        # Desactivar los eventos anteriores
        self.unbind("<Configure>")
        self.unbind("<Button-1>")
        self.title("Análisis Realizados")

        # Label para mostrar la información del proyecto
        self.labels=[]

        # Frame de la ventana
        self.mainFrame()

        # Título
        self.title_label("Análisis del Proyecto", self.main_frame)
        
        # Contenedor de la información del proyecto
        self.firstFrame(self.main_frame)
        self.info_part2=ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.info_part2.pack()
        self.widgets_list.append(self.info_part2)
        self.projectInfo(project)

        # Contenedor de la tabla de análisis
        self.secondaryFrame(self.main_frame)
        self.sec_frame.pack_forget()
        self.sec_frame.pack(fill="x")

        # Tabla de análisis
        self.analysis=self.table_widget(self.sec_frame, ("ID", "Archivo", "Nº de Vulnerabilidades", "Fecha", "Peligrosidad"), "extended")

        # Scrollbar de la tabla
        self.scrollbar_widget(self.sec_frame, self.analysis)
        self.analysis.configure(yscrollcommand=self.scrollbar.set)

        # Volcar los análisis de la base de datos en la tabla
        self.controlador.listAnalysis(self.analysis, project)

        # Eventos de la tabla
        self.analysis.bind("<<TreeviewSelect>>", self.selectAnalysis)
        self.bind("<Button-1>", lambda event: self.clearSelection(event, self.analysis, None))
        self.analysis.bind("<Double-1>", self.viewVulnerabilities)
        self.analysis.bind("<Button-3>", lambda event: self.menu_table(event, 2))
        
        # Contenedor del desplegable de los análisis
        self.thirdFrame(self.main_frame)

        # Desplegable para seleccionar el análisis que queremos realizar (por defecto, análisis recursivo)
        opciones=["Análisis Recursivo", "Análisis No Recursivo"]
        self.default= tk.StringVar(value=opciones[0])
        self.election_analysis=ttk.Combobox(self.third_frame, textvariable=self.default, values=opciones, style="Custom.TCombobox")
        self.election_analysis.pack(side="left", padx=5)
        self.election_analysis.bind("<<ComboboxSelected>>", self.analysisTypes)
        self.widgets_list.append(self.election_analysis)

        # Inicializar el desplegable de los análisis con el valor por defecto
        self.analysisTypes(None)

        # Contenedor de los botones
        self.fourthFrame(self.main_frame)

        # Botón para abrir un análisis
        self.button_widget(self.fourth_frame, "Ver Vulnerabilidades", lambda: self.vulnerabilitiesTable(self.var_analysis.get()) if self.var_analysis.get()!=0 else None)
        
        # Botón para eliminar un análisis
        self.button_widget(self.fourth_frame, "Eliminar Análisis", lambda: self.deleteAnalysis(self.var_analysis.get()))

        # Botón para descargar un análisis
        self.button_widget(self.fourth_frame, "Descargar Análisis.json", lambda: self.controlador.downloadJSON(self.var_analysis.get()))

        # Comparar dos análisis
        self.button_widget(self.fourth_frame, "         Comparar Análisis \n(Seleccionar 2 con Ctrl+Click)", lambda: self.comparison(self.var_analysis.get(), self.var_sec_analysis.get()) if self.var_sec_analysis.get()!=0 else None)

        # Volver a la tabla de proyectos
        self.backButton(1)

    # Funcionalidades del desplegable
    def analysisTypes(self, event):
        # Eliminar los widgets del análisis anterior (recursivo)
        if hasattr(self, "button_r"):
            self.button_r.destroy()
            
        # Eliminar los widgets del análisis anterior (no recursivo)
        if hasattr(self, "button_f"):
            self.p_label.destroy()
            self.button_f.destroy()
            self.button_nr.destroy()

        # Mostrar los botones para el análisis recursivo si se ha seleccionado
        if self.election_analysis.get()=="Análisis Recursivo":
            self.button_r=self.button_widget(self.third_frame, "Realizar Análisis Recursivo", lambda: self.controlador.addAnalysis('./osv-scanner -r --format json', self.var_project_id.get(), self.var_project_path.get(), self.analysis))

        # Mostrar los botones para el análisis no recursivo si se ha seleccionado
        elif self.election_analysis.get()=="Análisis No Recursivo":
            self.p_label=self.label_widget(self.third_frame, "Seleccione un archivo")
            self.p_label.config(font=("Times New Roman", 12))
            self.button_f=self.button_widget(self.third_frame, "Elegir un fichero", lambda: self.lockfileBrowser(self.p_label))
            self.button_nr=self.button_widget(self.third_frame, "Realizar Análisis No Recursivo", lambda: self.controlador.addAnalysis('./osv-scanner --format json', self.var_project_id.get(), self.p_label.cget("text"), self.analysis) if self.p_label.cget("text")!="Seleccione un archivo" else None)

    # Evento de doble click sobre un análisis para mostrar sus vulnerabilidades
    def viewVulnerabilities(self, event):
        # Recoger la selección de la tabla
        item=self.analysis.item(self.analysis.selection())

        # Comprobar si se ha seleccionado un análisis válido
        if item["values"]!="":
            # Mostrar las vulnerabilidades del análisis
            self.vulnerabilitiesTable(item["values"][0])

    # Recoger el evento de click derecho en un análisis para eliminarlo
    def deleteAnalysis(self, analysis_id):
        # Eliminar el análisis de la base de datos
        self.controlador.removeAnalysis(analysis_id)

        # Limpiar los widgets
        self.clearWidgets()

        # Actualizar la tabla de análisis
        self.analysisTable(self.var_project_id.get(), self.var_project_path.get())

    # Información del proyecto
    def projectInfo(self, project):
        # Obtener los datos del proyecto que se ha abierto
        atr=self.controlador.projectData(project)
        data=[
            "ID del Proyecto: "+str(atr[0]), 
            "Título del Proyecto: "+str(atr[1]),
            "Descripción del Proyecto: "+str(atr[2]),
            "Ruta del Proyecto: "+str(atr[3]), 
            "Nº Análisis Realizados: "+str(atr[4]),
            "Fecha Creación Proyecto: "+str(atr[5])
        ]

        # Recorrer los datos y mostrarlos en la ventana
        for i in range(len(data)):
            # Si el widget ya existe, actualizarlo
            if i<len(self.labels):
                self.labels[i].config(text=data[i])
            else:
                if i<3:
                    atribute=ttk.Label(self.first_frame, text=data[i], style="Custom.TLabel")
                    atribute.pack(side="left", padx=(5, 10), pady=5)
                    self.labels.append(atribute)
                    self.widgets_list.append(atribute)
                else:
                    atribute=ttk.Label(self.info_part2, text=data[i], style="Custom.TLabel")
                    atribute.pack(side="left", padx=(5, 10), pady=5)
                    self.labels.append(atribute)
                    self.widgets_list.append(atribute)
        
    # Evento de selección múltiple en la tabla de análisis
    def selectAnalysis(self, event):
        selected_items=self.analysis.selection()
        # Comprobar si existe una selección
        if selected_items:
            # Obtener el análisis seleccionado
            item=self.analysis.item(selected_items[0])

            # Comprobar si se ha seleccionado un análisis válido
            if item["values"]!="":
                # Guardar la primera selección
                item=self.analysis.item(self.analysis.selection()[0])

                # Si hay más de dos selecciones, evitar que se puedan seleccionar más
                if len(self.analysis.selection())>2:
                    for i in self.analysis.selection()[2:]:
                        self.analysis.selection_remove(i)

                # Si hay dos selecciones, guardar la segunda
                if len(self.analysis.selection())>1:
                    # Comprobar si la primera selección es la misma que la segunda
                    if self.var_analysis.get()==self.analysis.item(self.analysis.selection()[0])["values"][0]:
                        item2=self.analysis.item(self.analysis.selection()[1])
                        self.var_sec_analysis.set(item2["values"][0])

                    # Si no, guardar la primera
                    else:
                        item2=self.analysis.item(self.analysis.selection()[0])
                        self.var_sec_analysis.set(item2["values"][0])

                # Si solo hay una selección, guardarla
                else:
                    self.var_analysis.set(item["values"][0])

    # Explorador de archivos y seleccionar ficheros específicos
    def lockfileBrowser(self, label):
        # Tipos de archivo específicos
        types=[
            ("AndroidCompilationScript (Gradle)", "buildscript-gradle.lockfile"), 
            ("C++ (Conan)", "conan.lock"),
            ("Dart (Pub)", "pubspec.lock"),
            ("Elixir (Mix)", "mix.lock"),
            ("Go", "go.mod"),
            ("Java (Apache Maven)", "pom.xml"),
            ("Java|Android|Kotlin|Groovy (Gradle)", "gradle.lockfile"),
            ("JavaScript (npm|Yarn)", ["pnpm-lock.yaml", "yarn.lock"]),
            ("Node.js (npm)", ["package-lock.json", "packages.lock.json"]),
            ("PHP (Composer)", "composer.lock"),
            ("Python (Pip|Pipenv|Poetry)", ["requirements.txt", "Pipfile.lock", "poetry.lock"]),
            ("Ruby (RubyGems)", "Gemfile.lock"),
            ("Rust (Cargo)", "Cargo.lock")
        ]

        # Crear una opción para todos los archivos
        locks=[[ext] if isinstance(ext, str) else ext for _, ext in types]
        files=[item for sublist in locks for item in sublist]
        all_types=[("Todos los archivos", files)]
        filetypes=all_types+types

        while True:
            # Abrir el explorador de archivos
            file_route=tk.filedialog.askopenfilename(filetypes=filetypes, initialdir=self.var_project_path.get(), parent=self)
            
            # Si se selecciona un archivo específico, este debe estar en la ruta del proyecto
            if self.var_project_path.get()+"/" in file_route:
                label.config(text=file_route)
                break
            # Si no, mostrar un mensaje de error
            elif not file_route:
                break
            else:
                self.errorMessage(2)
                pass

    ''' %%%%%%%%%%%%%% FUNCIONES DE LAS VULNERABILIDADES %%%%%%%%%%%%%% '''
    # Tabla de vulnerabilidades de un análisis
    def vulnerabilitiesTable(self, analysis):
        # Limpiar los widgets existentes y desactivar el evento de click
        self.clearWidgets()
        self.unbind("<Button-1>")
        self.title("Vulnerabilidades del Análisis")

        # Frame de la ventana
        self.mainFrame()

        # Título
        self.title_label("Vulnerabilidades Halladas", self.main_frame)

        # Contenedor de la tabla de vulnerabilidades
        self.firstFrame(self.main_frame)
        self.first_frame.pack_forget()
        self.first_frame.pack(fill="x")

        self.vulnerabilities=self.table_widget(self.first_frame, ("ID", "Paquete", "Ecosistema", "Resumen", "Detalles", "Rango afectado", "Versión introducida", "Versión corregida"), "browse")

        # Scrollbar de la tabla
        self.scrollbar_widget(self.first_frame, self.vulnerabilities)
        self.vulnerabilities.configure(yscrollcommand=self.scrollbar.set)

        # Volcar las vulnerabilidades de la base de datos en la tabla
        self.controlador.listVulnerabilities(self.vulnerabilities, analysis)

        # Recoger eventos de la tabla
        self.currentPos=None
        self.tooltip=None
        self.vulnerabilities.bind("<Motion>", lambda event: self.show_tooltip(event, self.vulnerabilities))
        self.vulnerabilities.bind("<<TreeviewSelect>>", lambda event: self.selectVulnerability(event, self.vulnerabilities))
        self.bind("<Button-1>", lambda event: self.clearSelection(event, self.vulnerabilities, None))
        self.vulnerabilities.bind("<Double-1>", lambda event: self.browserVulnerability(event, self.vulnerabilities))
        

        # Volver a la tabla de análisis
        self.open_vuln=ttk.Button(self.main_frame, text="Ver en OSV Vulnerability Database", command=lambda: webbrowser.open("https://osv.dev/vulnerability/"+self.var_vuln.get()) if self.var_vuln.get()!="" else None, style="Custom.TButton")
        self.open_vuln.pack(pady=(20, 10))
        self.widgets_list.append(self.open_vuln)
        
        self.backButton(2)

    # Evento de hover sobre una vulnerabilidad para mostrar sus detalles
    def show_tooltip(self, event, table):
        # Identificar la posición del cursor
        row=table.identify_row(event.y)
        col=table.identify_column(event.x)

        # Asignar la actual posición del cursor
        pos=(row, col)

        # Destruir el tooltip si se cambia de posición
        if pos!=self.currentPos and self.tooltip:
            self.tooltip.destroy()
            self.tooltip=None
        
        # Mostrar la información de la vulnerabilidad si se cambia de posición
        elif pos!=self.currentPos:
            # Obtener la información de la vulnerabilidad si la posición es válida
            try:
                # Obtener el texto de la celda
                place=table.item(row)["values"][int(col[1])-1]
                if place!="":
                    # Crear el tooltip y su configuración
                    self.tooltip=tk.Toplevel(table, background=MENU)
                    self.tooltip.overrideredirect(True)
                    self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

                    wrapp_tex=textwrap.wrap(str(place), 45)
                    for line in wrapp_tex:
                        # Mostrar el texto de la celda en una etiqueta
                        info=tk.Label(self.tooltip, text=line, font=("Times New Roman", 12), fg=FG2, bg=MENU)
                        info.pack()
            except:
                pass

            # Actualizar la posición del cursor
            self.currentPos=pos

    # Evento de click sobre una vulnerabilidad para mostrar sus detalles
    def selectVulnerability(self, event, table):
        # Recoger la selección de la tabla
        item=table.item(table.selection())

        # Comprobar que la selección es válida
        if item["values"]!="":
            # Guardar el ID de la vulnerabilidad en la variable
            self.var_vuln.set(item["values"][0])

    # Evento de doble click sobre una vulnerabilidad para abrir su página de OSV en el navegador
    def browserVulnerability(self, event, table):
        # Recoger la selección de la tabla
        place=table.item(table.selection())

        # Comprobar que la selección es válida
        if place["values"]!="":
            # Abrir la página de la vulnerabilidad en el navegador
            webbrowser.open("https://osv.dev/vulnerability/"+place["values"][0])

    ''' %%%%%%%%%%%%%% FUNCIONES COMPARADOR %%%%%%%%%%%%%% '''
    # Comparación de dos análisis
    def comparison(self, analysis_1, analysis_2):
        # Limpiar los widgets existentes
        self.clearWidgets()
        self.title("Comparación de Análisis")

        # Frame de la ventana
        self.mainFrame()

        # Título
        self.title_label("Comparación de Análisis", self.main_frame)
        self.title_l.pack_forget()
        self.title_l.pack(pady=(20, 0))

        # Información del primer análisis
        self.analysis_1_label=self.title_label("Análisis con ID: "+str(analysis_1), self.main_frame)
        self.analysis_1_label.pack_forget()
        self.analysis_1_label.pack(pady=(0, 10))
        self.analysis_1_label.config(font=("Times New Roman", 16, "italic"))

        # Contenedor de la tabla de vulnerabilidades1
        self.firstFrame(self.main_frame)
        self.first_frame.pack_forget()
        self.first_frame.pack(fill="x")

        # Tabla de vulnerabilidades1
        self.analysis_1=self.table_widget(self.first_frame, ("ID", "Paquete", "Ecosistema", "Resumen", "Detalles", "Rango afectado", "Versión introducida", "Versión corregida"), "browse")
        self.analysis_1.configure(height=7)

        # Scrollbar de la tabla
        self.scrollbar_widget(self.first_frame, self.analysis_1)
        self.analysis_1.configure(yscrollcommand=self.scrollbar.set)

        # Volcar las vulnerabilidades de la base de datos en la tabla
        self.controlador.listVulnerabilities(self.analysis_1, analysis_1)

        # Eventos de la tabla del primer análisis
        self.currentPos=None
        self.tooltip=None
        self.analysis_1.bind("<Motion>", lambda event: self.show_tooltip(event, self.analysis_1))
        self.analysis_1.bind("<<TreeviewSelect>>", lambda event: self.selectVulnerability(event, self.analysis_1))
        self.analysis_1.bind("<Double-1>", lambda event: self.browserVulnerability(event, self.analysis_1))
        
        
        # Comparativa
        self.secondaryFrame(self.main_frame)
        self.sec_frame.pack_forget()
        self.sec_frame.pack(fill="x")

        self.results_label=self.title_label("Resultados", self.sec_frame)
        self.results_label.pack_forget()
        self.results_label.pack(pady=(10, 0))
        self.results_label.config(font=("Times New Roman", 16, "italic"))

        results=self.controlador.compVulnerabilities(analysis_1, analysis_2)
        cadena="Se han hallado "+str(results[0])+" nuevas vulnerabilidades:    "+results[1]+"\n\nSe han corregido "+str(results[2])+" vulnerabilidades:    "+results[3]+"\n\nSe han mantenido "+str(results[4])+" vulnerabilidades:    "+results[5]
        self.comparativa=tk.Text(self.sec_frame, font=("Times New Roman", 12), fg=FG, bg=BG, height=5)
        self.comparativa.insert("1.0", cadena)
        self.comparativa.tag_configure("center", justify="center")
        self.comparativa.configure(state="disabled")
        self.comparativa.pack(fill="x", expand=True, pady=(5, 10))
        self.widgets_list.append(self.comparativa)

        # Información del segundo análisis
        self.analysis_2_label=self.title_label("Análisis con ID: "+str(analysis_2), self.sec_frame)
        self.analysis_2_label.pack_forget()
        self.analysis_2_label.pack(pady=(0, 10))
        self.analysis_2_label.config(font=("Times New Roman", 16, "italic"))
        
        # Contenedor de la tabla de vulnerabilidades2
        self.thirdFrame(self.main_frame)
        self.third_frame.pack_forget()
        self.third_frame.pack(fill="x")
        self.analysis_2=self.table_widget(self.third_frame, ("ID", "Paquete", "Ecosistema", "Resumen", "Detalles", "Rango afectado", "Versión introducida", "Versión corregida"), "browse")
        self.analysis_2.configure(height=7)

        # Scrollbar de la tabla
        self.scrollbar_widget(self.third_frame, self.analysis_2)
        self.analysis_2.configure(yscrollcommand=self.scrollbar.set)
    
        # Volcar las vulnerabilidades de la base de datos en la tabla
        self.controlador.listVulnerabilities(self.analysis_2, analysis_2)

        # Eventos de la tabla del segundo análisis
        self.currentPos=None
        self.tooltip=None
        self.analysis_2.bind("<Motion>", lambda event: self.show_tooltip(event, self.analysis_2))
        self.analysis_2.bind("<<TreeviewSelect>>", lambda event: self.selectVulnerability(event, self.analysis_2))
        self.analysis_2.bind("<Double-1>", lambda event: self.browserVulnerability(event, self.analysis_2))
        
        # Evento de la ventana 
        self.bind("<Button-1>", lambda event: self.clearSelection(event, self.analysis_1, self.analysis_2))

        # Abrir la vulnerabilidad en el navegador
        self.open_vuln=ttk.Button(self.main_frame, text="Ver en OSV Vulnerability Database", command=lambda: webbrowser.open("https://osv.dev/vulnerability/"+self.var_vuln.get()) if self.var_vuln.get()!="" else None, style="Custom.TButton")
        self.open_vuln.pack(pady=(20, 10))
        self.widgets_list.append(self.open_vuln)

        # Volver a la tabla de análisis
        self.backButton(2)

    ''' %%%%%%%%%%%%%% WIDGETS GENERALES %%%%%%%%%%%%%% '''
    # Crear el frame principal
    def mainFrame(self):
        self.main_frame=ttk.Frame(self, style="Custom.TFrame")
        self.main_frame.pack(fill="both", expand=True)
        self.widgets_list.append(self.main_frame)

    # Crear frames auxiliares
    def firstFrame(self, master):
        self.first_frame=ttk.Frame(master, style="Custom.TFrame")
        self.first_frame.pack()
        self.widgets_list.append(self.first_frame)

    def secondaryFrame(self, master):
        self.sec_frame=ttk.Frame(master, style="Custom.TFrame")
        self.sec_frame.pack()
        self.widgets_list.append(self.sec_frame)

    def thirdFrame(self, master):
        self.third_frame=ttk.Frame(master, style="Custom.TFrame")
        self.third_frame.pack()
        self.widgets_list.append(self.third_frame)

    def fourthFrame(self, master):
        self.fourth_frame=ttk.Frame(master, style="Custom.TFrame")
        self.fourth_frame.pack()
        self.widgets_list.append(self.fourth_frame)

    # Crear frames auxiliares de la ventana secundaria
    def auxFrame1(self):
        self.aux_f1=ttk.Frame(self.sec_windows, style="Custom.TFrame")
        self.aux_f1.pack(fill="x", pady=(30, 20))

    def auxFrame2(self):
        self.aux_f2=ttk.Frame(self.sec_windows, style="Custom.TFrame")
        self.aux_f2.pack(fill="x", pady=20)

    def auxFrame3(self):
        self.aux_f3=ttk.Frame(self.sec_windows, style="Custom.TFrame")
        self.aux_f3.pack(fill="x", pady=(20, 30))

    # Botón para retroceder entre las tablas
    def backButton(self, position):
        # Crear el botón
        self.button_back=self.button_widget(self.main_frame, "Volver Atrás", lambda: (self.clearWidgets(), self.home()))
        self.button_back.pack_forget()
        
        # Volver al inicio
        if position==0:
            self.button_back.pack(padx=(0, 15), pady=5)

        # Volver a la tabla de proyectos
        elif position==1:
            self.button_back.config(command=lambda: (self.clearWidgets(), self.projectsTable()))
            self.button_back.pack()

        # Volver a la tabla de análisis
        elif position==2:
            self.button_back.config(command=lambda: (self.clearWidgets(), self.analysisTable(self.var_project_id.get(), self.var_project_path.get())))
            self.button_back.pack(pady=10)
    # Crear un título
    def title_label(self, text, frame):
        self.title_l=ttk.Label(frame, text=text, style="Custom.TLabel", font=("Times New Roman", 20, "bold"))
        self.title_l.pack(pady=(40, 20))
        self.widgets_list.append(self.title_l)
        return self.title_l

    # Crear un scrollbar
    def scrollbar_widget(self, frame, master):
        self.scrollbar=ttk.Scrollbar(frame, command=master.yview, style="Vertical.TScrollbar")
        self.scrollbar.pack(side="left", fill="y")
        self.widgets_list.append(self.scrollbar)

    # Crear una tabla
    def table_widget(self, frame, columns, selectmode):
        self.table=ttk.Treeview(frame, columns=columns, selectmode=selectmode, height=20)
        for col in self.table["columns"]:
            self.table.column(col, anchor=tk.CENTER)
            self.table.heading(col, text=col)
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.pack(side="left", fill="x", expand=True,)
        self.widgets_list.append(self.table)
        
        return self.table

    # Crear un botón
    def button_widget(self, frame, text, command):
        self.button=ttk.Button(frame, text=text, command=command, style="Custom.TButton")
        self.button.pack(side="left", padx=(15, 0), pady=15, fill="x")
        self.widgets_list.append(self.button)

        return self.button
    
    # Crear un label
    def label_widget(self, frame, text):
        self.label=ttk.Label(frame, text=text, style="Custom.TLabel", font=("Times New Roman", 12, "bold"))
        self.label.pack(side="left", padx=5)
        self.widgets_list.append(self.label)

        return self.label
    
    ''' %%%%%%%%%%%%%% FUNCIONES GENERALES %%%%%%%%%%%%%% '''
    # Limpiar los widgets de la ventana
    def clearWidgets(self):
        # Destruir los widgets almacenados
        for widget in self.widgets_list:
            widget.destroy()

        # Si se está en el inicio, poner la bandera a false
        if self.init:
            self.init=False
        
        # Vaciar la lista de widgets
        self.widgets_list.clear()
    
    # Seleccionar la ruta de un proyecto existente
    def openProject(self, var):
        # Abrir el explorador de archivos
        self.fileBrowser(None, var)

        # Comprobar si el proyecto seleccionado existe
        if var.get()!="Proyecto No Seleccionado":
            self.controlador.chckProject(var)
    
    # Explorador de archivos
    def fileBrowser(self, label, var):
        directory=tk.filedialog.askdirectory()

        # Comprobar si se ha seleccionado un directorio
        if directory:
            # Cambiar la ruta del proyecto si hay una etiqueta
            if label:
                label.config(text=directory)

            # Asignar la ruta del proyecto a la variable
            var.set(directory)

        # Si no se ha seleccionado un directorio
        else:
            var.set("Proyecto No Seleccionado")

    # Evento para eliminar la selección de la tabla
    def clearSelection(self, event, table, table2):
        # Si hay dos tablas (comparación de análisis)
        if table2:
            # Desactivar la selección de la tabla activa
            if event.widget!=table:
                table.selection_remove(table.selection())
            if event.widget!=table2:
                table2.selection_remove(table2.selection())

        # Si hay una tabla, desactivar la selección al hacer click izquierdo fuera de la tabla
        elif event.widget!=table:
            table.selection_remove(table.selection())

    # Apertura de las nuevas ventanas en el centro de la pantalla
    def open_w(self, window):
        # Actualizar la ventana para centrarla en la pantalla
        window.update_idletasks()

        # Obtener el ancho y alto de la pantalla
        screen_width=window.winfo_screenwidth()
        screen_height=window.winfo_screenheight()

        # Obtener el ancho y alto de la ventana
        width=window.winfo_width()
        height=window.winfo_height()
        
        # Calcular la posición de la ventana
        x=(screen_width-width)/2
        y=(screen_height-height)/2

        # Establecer la posición de la ventana
        window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    # Recoger el evento de click derecho en un proyecto o análisis
    def menu_table(self, event, table):
        # Tabla de proyectos
        if table==1:
            # Creamos el menú al hacer click derecho
            self.popup=tk.Menu(self.projects, tearoff=0, bg=MENU)

            # Recoger la selección de la tabla
            item=self.projects.item(self.projects.selection())

            # Si se ha seleccionado un proyecto, desplegar la opción de eliminar
            if item["values"]!="":
                self.popup.add_command(label="Eliminar", command=lambda: self.deleteProject(item["values"][0], self.projects))
            
            # Si no, desplegar la opción de crear
            else:
                self.popup.add_command(label="Añadir", command=lambda: self.createProject(self.var_project_path))
        
        # Tabla de análisis
        elif table==2:
            # Creamos el menú al hacer click derecho
            self.popup=tk.Menu(self.analysis, tearoff=0, bg=MENU)

            # Recoger la selección de la tabla
            item=self.analysis.item(self.analysis.selection())

            # Si se ha seleccionado un análisis, desplegar la opción de eliminar
            if item["values"]!="":
                self.popup.add_command(label="Eliminar", command=lambda: self.deleteAnalysis(item["values"][0]))
        
        # Intentar abrir el menú en la posición del cursor
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    # Mensaje de error al validar un proyecto o un archivo
    def errorMessage(self, option):
        # Si no se ha rellenado algún campo, mostrar un mensaje de error
        if option==0:
            messagebox.showerror("Error", "No ha rellenado todos los campos para crear el proyecto")

        # Si ya existe un proyecto con la misma ruta, mostrar un mensaje de error
        elif option==1:
            messagebox.showerror("Error", "El proyecto ya existe")

        # Si el archivo no se encuentra en el proyecto, mostrar un mensaje de error
        elif option==2:
            messagebox.showerror("Error", "El archivo no se encuentra en el proyecto")

        # El proyecto no existe
        else:
            messagebox.showerror("Error", "El proyecto no existe crea un nuevo proyecto")


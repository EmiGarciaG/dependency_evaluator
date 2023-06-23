# dependency_evaluator
<p align="center">
  <img src="img/icon.ico" alt="Dependency Evaluator" width="200">
</p>


## Descripción
Aplicación para la evaluación de dependencias de un proyecto de software. La aplicación se encarga de analizar el proyecto de software y generar un informe con las dependencias del proyecto que presentan vulnerabilidades. El usuario resolverá las vulnerabilidades, irá actualizando las dependencias y volverá a ejecutar la aplicación para comprobar si se han resuelto las vulnerabilidades.

## Instalación de Dependencias
```bash
pip3 install -r requirements.txt
```

## Instalar software de terceros
Tener previamente descargado [OSV-Scanner](https://github.com/google/osv-scanner/releases/), cambiar el nombre del ejecutable a *osv-scanner* y otorgrar permisos de ejecución.

```bash

chmod +x osv-scanner

```

## Uso
Ejecución de la aplicación

```bash
python3 app.py

```

## Consideraciones

## Consideraciones Importantes

**¡Importante! Si cambias los nombres de los archivos, el programa no funcionará correctamente.**

**Asegúrate de no cambiar el nombre de la base de datos local ni el ejecutable de OSV (solamente puede tener el nombre indicado previamente).**


## Licencia

GNU Affero General Public License Version 3.0

## Contacto

Correo electrónico: i92gague@uco.es


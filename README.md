Esta versión toma los datos de una planilla de Google Sheets, la cual se llena a través de una encuesta desde un chatbot, y guarda los resultados en una columna de esa misma planilla.

# Para correrlo:

#### Tener la versión de python3.8 o superior instalada

    python3 --version
    
>si no funciona en vez de "python3" probar "py" o "python"

#### Crear un entorno virtual usando el comando

    python3 -m venv <environment_name> 

>un nombre común usado es: .venv  
>como comenté anteriormente si no funciona probar con "python" o "py" en vez de "python3"

#### Activar entorno virtual

    source <environment_name>/bin/activate 

>yo para activarlo tuve que correr `.\.venv\Scripts\activate` , si no funciona probar así

#### Instalar los requirements

    pip install -r requirements.txt

#### Ejecutar el codigo con

    python3 main.py 

>como comenté anteriormente si no funciona probar con "python" o "py" en vez de "python3"

#### Tambien tener en cuenta que van a necesitar ciertos archivos, como por ejemplo las credenciales, los cuales no estan subidos al repositorio por motivos de seguridad
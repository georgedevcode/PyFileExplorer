def agregar_documento(registro, nombre, referencia, fecha, descripcion, ubicacion):
    registro[nombre] = (referencia, fecha, descripcion, ubicacion)

def buscar_documento(registro, nombre):
    return registro.get(nombre, None)

def mostrar_registro(registro):
    for nombre, (referencia, fecha, descripcion, ubicacion) in registro.items():
        print(f"Nombre: {nombre}")
        print(f"Referencia: {referencia}")
        print(f"Fecha: {fecha}")
        print(f"Descripcion: {descripcion}")
        print(f"Ubicacion: {ubicacion}")
        print("-" * 20)

def guardar_registro_en_archivo(registro, archivo):
    with open(archivo, "w") as f:
        for nombre, (referencia, fecha, descripcion, ubicacion) in registro.items():
            f.write(f"Nombre: {nombre}\n")
            f.write(f"Referencia: {referencia}\n")
            f.write(f"Fecha: {fecha}\n")
            f.write(f"Descripcion: {descripcion}\n")
            f.write(f"Ubicacion: {ubicacion}\n")
            f.write("-" * 20 + "\n")

# Registro para los documentos
registro_documentos = {}

agregar_documento(registro_documentos, "Documento1", "REF001", "2023-08-04", "Documento de ejemplo 1", "Carpeta A")
agregar_documento(registro_documentos, "Documento2", "REF002", "2023-08-04", "Documento de ejemplo 2", "Carpeta B")

# se mostrar el registro completo
mostrar_registro(registro_documentos)

# se guardara el registro en un archivo de texto
archivo_registro = "registro_documentos.txt"
guardar_registro_en_archivo(registro_documentos, archivo_registro)
print(f"Registro guardado en '{archivo_registro}'")

# Buscar un documento específico
nombre_documento = "Documento1"
documento_encontrado = buscar_documento(registro_documentos, nombre_documento)
if documento_encontrado:
    print(f"Documento encontrado: {nombre_documento}")
    referencia, fecha, descripcion, ubicacion = documento_encontrado
    print(f"Referencia: {referencia}")
    print(f"Fecha: {fecha}")
    print(f"Descripción: {descripcion}")
    print(f"Ubicación: {ubicacion}")

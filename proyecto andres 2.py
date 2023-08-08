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

# Registro de documentos
registro_documentos = {}

agregar_documento(registro_documentos, "Documento1", "REF001", "2023-08-04", "Documento de ejemplo 1", "Carpeta A")
agregar_documento(registro_documentos, "Documento2", "REF002", "2023-08-04", "Documento de ejemplo 2", "Carpeta B")

#se mostrara el registro completo
mostrar_registro(registro_documentos)

# se buscara un documento especifico
nombre_documento = "Documento1"
documento_encontrado = buscar_documento(registro_documentos, nombre_documento)
if documento_encontrado:
    print(f"Documento encontrado: {nombre_documento}")
    referencia, fecha, descripcion, ubicacion = documento_encontrado
    print(f"Referencia: {referencia}")
    print(f"Fecha: {fecha}")
    print(f"Descripción: {descripcion}")
    print(f"Ubicación: {ubicacion}")
else:
    print(f"El documento '{nombre_documento}' no se encontro en el registro.")

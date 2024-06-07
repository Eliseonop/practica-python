import openpyxl
import json

# Cargar el archivo de Excel y seleccionar la hoja específica
workbook = openpyxl.load_workbook("HORARIOS DE INGRESOS 2024.xlsx")
sheet = workbook["JUNIO 2024 "]  # Reemplaza "Nombre de la hoja" con el nombre de tu hoja

# Definir la lista para almacenar los objetos JSON
data_list = []

# Definir la fila y columna de inicio para leer los datos
start_row = 27  # Cambia a la fila desde donde quieres comenzar a leer
start_col = 1  # Cambia a la columna desde donde quieres comenzar a leer
end_col = 7
# Iterar sobre las filas y leer los datos
for index, row in enumerate(sheet.iter_rows(min_row=start_row, min_col=start_col, max_col=end_col, values_only=True)):
    obj = {}
    obj["id"] = str(row[0])
    obj["nombre"] = str(row[1])
    obj["entrada1"] = str(row[2])
    obj["salida1"] = str(row[3])
    obj["entrada2"] = str(row[4])
    obj["salida2"] = str(row[5])
    obj["Horas"] = str(row[6])
    data_list.append(obj)

# Convertir la lista de objetos JSON a formato JSON
json_data = json.dumps(data_list, indent=2)
output_file = "horarios_ingresos.json"
with open(output_file, 'w') as f:
    json.dump(data_list, f, indent=2)
# Imprimir el resultado
print(json_data)

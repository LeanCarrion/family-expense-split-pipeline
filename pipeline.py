import openpyxl
import pandas as pd

# Etapa de extraccion

# 1. Definimos la ruta del archivo genérico dentro de tu carpeta invisible
archivo_excel = "data/resumen.xlsx"

print("="*45)
print("Iniciando extracción del pipeline desde Excel...")
print("="*45)

# 2. Cargamos el libro de trabajo y seleccionamos la hoja activa
wb = openpyxl.load_workbook(archivo_excel, data_only=True) # data_only=True trae los valores, no las fórmulas
hoja = wb.active

datos_tarjetas = []
leyendo_totales = False

# 3. Iteramos fila por fila para parsear la estructura sucia
for fila in hoja.iter_rows(values_only=True):
    # fila es una tupla con los valores de cada celda: (ColA, ColB, ColC, ...)
    
    # Si la fila está completamente vacía, pasamos a la siguiente
    if not fila or fila[0] is None:
        continue
    
    #  SECCIÓN 1: Detectar el inicio de la tabla de totales
    if "Tarjetas incluidas en el resumen" in str(fila[0]):
        leyendo_totales = True
        continue # Saltamos la línea del encabezado
        
    #  SECCIÓN 2: Si estamos en la zona de totales, extraemos los datos de tus hermanos
    if leyendo_totales:
        # Si encontramos una fila vacía o cambia de sección ("Cierres y vencimientos"), frenamos el procesamiento de esta tabla
        if "Cierres" in str(fila[0]) or fila[0] is None:
            leyendo_totales = False
            break
            
        # Mapeamos las columnas exactas según el formato del banco
        tarjeta_info = fila[0]  # Ej: "Visa Crédito terminada en xxxx"
        titular_rol = fila[1]   # Ej: "Adicional de Leonardo..."
        monto_pesos = fila[2]   # Ej: "$379.675,25"
        monto_dolares = fila[3] # Ej: "U$S0,00"
        
        # Limpiamos el rol de los textos del banco para que quede el nombre limpio
        nombre_limpio = str(titular_rol).replace("(Adicional)", "").replace("(Titular)", "").replace("Adicional de ", "").strip()
        
        # Guardamos en nuestra lista de diccionarios
        datos_tarjetas.append({
            "Tarjeta": tarjeta_info,
            "Usuario": nombre_limpio,
            "Pesos": monto_pesos,
            "Dólares": monto_dolares
        })

# 4.Convertimos la lista sucia extraída en un DataFrame limpio de Pandas
df_final = pd.DataFrame(datos_tarjetas)

print("\n📊 Extracción completada. Datos listos en memoria:")
print(df_final)


# Etapa de limpieza de datos


print("\n🧹 Iniciando etapa de transformación y limpieza de strings...")

# Definimos una función helper para limpiar las monedas de manera genérica (Si en algun momento cambian la forma de escribir los datos en el xlsx cambiar aca)
def limpiar_monto_banco(valor):
    # Si el dato es nulo o está vacío, devolvemos 0.0 de entrada
    if pd.isna(valor) or str(valor).strip() == "" or valor is None:
        return 0.0
    
    # Pasamos a string para asegurar que podemos aplicar funciones de texto
    texto = str(valor)
    
    # Paso 1: Limpieza de caracteres de moneda, comillas y espacios
    texto = texto.replace("$", "").replace("U$S", "").replace('"', '').strip()
    
    # Paso 2: Corrección de formato numérico regional
    # Primero eliminamos los puntos que separan miles (ej: 1.234,56 -> 1234,56)
    texto = texto.replace(".", "")
    # Segundo cambiamos la coma decimal por el punto de Python (ej: 1234,56 -> 1234.56)
    texto = texto.replace(",", ".")
    
    # Paso 3: Conversión final a tipo numérico decimal
    try:
        return float(texto)
    except ValueError:
        # Si por alguna razón coló un texto extraño, devolvemos 0.0 y evitamos que rompa el pipeline
        return 0.0

# -------------------------------------------------------------------------
# Aplicamos la limpieza a las columnas correspondientes usando .map()
# -------------------------------------------------------------------------

# Limpiamos la columna de Pesos
print("-> Limpiando montos en Pesos...")
df_final["Pesos"] = df_final["Pesos"].map(limpiar_monto_banco)

# Limpiamos la columna de Dólares
print("-> Limpiando montos en Dólares...")
df_final["Dólares"] = df_final["Dólares"].map(limpiar_monto_banco)

print("\n✅ Transformación completada. Tipos de datos corregidos:")
print(df_final.dtypes) # Esto te va a mostrar en la terminal que ahora son float64
print("\n📊 DataFrame Limpio y listo para operar:")
print(df_final)
#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import pandas as pd

app = Flask(__name__)

df= None
url= None

@app.route('/')
def saludo():
    global df
    print( "hola")
    print(url)
    return str(df.shape)

@app.route('/cargar_archivo', methods=['POST'])
def cargar_url():
	global df
	global url
	url = request.json.get('url')
	sep = request.json.get('sep')
#	print("set_url: %s sep: %s /n"%(url,sep))
	df= pd.read_csv(url, sep=sep)
	return str(' ')

#REINICIAR DATA SET
@app.route('/init')
def reiniciar():
	df= pd.read_csv('/myhome/python/data_prueba.csv', sep=';')	
	return str(' ')

#CONTAR FILAS Y COLUMAS
@app.route('/shape')
def contar_filas_columnas():
	global df
	shape = df.shape
	return("cantidad de filas, columnas "+ str(shape)+ "\n")

#MOSTRAR NOMBRE ATRIBUTOS 
@app.route('/atributos')
def atributos():
	global df
	atributo = df.columns.values.tolist()
#	cadena = str(type(atributo))
	cadena = ""
	for i in atributo:
		cadena = cadena + str(i) + ";" 
	return(cadena + "\n")

#MOSTRAR TIPO DE DATOS DE LAS COLUMNAS
@app.route('/tipos')
def tipo_datos():
	global df
	tipo_dato= df.dtypes
	resp =" "+str(tipo_dato)+ "\n"
	return(" "+ resp)	

#FUNCIONES DE AGREGACION 
@app.route('/funcion', methods=['POST'])
def funcion():
	global df
	atributo = request.json.get('atributo')
	operador = request.json.get('operador')
	cabecera = df.columns.values.tolist()
	columna= [0]	
	respuesta= ""

	if atributo in cabecera: 
		columna = df[atributo]

		respuesta = "operador invalido"		
		if str(operador) ==  "media": 
			respuesta= "media: " + str(columna.mean())
		if str(operador) == "mediana":
			respuesta= "mediana: " + str(columna.median())
		if str(operador) == "moda":
			respuesta= "moda: "+ str(columna.mode())	
					 
	else:
		return("dato invalido \n")
	
	return(""+ respuesta+" \n") 



#AGRUPACION
@app.route('/agrupacion', methods=['POST'])
def agrupacion(): 
	global df
	agrupar= request.json.get('agrupar')
	campos= request.json.get('campos')
	operador= request.json.get('operador')
	grouped= df.groupby(agrupar)[campos]

	respuesta = "operador invalido"
	if str(operador) ==  "media":
		respuesta= "media: " + str(grouped.mean()) 
	if str(operador) == "mediana":
		respuesta= "mediana: " + str(grouped.median())
	if str(operador) == "sum":
		respuesta= "sum: "+ str(grouped.sum())	
#	print("dato ",len(df))
#	print("dato ",type(df))
#	print("dato: ", str(grouped.mean())) 
	return(respuesta+ "\n")




if __name__ == '__main__':
    df= pd.read_csv('/myhome/python/data_prueba.csv', sep=';')
    app.run(host='0.0.0.0',debug=True)


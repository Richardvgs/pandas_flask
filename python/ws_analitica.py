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

if __name__ == '__main__':
    df= pd.read_csv('/myhome/python/data_prueba.csv', sep=';')
    app.run(host='0.0.0.0',debug=True)


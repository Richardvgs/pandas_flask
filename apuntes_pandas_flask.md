TALLER COMO MONTAR EL CONTENEDOR EN VAGRANT, EXPONER UNA APLICACION WEB EN EL SERVIDOR XENIAL, EXPONER SERVICIOS WEB EN 
PYTHON  CON LA BIBLIOTECA FLASK  Y PROCESAR DATOS (HACER ANALITICA)CON PYTHON - PANDAS 
 
1. Montar Vagrant yy Virtual Box compatible en la maquina

2. montar el vagrantfile estandar  con la maquina que ya tiene isntalado el docker es la maquina que usamos en la practica

//
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "josanabr/xenial-docker"
  config.vm.provider :virtualbox do |vb|
    vb.customize [ 'modifyvm', :id, '--name', 'test-00' ]
    vb.customize [ 'modifyvm', :id, '--memory', '1250' ]
  end
end

//Parametrizar el virtualbox antes de hacer el vagrant up
-> Ir a las propiedades de la maquina virtual y cambiar el puerto serie, modo puerto: desconectado
-> vagrant up 
-> vagrant ssh

3. montar el github: iniciar la sesion, crear un nuevo repositorio, ejecutar las siguientes lineas de comando, primero toca
montar el git pero se puede hacer en la maquina virtual para no tocar la maquina local 

//configurar git, el sudo es para que lo ejecute como root
sudo apt-get update
sudo apt-get install git

//ir al direcgtorio vagrant para que los documentos queden montados en la maquina real 
cd /vagrant/

//
echo "# pandas_flask" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/Richardvgs/pandas_flask.git
git push -u origin master


//Vagrantfile
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "josanabr/xenial-docker"
  config.vm.provision "shell", path: "aprovicionamiento.sh" 
  config.vm.provider :virtualbox do |vb|
    vb.customize [ 'modifyvm', :id, '--name', 'test-00' ]
    vb.customize [ 'modifyvm', :id, '--memory', '1250' ]
  end
end

//aprovicionamiento.sh
#!/usr/bin/env bash
cd ./github/
echo "# pandas_flask" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/Richardvgs/pandas_flask.git

//cuando quise montar otro delos archivos en el github me tiro problemas hasta que corri el sigueinte comando
git config --global user.name "richardvgs"

// despues corri el comando 
git push -u origin master
git add apuntes_pandas_flask.md 
git commit -m "second commit"
git push -u origin master

// cuando se desnivelan los repositorios toca igualarlos con el comando
git pull


#4. MONTAR DOCKER CON PYTHON, FLASK (WS), PANDAS(ANALITICA)

// llamar a un contenedor ya creado en mi repositorio, el Docker File de ese contenedor es el siguiente:

FROM ubuntu

MAINTAINER John Sanabria - john.sanabria@gmail.com

RUN apt-get update

RUN apt-get -y --fix-missing install python3-pip ; exit 0

RUN pip3 install Flask

EXPOSE 5000
vagrant@dockervm2:~/dockerflask2018$ nano Dockerfile 
vagrant@dockervm2:~/dockerflask2018$ cat Dockerfile 
FROM ubuntu

MAINTAINER Ricardo Vargas - ricahrdvgs@gmail.com

RUN apt-get update

RUN apt-get -y --fix-missing install python3-pip ; exit 0

RUN pip3 install Flask

EXPOSE 5000 

// para llamar ese contendedor ejecutar el siguiente comando. OJO no lo vaya a correr por que ese se va a llamar es desde un vagranti file para montar PANDAS
docker run --rm -it -p 5000:5000 -v $(pwd):/myhome richardvgs/flask_pandas_taller  /bin/bash

// modificar el vagrant file de flask para ademas adicionar pandas 

FROM ubuntu

MAINTAINER Ricardo Vargas - richardvgs@gmail.com

RUN apt-get update

RUN apt-get -y --fix-missing install python3-pip ; exit 0

RUN pip3 install Flask

RUN pip3 install pandas numpy

EXPOSE 5000


// contruir la imagen del contenedor 
docker build -t richardvgs/flask_pandas_taller .

// correr para probarla
docker run --rm -it -v $(pwd):/myhome richardvgs/flask_pandas_taller /bin/bash

# 5. comenzar a construir el fuente en python para el web service y el analisis de datos 

// crear la fuente donde se va a colocar el codigo python 
nano ws_analitica.py

#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import pandas as pd

app = Flask(__name__)
df= None

@app.route('/')
def saludo():
    global df
    print( "hola")
    return str(df.shape)

if __name__ == '__main__':
    df= pd.read_csv('/myhome/python/data_prueba.csv', sep=';')
    app.run(host='0.0.0.0',debug=True)

// probar que funcione
	pararse en maquina virtual dentro del carpeta "docker"
	correr el contenedor
	docker run --rm -it -p 5000:5000 -v $(pwd):/myhome richardvgs/flask_pandas_taller /bin/bash
	en la consola del contenedor: python3 ./ws_analitica.py 
	en la cosnola de la maquina virtual:  curl http://localhost:5000/
	-- va a aparecer hola en la consola del contenedor que es el unico servicio montado hasta ahora 

// usar Curl para consumir servicios post - carga de archivos

	curl http://localhost:5000/tipos
	curl -i -H "Content-Type: application/json" -X POST -d '{"title": "read a book"}' http://localhost:5000/todo/api/v1.0/tasks

        curl -i -H "Content-Type: application/json" -X POST -d'{"url": "www.google.com", "sep": "c"}' http://localhost:5000/cargar_archivo
        curl -i -H "Content-Type: application/json" -X POST -d'{"url": "https://raw.githubusercontent.com/chendaniely/pandas_for_everyone/master/data/housing.csv", "sep": "c"}' http://localhost:5000/cargar_archivo
	curl -i -H "Content-Type: application/json" -X POST -d '{ "url": "https://raw.githubusercontent.com/jennybc/gapminder/master/inst/extdata/gapminder.tsv", "sep": "\t"}' http://localhost:5000/cargar_archivo

// funciones de agregacion y agrupaciones
	curl -i -H "Content-Type: application/json" -X POST -d'{"atributo": "NIT", "operador": "moda"}' http://localhost:5000/funcion	
	curl -i -H "Content-Type: application/json" -X POST -'{"agrupar": "country", "campos": "lifeExp", "operador": "sum"}' http://localhost:5000/agrupacion
 
#5. MONTAR EL CONTENEDOR EN AWS

se debe acomodar el contenedor actual para que ejecute solo sin entar al /bin/bash
   toca crear otro docker file y otra imagen donde ya funcione automaticamente y esa si es la que se despliega en AWS

// Desplegar contenedor actual en el dockerhub 
	docker build -t richardvgs/flask_pandas:1.0.0 .
	docker push richardvgs/flask_pandas:1.0.0
	docker login

// crear un nuevo contenedor que trabaje de forma automatica
  
   Dockerfile:

FROM richardvgs/flask_pandas:1.0.0
MAINTAINER Ricardo Vargas - richardvgs@gmail.com
COPY ./python/ws_analitica.py /myhome/ws_analitica.py
COPY ./python/data_prueba.csv /myhome/python/data_prueba.csv
ENTRYPOINT [ "python3" ]
CMD [ "/myhome/ws_analitica.py" ]

// desplegarlo y probarlo (el automatico) ojo cambia el numero de la version

	docker build -t richardvgs/flask_pandas:1.0.2 .
	docker push richardvgs/flask_pandas:1.0.2
	docker run  -p 5000:5000 richardvgs/flask_pandas:1.0.2
	
	curl http://localhost:5000/tipos


// montar el proyecto en AWS

	inicar sesion en AWS
	services -> Elastic Beanstalk
	crear enviroment -> colocar nombre
	plataforma: docker
	subir codigo: crear el siguiente archivo .json
	crear 

	Archivo aws.json:
  {
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "richardvgs/flask_pandas:1.0.2",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "5000"
    }
  ],
  "Logging": "/var/log/nginx"}
	
// probar (ver que no toca colocar el puerto en el curl)

	curl -i http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/tipos

#6. PREPARAR PRESENTACION
	
	a. cargar archivo de la web:
	curl -i -H "Content-Type: application/json" -X POST -d'{"url": "https://raw.githubusercontent.com/chendaniely/pandas_for_everyone/master/data/housing.csv", "sep": "c"}' http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/cargar_archivo
		
	b. consultar numero de filas y columnas
	curl -i http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/shape

	c. mostrar nombre de atributo de los datos 
	curl -i http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/atributos

	curl -i -H "Content-Type: application/json" -X POST -d '{ "url": "https://raw.githubusercontent.com/jennybc/gapminder/master/inst/extdata/gapminder.tsv", "sep": "\t"}' http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/cargar_archivo 

	d. funciones de agregacion 	
	curl -i -H "Content-Type: application/json" -X POST -d'{"atributo": "year", "operador": "media"}' http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/funcion
	curl -i -H "Content-Type: application/json" -X POST -d'{"atributo": "year", "operador": "mediana"}' http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/funcion

	e. agrupar
	curl -i -H "Content-Type: application/json" -X POST -d '{"agrupar": "country", "campos": "lifeExp", "operador": "sum"}' http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/agrupacion
	curl -i -H "Content-Type: application/json" -X POST -d '{"agrupar": "country", "campos": "lifeExp", "operador": "media"}' http://tallerpacifictic202-env.hizvr3mngk.us-east-2.elasticbeanstalk.com/agrupacion


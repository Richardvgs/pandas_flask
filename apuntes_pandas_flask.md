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

//

4.Montar el docker -> modifique el vagrant file para que leyera un .sh que tenia la mayoria de los comandos del git 
configurados   

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




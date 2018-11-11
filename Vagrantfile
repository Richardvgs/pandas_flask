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


# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.box_version = "1.1.0"

  # config.vm.synced_folder "../share", "/share"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    vb.memory = "2048"
  end

   config.vm.provision "shell", privileged: false, inline: <<-SHELL
     cd /vagrant; ./provision.sh
   SHELL

end

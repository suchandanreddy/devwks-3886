# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    # Deploy Multiple Nodes in a single Vagrantfile

    # Node 1: IOS XE Device
    config.vm.define "iosxe1" do |node|
        node.vm.box =  "iosxe/16.06.04"

        config.vm.network :forwarded_port, guest: 22, host: 2122, id: 'ssh', auto_correct: true
        config.vm.network :forwarded_port, guest: 830, host: 2123, id: 'netconf', auto_correct: true
        config.vm.network :forwarded_port, guest: 80, host: 2124, id: 'restconf', auto_correct: true
        config.vm.network :forwarded_port, guest: 443, host: 2125, id: 'restconf-ssl', auto_correct: true

        #auto-config is not supported
        node.vm.network :private_network, virtualbox__intnet: "wire1", auto_config: false
      end

    # Node 2: IOS XE Device
    config.vm.define "iosxe2" do |node|
          node.vm.box =  "iosxe/16.06.04"

          config.vm.network :forwarded_port, guest: 22, host: 2222, id: 'ssh', auto_correct: true
          config.vm.network :forwarded_port, guest: 830, host: 2223, id: 'netconf', auto_correct: true
          config.vm.network :forwarded_port, guest: 80, host: 2224, id: 'restconf', auto_correct: true
          config.vm.network :forwarded_port, guest: 443, host: 2225, id: 'restconf-ssl', auto_correct: true

          #auto-config is not supported
          node.vm.network :private_network, virtualbox__intnet: "wire1", auto_config: false
      end
end

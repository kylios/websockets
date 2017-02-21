# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.network :forwarded_port, guest: 5000, host: 8080

    config.vm.provider "virtualbox" do |vb, override|
        override.vm.box = "ubuntu/xenial64"
        vb.memory = 1024
        override.ssh.forward_agent = true
    end

    config.vm.define "development", autostart: true do |server|
        server.vm.hostname = "websockets"
        server.vm.synced_folder ".", "/vagrant"
        server.vm.provision "ansible" do |ansible|
            ansible.playbook = "deploy/playbooks/deploy/all.yml"
            ansible.inventory_path = "deploy/environments/development"
            ansible.verbose = "vvv"
        end
    end
end
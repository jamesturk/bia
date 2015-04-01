# vi: set ft=ruby

VAGRANTFILE_API_VERSION = "2"

Vagrant.require_version ">= 1.5.0"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "chef/ubuntu-14.10"

    config.vm.define "db" do |db|
        db.vm.network "private_network", ip: "10.135.1.101"

        db.vm.provider "virtualbox" do |v|
            v.memory = 1024
            v.name = "db.opencivicdata.org"
        end

        db.vm.provision "ansible" do |ansible|
            ansible.playbook = "ansible/db.yml"
            ansible.inventory_path = "ansible/hosts.vagrant"
            ansible.limit = "all"
            # needed for common tasks to avoid EBS & checkout over synced_folders
            ansible.extra_vars = { deploy_type: "vagrant" }
            # seems to avoid the delay with private IP not being available
            ansible.raw_arguments = ["-T 30"]
        end
    end
end


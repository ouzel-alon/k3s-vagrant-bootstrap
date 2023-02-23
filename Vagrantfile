# -*- mode: ruby -*-
# vi: set ft=ruby :

NUM_SERVERS = 1
NUM_NODES = 2
SUBNET = "192.168.1"
KEYPAIR_NAME = "id_ed25519_k3s"
K3S_ANSIBLE_PATH = "../k3s-ansible"

Vagrant.configure("2") do |config|
  # config.vm.box = "generic/rocky9"
  config.vm.box = "generic/alpine316"

  config.vm.provider :virtualbox do |vb|
    vb.customize [ "modifyvm", :id, "--ioapic", "on", "--hwvirtex", "on", "--pagefusion", "on" ]
    vb.linked_clone = true
    vb.memory = 4096
  end

  # setup passwordless ssh access
  ssh_prv_key = File.read("#{Dir.getwd}/files/#{KEYPAIR_NAME}")
  ssh_pub_key = File.readlines("#{Dir.getwd}/files/#{KEYPAIR_NAME}.pub").first.strip

  ssh_prv_setup_script = <<-SHELL
    echo "#{ssh_prv_key}" > /home/vagrant/.ssh/id_k3s
    chmod 600 /home/vagrant/.ssh/id_k3s
    chown -R vagrant:vagrant /home/vagrant
  SHELL

  ssh_pub_setup_script = <<-SHELL
    if [[ $(grep "#{ssh_pub_key}" "/home/vagrant/.ssh/authorized_keys") ]]; then
      echo "SSH keys already provisioned."
      exit 0;
    fi
    mkdir -p /home/vagrant/.ssh

    touch /home/vagrant/.ssh/authorized_keys
    echo '#{ssh_pub_key}' >> /home/vagrant/.ssh/authorized_keys
    echo '#{ssh_pub_key}' >> /home/vagrant/.ssh/id_k3s.pub
    chmod -R 600 /home/vagrant/.ssh/authorized_keys
    chmod -R 644 /home/vagrant/.ssh/id_k3s.pub

    echo 'Host #{SUBNET}.*' >> /home/vagrant/.ssh/config
    echo 'StrictHostKeyChecking no' >> /home/vagrant/.ssh/config
    echo 'UserKnownHostsFile /dev/null' >> /home/vagrant/.ssh/config
    chmod -R 600 /home/vagrant/.ssh/config
  SHELL

  # ansible control node
  ansible_node_name = "ansible"
  config.vm.define ansible_node_name do |a|
    a.vm.hostname = ansible_node_name
    a.vm.network :private_network, ip: "#{SUBNET}.100"
    a.vm.synced_folder ".", "/home/vagrant/ansible", mount_options: ["dmode=775", "fmode=644"]
    a.vm.synced_folder "#{K3S_ANSIBLE_PATH}", "/home/vagrant/k3s-ansible", mount_options: ["dmode=775", "fmode=644"]
    a.vm.provision "shell", inline: ssh_prv_setup_script, privileged: false
    a.vm.provision "shell", inline: ssh_pub_setup_script, privileged: false
    a.vm.provision "shell", privileged: false, path: "scripts/install_ansible"
    a.vm.provision "shell", privileged: false, path: "scripts/test_ansible"
  end

  # k3s servers/masters
  (1..NUM_SERVERS).each do |node|
    config.vm.define "k3sm#{node}" do |m|
      m.vm.hostname = "k3sm#{node}"
      m.vm.network :private_network, ip: "#{SUBNET}.1#{node-1}"
      m.vm.provision "shell", inline: "apk add python3"
      m.vm.provision "shell", inline: ssh_pub_setup_script, privileged: false
    end
  end

  # k3s nodes/workers
  (1..NUM_NODES).each do |node|
    config.vm.define "k3sw#{node}" do |w|
      w.vm.hostname = "k3sw#{node}"
      w.vm.network :private_network, ip: "#{SUBNET}.2#{node-1}"
      w.vm.provision "shell", inline: "apk add python3"
      w.vm.provision "shell", inline: ssh_pub_setup_script, privileged: false
    end
  end
end

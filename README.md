# Lightweight Kubernetes (k3s) bootstrapper

Quickly bootstrap a k3s sandbox cluster using Vagrant from a Windows 10/11 host.

Designed to be used with [k3s-ansible](https://github.com/k3s-io/k3s-ansible).

## Host requirements

- Windows 10/11
- VirtualBox 6+
- [Vagrant](https://www.vagrantup.com/)
- [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) (optional)

## Default address space

- `192.168.1.100` - Ansible control node
- `192.168.1.[10:19]` - k3s server nodes
- `192.168.1.[20:29]` - k3s agent nodes

## Usage

Generate an SSH keypair, then place both keys under the `files` directory:

```bash
ssh-keygen -t ed25519
```

Ensure Virtualbox has a host-only network (File -> Host Network Manager) configured on the correct subnet.

To customize the cluster like the number of nodes that get built, update the variables near the top of the `Vagrantfile`. You can also update the subnet here to match your Virtualbox host-only network:

```ruby
NUM_SERVERS = 1
NUM_NODES = 2
SUBNET = "192.168.1"
KEYPAIR_NAME = "id_ed25519_k3s"
K3S_ANSIBLE_PATH = "../k3s-ansible"
```

Clone [k3s-ansible](https://github.com/k3s-io/k3s-ansible) to the parent folder that you cloned this repo. If it's in
a different location, update `K3S_ANSIBLE_PATH` in the `Vagrantfile` so it gets synced to the Ansible control node.

Provision the Ansible control node and the k3s cluster:

```bash
cd k3s-vagrant-bootstrap
vagrant up
```

Update `inventory/hosts.ini` with your server IPs or copy over `hosts.ini` from k3s-ansible if you have it setup already.

Connect to the Ansible control node and confirm Ansible can reach all running nodes using your SSH key:

```bash
vagrant ssh ansible

ssh-agent -s
ssh-add ~/.ssh/id_k3s

cd ansible
ansible -m ping all -i inventory/hosts.ini
```

On the Ansible control node, navigate to your synced folder mount of k3s-ansible and run the `site.yml` playbook to provision the cluster:

```bash
vagrant ssh ansible
cd k3s-ansible
ansible-playbook site.yml -i inventory/hosts.ini
```

After the playbook has finished running, connect to a server node from the host and check the cluster details:

```bash
vagrant ssh k3sm1
$ sudo kubectl cluster-info
$ sudo kubectl get services -A
$ sudo kubectl get nodes
```

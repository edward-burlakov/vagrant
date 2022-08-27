# Образ для развертывания
ISO = "bento/ubuntu-20.04"
# Префикс для LAN сети
NET="192.168.192."
# Домен который будем использовать для всей площадки
DOMAIN=".netology"
# Файл конфигурации ansible
INVENTORY_PATH = "../ansible/inventory"
# Массив из хешей, в котором заданы настройки для каждой виртуальной машины
servers=[
  {
    :hostname => "ansible" + DOMAIN,
    :ip => NET + "11",
	:ram => 2048,
	:core => 1  
  },
  {
    :hostname => "docker" + DOMAIN,
    :ip => NET + "12",
	:ram => 2048,
	:core => 1  
  }
]
 
# Входим в Главную конфигурацию vagrant версии 2

Vagrant.configure(2) do |config|
	config.vm.synced_folder ".", "/vagrant", disabled: false
    # Проходим по элементах массива "servers"
    servers.each do |machine|
        # Применяем конфигурации для каждой машины. Имя машины(как ее будет видно в Vbox GUI) находится в переменной "machine[:hostname]"
        config.vm.define machine[:hostname] do |node|
            # Поднять машину из образа "ubuntu 20.04"
            node.vm.box = ISO
            # Hostname который будет присвоен VM (самой ОС)
            node.vm.hostname = machine[:hostname]
            # Добавление и настройка внутреннего сетевого адаптера
            node.vm.network "private_network", ip: machine[:ip]
			# Проброс порта внутрь гостевой машины
			# config.vm.network "forwarded_port", guest: machine[:ssh_vm], host: machine[:ssh_host]
            # Тонкие настройки для конкретного провайдера (в нашем случаи - VBoxManage)
            node.vm.provider "virtualbox" do |vb|
                # Размер RAM памяти
                vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
				# Количество ядер
				vb.customize ["modifyvm", :id, "--cpus", machine[:core]]
                # Перезаписать название VM в Vbox GUI
                vb.name = machine[:hostname]
            end
        end
    end
end
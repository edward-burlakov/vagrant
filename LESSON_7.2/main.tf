// Configure the Yandex.Cloud provider

provider "yandex" {
// Все переменные находятся в файле variables.tf
  token     = "${var.YC_TOKEN}"
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
  zone = "ru-central1-a"
}

// Create a new instance . Выбираем планируемую конфигурацию и зоны  для размещения инстанса.
resource "yandex_compute_instance" "node01" {
      name                      = "node01-lesson-7.2"
      zone                      = "ru-central1-a"
      hostname                  = "node01.netology.cloud"
      allow_stopping_for_update = true

      resources {
        cores  = 2
        memory = 2
      }

      // Create a new boot disk. Выбираем базовый образ-источник и тип диска.
      boot_disk {
        initialize_params {
          image_id = "${var.centos-7-base-image}"
          name     = "root-node01-disk"
          type     = "network-nvme"
          size     = "20"
        }
      }

      network_interface {
        subnet_id = "${yandex_vpc_subnet.subnet-1.id}"
        nat       = true
      }

      metadata = {
        ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
      }
}

  // Create a new net and subnet . Выбираем планируемый диапазон IP-адресов.
  resource "yandex_vpc_network" "network-1" {
    name = "network1"
  }

  resource "yandex_vpc_subnet" "subnet-1" {
    name           = "subnet1"
    zone           = "ru-central1-a"
    network_id     = "${yandex_vpc_network.network-1.id}"
    v4_cidr_blocks = ["192.168.101.0/24"]
  }

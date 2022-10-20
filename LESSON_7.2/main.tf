// Configure the Yandex.Cloud provider
variable "YC_TOKEN" {
  default = ""
}
provider "yandex" {
  token = "${var.YC_TOKEN}"
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
  zone = "ru-central1-a"
}

// Выбираем используемый образ
resource "yandex_compute_image" "centos-7-v20220620" {
  name       = "centos-7-v20220620"
}

// Create a new instance . Выбираем планируемую конфигурацию и зоны  для размещения инстанса.
resource "yandex_compute_instance" "node01" {
  name                      = "node01"
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
      image_id    = "${var.centos-7-base-image}"
      name        = "root-node01-disk"
      type        = "network-nvme"
      size        = "50"
    }
  }


// Create a new net anв subnet . Выбираем планируемый диапазон IP-адресов.
  resource "yandex_vpc_network" "default" {
    name = "net"
  }

  resource "yandex_vpc_subnet" "default" {
    name = "subnet"
    zone           = "ru-central1-a"
    network_id     = "${yandex_vpc_network.default.id}"
    v4_cidr_blocks = ["192.168.101.0/24"]
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.default.id}"
    nat       = true
  }
}

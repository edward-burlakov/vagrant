// Configure the Yandex.Cloud provider
provider "yandex" {
  token                    = "auth_token_here"
  service_account_key_file = "key.json""
  cloud_id                 = "b1g3dtd6rmc18p0kufbd"
  folder_id                = "b1gks5lsfvt1r1gh37ib"
  zone                     = "ru-central1-a"
}

// Create a new instance
resource "yandex_compute_instance" "default" {
  ...
}
provider "yandex" {
  service_account_key_file = "key.json"
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
  zone = "ru-central1-a"
}

// Выбираем используемый образ
resource "yandex_compute_image" "centos7-" {
  name       = "my-centos7-image"
  source_url = "https://storage.yandexcloud.net/lucky-images/kube-it.img"
}

.. ВЫЮиреем палнируюемыю конфигруацию
resource "yandex_compute_instance" "vm" {
  name = "vm-from-custom-image"

  # ...

  boot_disk {
    initialize_params {
      image_id = "${yandex_compute_image.foo-image.id}"
    }
  }
}

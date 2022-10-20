# Заменить на ID своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_cloud_id" {
  default = "b1g3dtd6rmc18p0kufbd"
}

# Заменить на Folder своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_folder_id" {
  default = "b1gks5lsfvt1r1gh37ib"
}

# Заменить на ID своего образа
# ID можно узнать с помощью команды yc compute image list
# либо с помощью команды
# yc compute image list --folder-id standard-images | grep centos-7-v202206

variable "centos7-image" {
  default = "fd88d14a6790do254kj7"
}

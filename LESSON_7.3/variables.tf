# Создаем переменную для хранения  токена
variable "YC_TOKEN" {
  default = "y0_AgAEA7qjbCX2AATuwQAAAADNx-_dP9L62XaATFq3ZDEjDT3hOpl-..."
  // fwo -> ...
}

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

variable "centos7-base-image" {
  default = "fd88d14a6790do254kj7"
}


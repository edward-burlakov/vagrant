# Provider
terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version= ">= 0.78"

  backend "s3" {
    endpoint   = "storage.yandexcloud.net"
    region     = "ru-central1"
    bucket     = "lesson_7_3"
    key        = "<путь к файлу состояния в бакете>/lesson_7_3.tfstate"
    access_key = "YCAJE3QrWRjNZqJIvlbRxDvvL"
    secret_key = "YCMHf3VzH7oMYafuz19cGgDhyAzTN6oz7uc2X98b"

    skip_region_validation      = true
    skip_credentials_validation = true
  }


}


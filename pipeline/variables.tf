variable "account_id" {
  default = ""
}

variable "region" {
  default = ""
}

variable "vpc_id" {
  default = ""
}

variable "security_group_id" {
  default = ""
}

variable "subnets" {
  type = list
  default = []
}

variable "github_repository" {
  default = ""
}


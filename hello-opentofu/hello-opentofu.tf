variable "first_string" {
  description = "The first string to display"
  type        = string
  default     = "Hello"
}

variable "second_string" {
  description = "The second string to display"
  type        = string
  default     = "World"
}

resource "null_resource" "hello" {
  provisioner "local-exec" {
    command = "echo '${var.first_string}'"
  }
}

resource "null_resource" "world" {
  provisioner "local-exec" {
    command = "echo '${var.second_string}'"
  }
}

output "first_output" {
  description = "The first string that was displayed"
  value       = var.first_string
}

output "second_output" {
  description = "The second string that was displayed"
  value       = var.second_string
}
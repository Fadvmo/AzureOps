variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "location" {
  description = "Azure deployment region"
  type        = string
  default     = "canadacentral"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

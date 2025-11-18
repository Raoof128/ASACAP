variable "prefix" {
  description = "Resource prefix"
  type        = string
  default     = "asacap"
}

variable "location" {
  description = "Azure region (Australia East/Southeast)"
  type        = string
  default     = "Australia East"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "staging"
}

variable "tenant_id" {
  description = "Azure AD tenant ID"
  type        = string
}

variable "postgres_admin_login" {
  description = "PostgreSQL admin username"
  type        = string
  default     = "asacapadmin"
}

variable "postgres_admin_password" {
  description = "PostgreSQL admin password"
  type        = string
  sensitive   = true
}

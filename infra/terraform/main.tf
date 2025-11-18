terraform {
  required_version = ">= 1.3.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

locals {
  location = var.location
  prefix   = var.prefix
  tags = {
    environment = var.environment
    project     = "asacap"
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${local.prefix}-rg"
  location = local.location
  tags     = local.tags
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = "${local.prefix}-law"
  location            = local.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.tags
}

resource "azurerm_storage_account" "evidence" {
  name                     = "${local.prefix}evidence"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = local.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  tags                     = local.tags
}

resource "azurerm_key_vault" "main" {
  name                        = "${local.prefix}-kv"
  location                    = local.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = var.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = true
  soft_delete_retention_days  = 90
  enabled_for_disk_encryption = true
  tags                        = local.tags
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${local.prefix}-psql"
  resource_group_name    = azurerm_resource_group.main.name
  location               = local.location
  version                = "14"
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"
  administrator_login    = var.postgres_admin_login
  administrator_password = var.postgres_admin_password
  zone                   = "1"
  backup_retention_days  = 7
  geo_redundant_backup_enabled = false
  tags                   = local.tags
}

resource "azurerm_postgresql_flexible_server_database" "app" {
  name      = "asacap"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_container_registry" "main" {
  name                = "${local.prefix}acr"
  resource_group_name = azurerm_resource_group.main.name
  location            = local.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = local.tags
}

resource "azurerm_container_group" "backend" {
  name                = "${local.prefix}-api"
  location            = local.location
  resource_group_name = azurerm_resource_group.main.name
  ip_address_type     = "Public"
  dns_name_label      = "${local.prefix}-api"
  os_type             = "Linux"
  tags                = local.tags

  container {
    name   = "backend"
    image  = "${azurerm_container_registry.main.login_server}/backend:latest"
    cpu    = 1
    memory = 2

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      DATABASE_URL = "postgresql://${var.postgres_admin_login}:${var.postgres_admin_password}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/asacap"
    }
  }

  diagnostics {
    log_analytics {
      workspace_id = azurerm_log_analytics_workspace.main.workspace_id
      workspace_key = azurerm_log_analytics_workspace.main.primary_shared_key
    }
  }
}

resource "azurerm_dashboard" "compliance" {
  name                = "${local.prefix}-dashboard"
  resource_group_name = azurerm_resource_group.main.name
  location            = local.location
  dashboard_properties = jsonencode({
    lenses = {
      overview = {
        order = 1
        parts = {
          complianceScore = {
            position = {
              x = 0
              y = 0
              colSpan = 12
              rowSpan = 6
            }
            metadata = {
              inputs = []
              type   = "Extension/AppInsightsMetricsLens"
            }
          }
        }
      }
    }
    metadata = {
      model = "v2"
    }
  })
}

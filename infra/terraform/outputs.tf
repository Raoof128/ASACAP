output "resource_group" {
  value = azurerm_resource_group.main.name
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}

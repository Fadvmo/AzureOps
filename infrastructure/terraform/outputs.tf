output "resource_group_name" {
  value = azurerm_resource_group.azureops.name
}

output "virtual_network_name" {
  value = azurerm_virtual_network.azureops.name
}

output "subnet_name" {
  value = azurerm_subnet.app.name
}

output "network_security_group_name" {
  value = azurerm_network_security_group.app.name
}

output "storage_account_name" {
  value = azurerm_storage_account.azureops.name
}

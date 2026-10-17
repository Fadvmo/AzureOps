locals {
  tags = {
    project     = "AzureOps"
    environment = var.environment
    managed_by  = "Terraform"
    client      = "Northstar-Consulting-Demo"
  }
}

resource "azurerm_resource_group" "azureops" {
  name     = "rg-azureops-dev"
  location = var.location
  tags     = local.tags
}

resource "azurerm_virtual_network" "azureops" {
  name                = "vnet-azureops-dev"
  location            = azurerm_resource_group.azureops.location
  resource_group_name = azurerm_resource_group.azureops.name
  address_space       = ["10.20.0.0/16"]
  tags                = local.tags
}

resource "azurerm_subnet" "app" {
  name                            = "snet-azureops-app"
  resource_group_name             = azurerm_resource_group.azureops.name
  virtual_network_name            = azurerm_virtual_network.azureops.name
  address_prefixes                = ["10.20.1.0/24"]
  default_outbound_access_enabled = false
}

resource "azurerm_network_security_group" "app" {
  name                = "nsg-azureops-app"
  location            = azurerm_resource_group.azureops.location
  resource_group_name = azurerm_resource_group.azureops.name
  tags                = local.tags

  security_rule {
    name                       = "DenyInternetInbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}

resource "random_string" "storage_suffix" {
  length  = 8
  lower   = true
  upper   = false
  numeric = true
  special = false
}

resource "azurerm_storage_account" "azureops" {
  name                     = "stazureops${random_string.storage_suffix.result}"
  resource_group_name      = azurerm_resource_group.azureops.name
  location                 = azurerm_resource_group.azureops.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  min_tls_version                 = "TLS1_2"
  https_traffic_only_enabled      = true
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = false
  shared_access_key_enabled       = false

  tags = local.tags

  blob_properties {
    delete_retention_policy {
      days = 7
    }
  }
}

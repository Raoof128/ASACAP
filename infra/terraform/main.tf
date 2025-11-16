terraform {
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

resource "azurerm_resource_group" "soci_rg" {
  name     = "soci-compliance-platform-rg"
  location = "Australia East"
}

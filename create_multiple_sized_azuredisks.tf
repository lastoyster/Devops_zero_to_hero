# Example 1: Creating a virtual machine for each VM size
  
variable "vm_sizes" {
  type    = list(string)
  default = ["Standard_B1s", "Standard_B2ms", "Standard_B4ms"]
}

resource "azurerm_linux_virtual_machine" "main" {
  count                 = length(var.vm_sizes)
  name                  = "example-vm-${count.index}"
  location              = "East US"
  resource_group_name   = var.rg_name
  network_interface_ids = [azurerm_network_interface.main.id]
  size                  = var.vm_sizes[count.index]
  admin_username        = "adminuser"
  admin_password        = "adminpass"

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
}

# Example 2: Creating multiple disks based on the number of disk sizes listedCreating multiple disks based on the number of disk sizes listed
variable "vm_sizes" {
  type    = list(string)
  default = ["Standard_B1s", "Standard_B2ms", "Standard_B4ms"]
}

resource "azurerm_linux_virtual_machine" "main" {
  count                 = length(var.vm_sizes)
  name                  = "example-vm-${count.index}"
  location              = "East US"
  resource_group_name   = var.rg_name
  network_interface_ids = [azurerm_network_interface.main.id]
  size                  = var.vm_sizes[count.index]
  admin_username        = "adminuser"
  admin_password        = "adminpass"

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
}

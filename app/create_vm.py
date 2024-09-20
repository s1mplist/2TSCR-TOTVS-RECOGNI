import os

# Define your parameters
vm_name = "vm-gpu-recogni"
resource_group = "recogni-resource-group"
image = "Ubuntu2204"
vm_size = "Standard_NC6s_v3"
username = "recogni-user"
password = "Senhaadmin123!"
accelerated_networking = "true"
nsg_rule = "SSH"
nsg = "recogni-nsg-vm-gpu"
vnet_name = "vnet-vm-gpu"
subnet = "private-subnet"

# Create the VM
os.system(f"az vm create --name {vm_name} --resource-group {resource_group} --image {image} --size {vm_size} --admin-username {username} --admin-password {password} --accelerated-networking {accelerated_networking} --nsg-rule {nsg_rule} --nsg {nsg} --vnet-name {vnet_name} --subnet {subnet}")
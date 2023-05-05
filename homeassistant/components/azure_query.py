from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient

# sample from my accessTokens.json
"""
[
  {
      "tokenType": "Bearer",
      "expiresIn": 189302400,
      "expiresOn": "2029-05-03 23:59:59.999999",
      "resource": "https://management.core.windows.net/",
      "accessToken": "eyJ0eXAiOiI4aU9TXzA5RDI12jZqbWx4dHp3QUx4Q2swZ2dYU2FmU0xJbXlPbFpHb0xZd1J1UmpCazNFSzB2Q2d0enFxcTNiZGFj",
      "refreshToken": "AQABAAAAAAG9XpTzGjRl0sI423VlA3OxQ2hrkWYVzjv3e9vn3rM2n1WfV7JvNjNpV7DfRwYJp8HvGuvfXnREURlgg5df5Jk50Qn",
      "identityProvider": "downsideup.invalid",
      "userId": "downsideup@downsideup.invalid",
      "isMRRT": true,
      "_clientId": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
      "_authority": "https://login.microsoftonline.com/common"
  }
]
"""

# sample from my azureProfile.json

"""
{
  "subscriptions": [
    {
      "id": "df62f6b9-6d2a-40e1-97b1-7bba195e4708",
      "name": "downsideup_sub",
      "state": "Enabled",
      "user": {
        "name": "downsideup@downsideup.invalid",
        "type": "user"
      },
      "isDefault": true,
      "tenantId": "89f7499d-6ad0-4d17-96e0-56e4985c2fdd",
      "environmentName": "AzureCloud"
    }
  ],
  "installationId": "1de3b9db-5e5b-48a5-81e5-7eafe2d2bace"
}
"""

# Replace these values with your own credentials
tenant_id = "YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
subscription_id = "YOUR_SUBSCRIPTION_ID"

# Authenticate using the provided credentials
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

# Create a ComputeManagementClient instance
compute_client = ComputeManagementClient(credential, subscription_id)

# Create a ResourceManagementClient instance
resource_client = ResourceManagementClient(credential, subscription_id)

# List all resource groups in the subscription
resource_groups = resource_client.resource_groups.list()

# Iterate through the resource groups and list running VMs
for rg in resource_groups:
    vms = compute_client.virtual_machines.list(rg.name)
    for vm in vms:
        vm_instance_view = compute_client.virtual_machines.instance_view(rg.name, vm.name)
        vm_status = vm_instance_view.statuses[-1].display_status

        if vm_status == "VM running":
            print(f"VM Name: {vm.name}, Resource Group: {rg.name}, Status: {vm_status}")



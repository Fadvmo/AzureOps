import os

from azure.identity import AzureCliCredential
from azure.mgmt.resource.resources import ResourceManagementClient

subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

if not subscription_id:
    raise SystemExit(
        "AZURE_SUBSCRIPTION_ID is not set."
    )

credential = AzureCliCredential()

client = ResourceManagementClient(
    credential,
    subscription_id
)

print("Connected to Azure successfully!")
print("\nResource Groups:")

for group in client.resource_groups.list():
    print(f" - {group.name} ({group.location})")

import os
import json
from datetime import datetime, timezone

from azure.identity import AzureCliCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient


RESOURCE_GROUP = "rg-azureops-dev"
STORAGE_ACCOUNT = "stazureopsyfhwohr6"
NSG_NAME = "nsg-azureops-app"
VNET_NAME = "vnet-azureops-dev"
SUBNET_NAME = "snet-azureops-app"

subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

if not subscription_id:
    raise SystemExit("ERROR: AZURE_SUBSCRIPTION_ID is missing.")

credential = AzureCliCredential()

storage_client = StorageManagementClient(
    credential, subscription_id
)

network_client = NetworkManagementClient(
    credential, subscription_id
)

findings = []


def check(check_id, name, condition, severity, evidence):
    result = {
        "id": check_id,
        "name": name,
        "status": "PASS" if condition else "FAIL",
        "severity": severity,
        "evidence": evidence
    }

    findings.append(result)

    symbol = "[PASS]" if condition else "[FAIL]"
    print(f"{symbol} {check_id}: {name}")


print("=" * 60)
print("AZUREOPS CLOUD SECURITY AUDITOR")
print("=" * 60)

print("\nConnecting to Azure resources...")

storage = storage_client.storage_accounts.get_properties(
    RESOURCE_GROUP,
    STORAGE_ACCOUNT
)

nsg = network_client.network_security_groups.get(
    RESOURCE_GROUP,
    NSG_NAME
)

subnet = network_client.subnets.get(
    RESOURCE_GROUP,
    VNET_NAME,
    SUBNET_NAME
)

print("\nRunning security checks...\n")

# AZ-001: TLS minimum version
tls = storage.minimum_tls_version
tls_value = getattr(tls, "value", tls)
tls_value = str(tls_value or "")

check(
    "AZ-001",
    "Storage requires TLS 1.2 or higher",
    tls_value.upper() in ("TLS1_2", "TLS1_3"),
    "HIGH",
    f"Configured minimum TLS: {tls_value}"
)

# AZ-002: HTTPS-only traffic
https_only = storage.enable_https_traffic_only is True

check(
    "AZ-002",
    "Storage enforces HTTPS-only traffic",
    https_only,
    "HIGH",
    f"HTTPS only: {storage.enable_https_traffic_only}"
)

# AZ-003: Public network access
public_network = storage.public_network_access
public_network_value = getattr(
    public_network, "value", public_network
)
public_network_value = str(public_network_value or "")

check(
    "AZ-003",
    "Storage public network access is disabled",
    public_network_value.lower() == "disabled",
    "HIGH",
    f"Public network access: {public_network_value}"
)

# AZ-004: Shared-key authentication
shared_keys = storage.allow_shared_key_access

check(
    "AZ-004",
    "Shared-key authentication is disabled",
    shared_keys is False,
    "MEDIUM",
    f"Shared-key access: {shared_keys}"
)

# AZ-005: Public blob access
public_blobs = storage.allow_blob_public_access

check(
    "AZ-005",
    "Public blob access is disabled",
    public_blobs is False,
    "CRITICAL",
    f"Public blob access: {public_blobs}"
)

# AZ-006: NSG association
subnet_nsg_id = (
    subnet.network_security_group.id
    if subnet.network_security_group
    else None
)

nsg_associated = (
    subnet_nsg_id is not None
    and subnet_nsg_id.lower() == nsg.id.lower()
)

check(
    "AZ-006",
    "Subnet is associated with the expected NSG",
    nsg_associated,
    "MEDIUM",
    f"Associated NSG: {subnet_nsg_id}"
)
# AZ-007: Explicit inbound internet deny rule

def normalize(value):
    return str(getattr(value, "value", value) or "").lower()


deny_rules = []

for rule in nsg.security_rules or []:
    direction = normalize(rule.direction)
    access = normalize(rule.access)
    source = normalize(rule.source_address_prefix)
    protocol = normalize(rule.protocol)
    destination_port = normalize(rule.destination_port_range)

    if (
        direction == "inbound"
        and access == "deny"
        and source == "internet"
        and protocol == "*"
        and destination_port == "*"
    ):
        deny_rules.append(rule.name)

check(
    "AZ-007",
    "Explicit inbound internet deny rule exists",
    len(deny_rules) > 0,
    "HIGH",
    f"Matching deny rules: {deny_rules}"
)
# Generate JSON report
passed = sum(
    1 for finding in findings
    if finding["status"] == "PASS"
)

failed = len(findings) - passed

report = {
    "project": "AzureOps",
    "client": "Northstar Consulting Group (Fictional)",
    "assessment_date": datetime.now(timezone.utc).isoformat(),
    "resource_group": RESOURCE_GROUP,
    "summary": {
        "total_checks": len(findings),
        "passed": passed,
        "failed": failed
    },
    "findings": findings
}

os.makedirs("reports", exist_ok=True)

report_path = "reports/security_assessment.json"

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("\n" + "=" * 60)
print("SECURITY ASSESSMENT SUMMARY")
print("=" * 60)

print(f"Total checks: {len(findings)}")
print(f"Passed:       {passed}")
print(f"Failed:       {failed}")
print(f"\nJSON report saved: {report_path}")

if failed:
    print("\nWARNING: Security findings require review.")
else:
    print("\nAll configured security checks passed.")

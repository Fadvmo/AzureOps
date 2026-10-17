# AzureOps — Cloud Infrastructure & Security Automation

**Microsoft Azure | Terraform | Python | GitHub Actions | Checkov | Cloud Security**

AzureOps is a hands-on cloud engineering project demonstrating the deployment, management, security assessment, and automation of Microsoft Azure infrastructure.

The project simulates a cloud consulting engagement for **Northstar Consulting Group**, a fictional organization seeking to standardize its cloud infrastructure, improve security configurations, and introduce automated validation into its development workflow.

AzureOps combines Infrastructure as Code (IaC), Python-based security auditing, Azure networking, configuration drift detection, and CI/CD automation.

## Project Objectives

- Deploy repeatable Azure infrastructure using Terraform.
- Implement secure cloud networking and storage configurations.
- Develop Python automation to assess Azure security settings.
- Generate JSON and HTML security assessment reports.
- Detect and remediate infrastructure configuration drift.
- Integrate Terraform validation and security scanning into GitHub Actions.
- Document technical decisions, security findings, and operational improvements.

## Technology Stack

| Technology | Purpose |
|---|---|
| Microsoft Azure | Cloud infrastructure and resource management |
| Terraform | Infrastructure provisioning and configuration management |
| Python | Automated security auditing and report generation |
| Azure SDK for Python | Retrieving live Azure resource configurations |
| Azure CLI | Cloud administration and configuration verification |
| Git and GitHub | Source control and project collaboration |
| GitHub Actions | Continuous integration and automated validation |
| Checkov | Infrastructure as Code security scanning |
| Linux (Ubuntu) | Development and automation environment |

## Cloud Architecture

The environment includes:

- **Azure Resource Group:** Organizes project resources.
- **Azure Virtual Network:** Provides an isolated virtual network.
- **Azure Subnet:** Defines the application network segment.
- **Network Security Group:** Controls inbound network traffic.
- **Azure Storage Account:** Provides secured cloud storage infrastructure.
- **Python Security Auditor:** Evaluates deployed Azure resource configurations.
- **GitHub Actions:** Validates Terraform code and performs security scans.

### Infrastructure Configuration

| Resource | Configuration |
|---|---|
| Azure Region | Canada Central |
| Virtual Network | 10.20.0.0/16 |
| Application Subnet | 10.20.1.0/24 |
| Network Security Group | Explicit inbound Internet deny rule |
| Storage Account | Standard LRS |
| Minimum TLS Version | TLS 1.2 |
| HTTPS Enforcement | Enabled |
| Public Network Access | Disabled |
| Shared-Key Authentication | Disabled |
| Public Blob Access | Disabled |
| Blob Soft-Delete | Enabled, 7-day retention |

The environment is designed as a limited, low-cost technical demonstration rather than a production deployment.

## Infrastructure as Code

Terraform manages the Azure infrastructure through version-controlled configuration files.

The project demonstrates:

- Declarative infrastructure provisioning.
- Reusable configuration through Terraform variables.
- Resource dependency management.
- Infrastructure state management.
- Configuration drift detection.
- Controlled infrastructure updates.

Terraform formatting and validation are also included in the automated CI workflow.

## Python Cloud Security Auditor

A custom Python security auditor connects to Microsoft Azure using the Azure SDK and evaluates deployed resources against seven project-defined security checks.

| Check ID | Security Control |
|---|---|
| AZ-001 | Storage requires TLS 1.2 or higher |
| AZ-002 | HTTPS-only traffic is enforced |
| AZ-003 | Public network access is disabled |
| AZ-004 | Shared-key authentication is disabled |
| AZ-005 | Public blob access is disabled |
| AZ-006 | Expected Network Security Group is associated with the subnet |
| AZ-007 | Explicit inbound Internet deny rule exists |

### Assessment Results

**Final assessment: 7 passed, 0 failed.**

The auditor generates machine-readable JSON output, while a separate report generator produces an HTML security assessment with an executive summary, findings, supporting evidence, and recommendations.

These results reflect the seven implemented checks and do not represent a comprehensive Azure security audit.

## Security Misconfiguration and Remediation

AzureOps includes a controlled security misconfiguration exercise to demonstrate cloud security monitoring and Infrastructure as Code remediation.

### Scenario

HTTPS-only enforcement was temporarily disabled on a demonstration Azure Storage Account while public network access remained disabled.

### Workflow

1. Establish a secure baseline.
2. Introduce a controlled configuration change using Azure CLI.
3. Execute the Python security auditor.
4. Capture the security assessment.
5. Restore the intended configuration.
6. Rerun the auditor to verify remediation.

### Outcome

The final Azure configuration was verified with HTTPS-only enforcement enabled and all seven custom security checks passing.

This exercise demonstrates practical experience with cloud configuration assessment, security troubleshooting, and remediation verification.

## CI/CD Automation

GitHub Actions provides automated validation whenever changes are pushed to the main branch or submitted through pull requests.

The workflow performs:

**Terraform Validation**
- Terraform formatting checks.
- Terraform initialization without configuring a remote backend.
- Terraform configuration validation.

**Infrastructure Security Scanning**
- Checkov static analysis of Terraform configuration.
- Identification of infrastructure security findings.
- Reporting of passed, failed, and skipped checks.

The CI workflow does not automatically deploy Azure resources.

### Checkov Security Scan Results

| Metric | Initial Scan | Updated Scan |
|---|---:|---:|
| Passed | 16 | 17 |
| Failed | 5 | 4 |
| Skipped | 0 | 0 |

The updated scan followed the implementation of Azure Storage blob soft-delete.

The remaining findings involve queue logging, storage replication requirements, private endpoints, and customer-managed encryption keys.

These findings remain documented for future evaluation. The demonstration uses a low-cost configuration and does not claim to meet every production security requirement.

Checkov currently runs in reporting mode using `--soft-fail`, allowing findings to be reviewed without automatically blocking the pipeline.

## Project Structure

```text
AzureOps/
├── .github/
│   └── workflows/
│       └── terraform-ci.yml
├── infrastructure/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── versions.tf
│       └── .terraform.lock.hcl
├── security-auditor/
│   ├── auditor.py
│   ├── generate_report.py
│   └── test_connection.py
├── .gitignore
└── README.md
```

Terraform state files, credentials, virtual environments, and generated reports are excluded from source control.

## Technical Challenges and Solutions

### Azure Authentication and Provider Configuration

Configured Azure CLI authentication and Terraform provider settings to support infrastructure management with restricted storage access.

### Python SDK Compatibility

Resolved Azure SDK import and enumeration differences encountered while implementing the resource assessment logic.

### Infrastructure Drift Detection

Used Terraform to compare deployed Azure configurations with the intended Infrastructure as Code definitions.

### Security Findings and Remediation

Reviewed Checkov findings and implemented seven-day blob soft-delete retention as an additional data protection control.

### Continuous Integration

Integrated GitHub Actions to automatically validate Terraform configuration and run infrastructure security scans.

## Future Enhancements

- Introduce Azure Bicep templates for alternative infrastructure provisioning.
- Expand Python auditing to include additional Azure security controls.
- Add automated unit tests for security assessment logic.
- Implement private endpoints and private DNS integration.
- Integrate Azure Monitor and Log Analytics.
- Evaluate stronger storage replication and customer-managed encryption.
- Introduce policy-based CI security gates.
- Explore Azure DevOps pipelines for an alternative CI/CD implementation.

## Project Scope

AzureOps is an independent technical portfolio project developed for hands-on learning and demonstration.

Northstar Consulting Group is a fictional client used to provide a realistic consulting scenario. No production client infrastructure or data is involved.

The project demonstrates foundational cloud engineering, infrastructure automation, security assessment, and DevOps practices.

---

**Repository:** https://github.com/Fadvmo/AzureOps

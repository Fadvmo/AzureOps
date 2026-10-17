import json
from pathlib import Path
from datetime import datetime
from html import escape

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "reports/security_assessment.json"
HTML_PATH = BASE_DIR / "reports/security_assessment.html"

with open(JSON_PATH, encoding="utf-8") as file:
    report = json.load(file)

summary = report["summary"]
findings = report["findings"]

total = summary["total_checks"]
passed = summary["passed"]
failed = summary["failed"]

score = round((passed / total) * 100) if total else 0

recommendations = {
    "AZ-001": "Configure minimum TLS version to TLS 1.2 or higher.",
    "AZ-002": "Require HTTPS traffic for the storage account.",
    "AZ-003": "Disable public network access unless explicitly required.",
    "AZ-004": "Disable shared-key authentication and use Microsoft Entra ID.",
    "AZ-005": "Disable anonymous public blob access.",
    "AZ-006": "Associate the subnet with the approved network security group.",
    "AZ-007": "Review inbound NSG rules and enforce appropriate restrictions."
}

rows = ""

for finding in findings:
    status = finding["status"]
    status_class = "pass" if status == "PASS" else "fail"

    rows += f"""
    <tr>
        <td>{escape(finding['id'])}</td>
        <td>{escape(finding['name'])}</td>
        <td><span class="{status_class}">{escape(status)}</span></td>
        <td>{escape(finding['severity'])}</td>
        <td>{escape(str(finding['evidence']))}</td>
        <td>{escape(recommendations.get(finding['id'], 'Review configuration.'))}</td>
    </tr>
    """

assessment_date = datetime.fromisoformat(
    report["assessment_date"].replace("Z", "+00:00")
).strftime("%B %d, %Y %H:%M UTC")

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AzureOps Security Assessment</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f3f6fb;
    color: #1c2938;
}}

header {{
    background: #10243a;
    color: white;
    padding: 45px 8%;
}}

header h1 {{
    margin: 0 0 12px;
    font-size: 32px;
}}

header p {{
    color: #c4d3e5;
}}

main {{
    max-width: 1250px;
    margin: 35px auto;
    padding: 0 20px;
}}

section {{
    background: white;
    padding: 28px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.05);
}}

h2 {{
    margin-top: 0;
    color: #10243a;
}}

.metrics {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
}}

.metric {{
    background: #edf3fa;
    padding: 22px;
    border-radius: 10px;
    text-align: center;
}}

.metric strong {{
    display: block;
    font-size: 32px;
    margin-bottom: 8px;
}}

.metric span {{
    color: #536477;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th, td {{
    padding: 14px;
    border-bottom: 1px solid #e4e9ef;
    text-align: left;
    vertical-align: top;
    overflow-wrap: anywhere;
}}

th {{
    background: #edf3fa;
}}

.pass {{
    color: #147d43;
    font-weight: bold;
}}

.fail {{
    color: #c12b2b;
    font-weight: bold;
}}

.table-wrapper {{
    overflow-x: auto;
}}

footer {{
    text-align: center;
    padding: 25px;
    color: #64748b;
    font-size: 12px;
}}

@media (max-width: 700px) {{
    .metrics {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media print {{
    body {{
        background: white;
    }}

    section {{
        box-shadow: none;
        border: 1px solid #ddd;
    }}
}}
</style>
</head>

<body>

<header>
    <h1>AzureOps | Cloud Security Assessment</h1>
    <p>Infrastructure Security & Configuration Review</p>
    <p>Client: {escape(report['client'])}</p>
    <p>Assessment Date: {escape(assessment_date)}</p>
</header>

<main>

<section>
    <h2>Executive Summary</h2>

    <p>
    This assessment evaluates selected security configurations
    across the AzureOps demonstration environment.
    The checks use live Azure management API data.
    </p>

    <p>
    The assessment covers storage transport security,
    public access restrictions, authentication settings,
    and selected network security controls.
    </p>

    <p>
    Results represent the seven defined project checks,
    not a comprehensive Azure security certification.
    </p>
</section>

<section>
    <h2>Security Assessment Overview</h2>

    <div class="metrics">
        <div class="metric">
            <strong>{score}%</strong>
            <span>Checks Passed</span>
        </div>

        <div class="metric">
            <strong>{total}</strong>
            <span>Total Checks</span>
        </div>

        <div class="metric">
            <strong>{passed}</strong>
            <span>Passed</span>
        </div>

        <div class="metric">
            <strong>{failed}</strong>
            <span>Failed</span>
        </div>
    </div>
</section>

<section>
    <h2>Security Findings</h2>

    <div class="table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Security Control</th>
                    <th>Status</th>
                    <th>Severity</th>
                    <th>Evidence</th>
                    <th>Remediation Recommendation</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
</section>

<section>
    <h2>Assessment Scope</h2>

    <p><strong>Resource Group:</strong>
    {escape(report['resource_group'])}</p>

    <p><strong>Assessment Method:</strong>
    Automated Azure SDK configuration inspection</p>

    <p><strong>Environment:</strong>
    AzureOps development demonstration</p>

    <p><strong>Limitations:</strong>
    This assessment checks specific configurations.
    It does not perform penetration testing, traffic analysis,
    or comprehensive effective-access evaluation.</p>
</section>

</main>

<footer>
    AzureOps | Northstar Consulting Group — Fictional Client Scenario
</footer>

</body>
</html>
"""

HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
HTML_PATH.write_text(html, encoding="utf-8")

print("=" * 55)
print("AZUREOPS HTML REPORT GENERATOR")
print("=" * 55)
print(f"Security score: {score}%")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Report generated: {HTML_PATH}")

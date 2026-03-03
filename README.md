Markdown
# AAA — Autonomy, Algorithms & Agency

## AI-Assisted Civic Infrastructure for Strengthening Democratic Autonomy

**AAA (Autonomy, Algorithms & Agency)** is a hybrid civic-tech infrastructure prototype designed to assess and strengthen the democratic autonomy of community-based organizations.

This system integrates:
- Structured data collection.
- Rule-based classification.
- AI-assisted diagnostics.
- Machine-readable JSON outputs.

Developed by **Corporación ASFINDES / Vita'e Plena** in Medellín, Colombia.

---

## System Architecture

```mermaid
graph TD
    A[Data] --> B[Normalization]
    B --> C[Analysis]
    C --> D[AI Module]
    D --> E[JSON Output]
    E --> F[Reports]
Prototype Capabilities
Ingesting organizational metrics CSV files.

Normalizing data and calculating composite indices.

Classifying structural risks via rules.

Generating multi-dimensional governance diagnostics.

Providing strategic recommendations per organization.

Producing JSON outputs suitable for integration.

How to Run the Prototype
Clone: git clone https://github.com/CorpAsfindes/AAA-Autonomy-Algorithms-Agency.git

Install: pip install -r requirements.txt

Run: python sistema_aaa.py

Tests: pytest tests/

Repository Structure
/data: Raw pilot datasets.

/examples: Sample CSV and JSON.

/tests: Automated test suite.

sistema_aaa.py: Core logic.

requirements.txt: Dependencies.

License
This project is licensed under the MIT License.

Developed by Corporación ASFINDES / Vita'e Plena - Medellín, Colombia.

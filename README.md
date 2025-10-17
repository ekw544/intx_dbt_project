# 🧠 Interactions Evidence Project (intx_dbt)

This project uses **dbt** (data build tool) with a local **SQLite** database to model, transform, and analyze simulated interaction data. It’s designed as a foundation for future integrations with de-identified real data and more advanced analytics pipelines.

This project analyzes the nature and evolution of interactions over time.

## Project Overview

The goal is to understand:
- The frequency and categories of interactions
- How interactions change over time
- Key factors influencing their patterns

ChatGPT (AI Co-Pilot): Served as a sounding board for project design, tool selection, and problem-solving. Helped structure the project for portfolio readiness while ensuring data privacy and alignment with real-world analytics workflows.

## Tech Stack
- **dbt (Core)**
- **SQLite**
- **Python**
- **VS Code**

## Data
For privacy reasons, all data in this repository is **simulated** or **de-identified**. The raw dataset is sensitive and not included.

- **Simulated inputs**: `data/simulated_interactions.csv` (safe, local) 

**Note on Data:** The CSV files included here are fully de-identified and pseudonymized. No real names, locations, or notes are included. They are for demonstration purposes only.
- **De-identified outputs**:  
  - `data/interactions_deid.csv` — pseudonymized interactions  
  - `data/interaction_person.csv` — interaction-person links for reproducible analysis 
  - `data/persons.csv` — mapping of pseudonyms  



---

## 📁 Project Structure

```
intx_project/
│
├── data/
│ ├── demo_interactions_deid.csv # Pseudonymized interactions
│ ├── demo_interaction_person.csv # Interaction-person mapping table
│ ├── demo_persons.csv # Pseudonym mapping table
│ ├── simulated_interactions.csv # Sample dataset (local only, safe & simulated) 
│
├── scripts/
│ ├── generate_simulated_data.py
│ ├── deidentify_interactions.py
│
├── intx_dbt/ # dbt project folder
│ ├── models/
│ │ ├── staging/ # Source staging models (stg_*)
│ │ ├── facts/ # Aggregated fact tables (fct_*)
│ │ └── example/ # dbt tutorial models
│ ├── macros/
│ ├── dbt_project.yml
│
├── .gitignore
└── README.md # ← You are here
```

---

## 🧰 Environment Setup (local, safe)

1. **Create and activate a conda environment (recommended)**

   ```bash
   conda create -n dbt_env python=3.12
   conda activate dbt_env
    ```
2. **Install dbt with SQLite adapter and helpers**
    ```
    pip install dbt-core dbt-sqlite faker pandas
    ```
3. **Verify installation**
    ```
    python --version
    dbt --version
    ```
---

## 🧩 Local Database

- The local SQLite database (e.g. intx.db) should remain local and never be committed.
- Your profiles.yml (in ~/.dbt/profiles.yml) should reference the absolute path to your local .db and be kept private.

Example path in profiles.yml:
```
intx_dbt:
  outputs:
    dev:
      type: sqlite
      threads: 1
      database: ~/intx_project/intx.db
      schema: main
      schemas_and_paths:
        main: ~/intx_project/intx.db
      schema_directory: ~/intx_project
  target: dev
```
---

## 🧮 Running dbt

After setup, run these commands inside the intx_dbt folder:
```
cd intx_dbt
dbt debug           # confirm connection to local sqlite
dbt run             # build models
dbt test            # run schema/tests
dbt docs generate   # generate docs
dbt docs serve      # view docs locally
```

---

## 🧠 Models / Pipeline Overview

- Raw data is **cleaned and preprocessed**:
  - Names in `Parties` are cleaned and split
  - Uncertain names and text inside parentheses are removed
- Names are then **pseudonymized consistently** across `Parties` and `Proof` columns
- `Proof` text category words are normalized to canonical forms for consistent aggregation
- De-identified outputs and mapping tables are generated for safe use in dbt models

| Layer                    | Model                      | Description                                                     |
| ------------------------ | -------------------------- | --------------------------------------------------------------- |
| **Staging**              | `stg_interactions`         | Loads and cleans raw simulated data (from CSV import)           |
| **Facts / Aggregates**   | `fct_interactions_summary` | Aggregated metrics (counts, averages, date ranges) by category  |
| **Example**              | `my_first_dbt_model`       | Default dbt example model (safe to delete later)                |

---

## 🔒 Privacy and De-identification

This project uses simulated data only for testing and modeling purposes.
When integrating real data:
- Remove all personally identifiable information (PII)
- Use consistent pseudonymization
- Store sensitive source data in a private folder outside the Git repository
- Never push .db, raw data files, or profiles.yml (if it contains real credentials or local paths) to GitHub

---

## 📤 Git & Sharing

- Push only non-sensitive artifacts: models, docs, simulated data, notebooks, READMEs.
- The .gitignore ensures private and auto-generated files (like databases and virtual environments) are excluded.

---

## 🚀 Next Steps

- Add a short technical write-up describing the business problem and approach.
- Include screenshots or embedded Tableau/Power BI/Streamlit demos (linked, not containing PII).
- Add a notebooks/ folder with exploratory analysis (Jupyter) using simulated data.
- Add dbt docs output and a short data model diagram to the repo.

---

## 👩‍💻 Author

- **Name:** EKW544  
- **Project:** Interactions Evidence Project  
- **Stack:** dbt, SQLite, Miniconda, VS Code
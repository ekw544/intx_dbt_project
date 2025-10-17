import pandas as pd
import hashlib
from faker import Faker
from pathlib import Path
import re

# --- Paths ---
input_path = Path("data/simulated_interactions.csv")
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

private_input_path = Path("private_data/interactions.csv")
private_output_dir = Path("private_data")
private_output_dir.mkdir(exist_ok=True)

# --- Load raw data ---
df = pd.read_csv(input_path)

# --- Drop unused PII columns ---
drop_columns = ["Notes", "Transportation", "Location", "Event"]
df = df.drop(columns=[c for c in drop_columns if c in df.columns])

# --- Initialize Faker ---
fake = Faker()

# --- Helper functions ---
def hash_name(name):
    return hashlib.sha256(str(name).encode("utf-8")).hexdigest()

def deterministic_pseudonym(name_hash):
    seed_int = int(name_hash[:8], 16)
    fake.seed_instance(seed_int)
    return fake.first_name()

def clean_names(raw_string):
    if pd.isnull(raw_string):
        return[]
    # Remove parentheses and what's inside
    val = re.sub(r"\s*\(.*?\)", "", raw_string)
    # Split by commas and drop uncertain names
    names = [n.strip() for n in val.split(",") if n.strip() and not n.endswith("?")]
    return names

# --- Step 0: Preprocess names in Parties ---
df["Parties_clean"] = df["Parties"].apply(lambda x: ", ".join(clean_names(x)))

# --- Step 1: Build mapping of all unique names ---
all_names = set()

# Add names from Parties
for val in df["Parties_clean"].dropna():
    all_names.update([n.strip() for n in val.split(",") if n.strip()])

# Optionally: extract names from Proof column if it contains names
# Here we assume names in Proof are exactly as in Parties for simplicity
# If more names can appear, extract them similarly and add to all_names

mapping = pd.DataFrame({"real_name": list(all_names)})
mapping["hashed_id"] = mapping["real_name"].apply(hash_name)
mapping["fake_name"] = mapping["hashed_id"].apply(deterministic_pseudonym)
mapping["person_id"] = range(1, len(mapping) + 1)

persons_df = mapping[["person_id", "fake_name"]].rename(columns={"fake_name": "person_name"})

# --- Step 2: Pseudonymize Parties in interactions ---
def pseudonymize_parties(parties_str, mapping):
    names = clean_names(parties_str)
    pseudonyms = []
    for n in names:
        match = mapping.loc[mapping["real_name"] == n, "fake_name"]
        if not match.empty:
            pseudonyms.append(match.values[0])
    return ", ".join(pseudonyms)

df["Parties_pseudo"] = df["Parties"].apply(lambda x: pseudonymize_parties(x, mapping))

# --- Step 3: Pseudonymize Proof column consistently, normalize capitalization ---
def pseudonymize_proof(text, mapping):
    if pd.isnull(text) or str(text).strip() == "":
        return ""
    
    text_str = str(text)

    # Replace all real names with their fake names
    for real_name, fake_name in zip(mapping["real_name"], mapping["fake_name"]):
        pattern = r"\b" + re.escape(real_name) + r"\b"
        text_str = re.sub(pattern, fake_name, text_str)

    # Map category words to canonical forms
    category_map = {
        "text": "text",
        "texts": "text",
        "call": "call",
        "phone": "call",
        "pictures": "pictures"
    }

    # Replace any category word with its canonical form
    pattern = r"\b(" + "|".join(category_map.keys()) + r")\b"
    def replace_with_canonical(match):
        return category_map[match.group(0).lower()]

    text_str = re.sub(pattern, replace_with_canonical, text_str, flags=re.IGNORECASE)

    return text_str
    
# Apply function
df["Proof_pseudo"] = df["Proof"].apply(lambda x: pseudonymize_proof(x, mapping))

# --- Step 4: Build interaction_person table ---
records = []
for i, row in df.iterrows():
    for name in clean_names(row["Parties"]):
        match = mapping.loc[mapping["real_name"] == name, "person_id"]
        if not match.empty:
            records.append({"interaction_id": i + 1, "person_id": match.values[0]})

interaction_person_df = pd.DataFrame(records)

# --- Step 5: Add interaction_id and Final de-identified DataFrame ---
df["interaction_id"] = range(1, len(df) + 1)
# Drop original PII columns
df_deid = df.drop(columns=["Parties", "Proof", "Parties_clean"])
# Keep pseudonymized versions only
df_deid = df_deid.rename(columns={"Parties_pseudo": "Parties", "Proof_pseudo": "Proof"})
del df # Remove the original PII DataFrame from memory

# --- Step 5.1 Save private mapping (optional, local only) ---
# private_mapping_dir = Path("private_data/mappings")
# private_mapping_dir.mkdir(parents=True, exist_ok=True)
# mapping.to_csv(private_mapping_dir / "real_to_fake_persons.csv", index=False)
# print("   - private_data/mappings/real_to_fake_persons.csv (private)")
del mapping # Remove mapping PII DataFrame from memory

# --- Step 6: Preview transformed data ---
print("Preview of de-identified interactions:")
print(df_deid.columns.tolist())
print(df_deid.head(10))
print(persons_df.head(10))
print(interaction_person_df.head(10))

# --- Step 7: Save outputs ---

# For local private data
# df_deid.to_csv(private_output_dir / "interactions_deid.csv", index=False)
# persons_df.to_csv(private_output_dir / "persons.csv", index=False)
# interaction_person_df.to_csv(private_output_dir / "interaction_person.csv", index=False)

# print("All private de-identified tables saved:")
# print("   - private_data/persons.csv")
# print("   - private_data/interactions_deid.csv")
# print("   - private_data/interaction_person.csv")

# For GitHub portfolio/demo purposes (optional)
df_deid.to_csv(output_dir / "demo_interactions_deid.csv", index=False)
persons_df.to_csv(output_dir / "demo_persons.csv", index=False)
interaction_person_df.to_csv(output_dir / "demo_interaction_person.csv", index=False)

print("All demo de-identified tables saved:")
print("   - data/demo_persons.csv")
print("   - data/demo_interactions_deid.csv")
print("   - data/demo_interaction_person.csv")



import pandas as pd
import ast

# Load the Excel file (replace with actual filename)
df = pd.read_excel("sato_space.xlsx")

# 1. Add "Space:" prefix to all IDs
df["id"] = df["id"].apply(lambda x: f"Space:{x}" if not str(x).startswith("Space:") else x)

# Helper to prefix items in column
def prefix_column_entries(value, prefix):
    if pd.isna(value):
        return value
    try:
        # Convert stringified list to Python list
        parsed = ast.literal_eval(value) if isinstance(value, str) and value.startswith("[") else value
    except (SyntaxError, ValueError):
        parsed = value

    if isinstance(parsed, list):
        return [f"{prefix}{item}" if not str(item).startswith(prefix) else item for item in parsed]
    elif isinstance(parsed, str):
        return f"{prefix}{parsed}" if not parsed.startswith(prefix) else parsed
    else:
        return value

# 2. Add "Zone:" prefix to hasZone
# df["hasZone"] = df["hasZone"].apply(lambda x: prefix_column_entries(x, "Zone:"))

# 3. Add "Space:" prefix to hasSpace
df["hasSpace"] = df["hasSpace"].apply(lambda x: prefix_column_entries(x, "Space:"))

# Save to new Excel file
df.to_excel("sato_space_prefixed.xlsx", index=False)
print("Transformation complete. Saved to 'sato_space_prefixed.xlsx'")

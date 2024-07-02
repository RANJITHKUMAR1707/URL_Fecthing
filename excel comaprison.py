import pandas as pd
import re

# Load the Excel files
file_live = 'C:\\Users\\ranjithkumar.sivakum\\Downloads\\Coats_live.xlsx'
file_mock = 'C:\\Users\\ranjithkumar.sivakum\\Downloads\\coats_mock.xlsx'

# Read the Excel files
df_live = pd.read_excel(file_live)
df_mock = pd.read_excel(file_mock)

# Print the number of rows in each file before processing
print(f"Number of rows in Coats_live.xlsx: {len(df_live)}")
print(f"Number of rows in coats_mock.xlsx: {len(df_mock)}")

# Function to extract the URL part after 'com' and convert to lowercase, ignoring trailing slashes
def extract_url_path(url):
    match = re.search(r'com/?(.*)', url, re.IGNORECASE)
    if match:
        path = match.group(1).lower()
        return path.rstrip('/')  # Remove trailing slashes
    return None

# Apply the function to the relevant columns and retain original URLs
df_live['URL Path'] = df_live.iloc[:, 0].apply(extract_url_path)
df_live['Original URL'] = df_live.iloc[:, 0]
df_mock['URL Path'] = df_mock.iloc[:, 0].apply(extract_url_path)
df_mock['Original URL'] = df_mock.iloc[:, 0]

# Drop rows with None values (in case there are any)
df_live = df_live.dropna(subset=['URL Path'])
df_mock = df_mock.dropna(subset=['URL Path'])

# Print the number of rows after dropping None values
print(f"Number of rows in Coats_live.xlsx after processing: {len(df_live)}")
print(f"Number of rows in coats_mock.xlsx after processing: {len(df_mock)}")

# URLs present in df_live but not in df_mock
unique_to_live = df_live[~df_live['URL Path'].isin(df_mock['URL Path'])]

# URLs present in df_mock but not in df_live
unique_to_mock = df_mock[~df_mock['URL Path'].isin(df_live['URL Path'])]

# Print the number of unique URLs in each file
print(f"Number of unique URLs in Coats_live.xlsx: {len(unique_to_live)}")
print(f"Number of unique URLs in coats_mock.xlsx: {len(unique_to_mock)}")

# Save the results to Excel files
unique_to_live.to_excel('unique_to_live.xlsx', index=False, columns=['Original URL'])
unique_to_mock.to_excel('unique_to_mock.xlsx', index=False, columns=['Original URL'])

print("URLs unique to Coats_live.xlsx:")
print(unique_to_live[['Original URL']])
print("\nURLs unique to coats_mock.xlsx:")
print(unique_to_mock[['Original URL']])

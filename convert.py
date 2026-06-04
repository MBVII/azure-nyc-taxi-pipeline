import pandas as pd

# Change this path to wherever you downloaded the parquet file
input_file = r"C:\Users\Manan\Downloads\yellow_tripdata_2025-03.parquet"
output_file = r"C:\Users\Manan\Downloads\yellow_tripdata_2025-03.csv"

print("Reading parquet file...")
df = pd.read_parquet(input_file, engine='pyarrow')

print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Keep only the columns we need (reduces file size)
cols = [
    'tpep_pickup_datetime', 'tpep_dropoff_datetime',
    'passenger_count', 'trip_distance', 'fare_amount',
    'total_amount', 'PULocationID', 'DOLocationID'
]
df = df[cols]

print("Converting to CSV...")
df.to_csv(output_file, index=False)
print(f"Done! Saved to {output_file}")
print(f"File has {len(df):,} rows")
#!/usr/bin/env python
# coding: utf-8

# ## NB_Transform_TaxiData
# 
# 
# 

# In[2]:


from pyspark.sql.functions import col, year, month, hour, avg, count

# Read CSV files from ADLS raw zone
df = spark.read.option("header", "true") \
               .option("inferSchema", "true") \
               .csv("abfss://raw@taxidatalakemanan.dfs.core.windows.net/Taxi/")

print(f"Total rows: {df.count()}")
df.printSchema()


# In[3]:


# Drop nulls in critical columns
df_clean = df.dropna(subset=["tpep_pickup_datetime", "fare_amount"])

# Filter out bad data
df_clean = df_clean.filter(
    (col("fare_amount") > 0) &
    (col("trip_distance") > 0) &
    (col("passenger_count") > 0)
)

# Add derived columns
df_clean = df_clean.withColumn("trip_year", year(col("tpep_pickup_datetime")))
df_clean = df_clean.withColumn("trip_month", month(col("tpep_pickup_datetime")))
df_clean = df_clean.withColumn("pickup_hour", hour(col("tpep_pickup_datetime")))

print(f"Clean rows: {df_clean.count()}")


# In[4]:


# Aggregated summary
df_agg = df_clean.groupBy("trip_year", "trip_month", "pickup_hour") \
    .agg(
        count("*").alias("total_trips"),
        avg("fare_amount").alias("avg_fare"),
        avg("trip_distance").alias("avg_distance")
    )

# Write clean data to processed zone
df_clean.write.mode("overwrite") \
    .option("header", "true") \
    .csv("abfss://processed@taxidatalakemanan.dfs.core.windows.net/taxi_clean/")

# Write aggregated data to curated zone
df_agg.write.mode("overwrite") \
    .option("header", "true") \
    .csv("abfss://curated@taxidatalakemanan.dfs.core.windows.net/taxi_agg/")

print("Done! Data written to processed and curated zones.")


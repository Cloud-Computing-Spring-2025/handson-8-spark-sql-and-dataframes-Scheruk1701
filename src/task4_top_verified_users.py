from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

spark = SparkSession.builder.appName("TopVerifiedUsers").getOrCreate()

# Load datasets
posts_df = spark.read.option("header", True).csv("input/posts.csv", inferSchema=True)
users_df = spark.read.option("header", True).csv("input/users.csv", inferSchema=True)

# Filter verified users
verified_users = users_df.filter(col("Verified") == True)

# Join with posts
joined_df = posts_df.join(verified_users, on="UserID", how="inner")

# Calculate total reach and group by Username
reach_df = joined_df.withColumn("Reach", col("Likes") + col("Retweets")) \
    .groupBy("Username") \
    .agg(_sum("Reach").alias("Total_Reach")) \
    .orderBy(col("Total_Reach").desc()) \
    .limit(5)

top_verified = reach_df

# Save result
top_verified.coalesce(1).write.mode("overwrite").csv("outputs/top_verified_users.csv", header=True)
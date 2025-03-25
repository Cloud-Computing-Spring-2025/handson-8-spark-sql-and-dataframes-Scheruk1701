from pyspark.sql import SparkSession
from pyspark.sql.functions import when, avg, col, round

spark = SparkSession.builder.appName("SentimentVsEngagement").getOrCreate()

# Load posts data
posts_df = spark.read.option("header", True).csv("input/posts.csv", inferSchema=True)

# Categorize sentiment
posts_categorized = posts_df.withColumn(
    "Sentiment",
    when(col("SentimentScore") > 0.3, "Positive")
    .when((col("SentimentScore") >= -0.3) & (col("SentimentScore") <= 0.3), "Neutral")
    .otherwise("Negative")
)

# Group by Sentiment and compute rounded average Likes and Retweets
sentiment_stats = posts_categorized.groupBy("Sentiment").agg(
    round(avg("Likes"), 1).alias("Avg_Likes"),
    round(avg("Retweets"), 1).alias("Avg_Retweets")
).orderBy(col("Avg_Likes").desc())

# Save result
sentiment_stats.coalesce(1).write.mode("overwrite").csv("outputs/sentiment_engagement.csv", header=True)
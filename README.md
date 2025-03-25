# handson-08-sparkSQL-dataframes-social-media-sentiment-analysis

## **Prerequisites**

Before starting the assignment, ensure you have the following software installed and properly configured on your machine:

1. **Python 3.x**:
   - [Download and Install Python](https://www.python.org/downloads/)
   - Verify installation:
     ```bash
     python --version
     ```

2. **PySpark**:
   - Install using `pip`:
     ```bash
     pip install pyspark
     ```

3. **Apache Spark**:
   - Ensure Spark is installed. You can download it from the [Apache Spark Downloads](https://spark.apache.org/downloads.html) page.
   - Verify installation by running:
     ```bash
     spark-submit --version
     ```

## **Setup Instructions**

### **1. Project Structure**

Ensure your project directory follows the structure below:

```
SocialMediaSentimentAnalysis/
├── input/
│   ├── posts.csv
│   └── users.csv
├── outputs/
│   ├── hashtag_trends.csv
│   ├── engagement_by_age.csv
│   ├── sentiment_engagement.csv
│   └── top_verified_users.csv
├── src/
│   ├── task1_hashtag_trends.py
│   ├── task2_engagement_by_age.py
│   ├── task3_sentiment_vs_engagement.py
│   └── task4_top_verified_users.py
├── docker-compose.yml
└── README.md
```



- **input/**: Contains the input datasets (`posts.csv` and `users.csv`)  
- **outputs/**: Directory where the results of each task will be saved.
- **src/**: Contains the individual Python scripts for each task.
- **docker-compose.yml**: Docker Compose configuration file to set up Spark.
- **README.md**: Assignment instructions and guidelines.

### **2. Running the Analysis Tasks**

You can run the analysis tasks either locally or using Docker.

#### **a. Running Locally**

1. **Navigate to the Project Directory**:
   ```bash
   cd /workspaces/handson-8-spark-sql-and-dataframes-Scheruk1701
   ```

2. **Execute Each Task Using `spark-submit`**:
   ```bash
 
     spark-submit src/task1_hashtag_trends.py
     spark-submit src/task2_engagement_by_age.py
     spark-submit src/task3_sentiment_vs_engagement.py
     spark-submit src/task4_top_verified_users.py
     
   ```

3. **Verify the Outputs**:
   Check the `outputs/` directory for the resulting files:
   ```bash
   ls outputs/
   ```

## **Overview**

In this assignment, you will leverage Spark Structured APIs to analyze a dataset containing employee information from various departments within an organization. Your goal is to extract meaningful insights related to employee satisfaction, engagement, concerns, and job titles. This exercise is designed to enhance your data manipulation and analytical skills using Spark's powerful APIs.

## **Objectives**

By the end of this assignment, you should be able to:

1. **Data Loading and Preparation**: Import and preprocess data using Spark Structured APIs.
2. **Data Analysis**: Perform complex queries and transformations to address specific business questions.
3. **Insight Generation**: Derive actionable insights from the analyzed data.

## **Dataset**

## **Dataset: posts.csv **

You will work with a dataset containing information about **100+ users** who rated movies across various streaming platforms. The dataset includes the following columns:

| Column Name     | Type    | Description                                           |
|-----------------|---------|-------------------------------------------------------|
| PostID          | Integer | Unique ID for the post                                |
| UserID          | Integer | ID of the user who posted                             |
| Content         | String  | Text content of the post                              |
| Timestamp       | String  | Date and time the post was made                       |
| Likes           | Integer | Number of likes on the post                           |
| Retweets        | Integer | Number of shares/retweets                             |
| Hashtags        | String  | Comma-separated hashtags used in the post             |
| SentimentScore  | Float   | Sentiment score (-1 to 1, where -1 is most negative)  |


---

## **Dataset: users.csv **
| Column Name | Type    | Description                          |
|-------------|---------|--------------------------------------|
| UserID      | Integer | Unique user ID                       |
| Username    | String  | User's handle                        |
| AgeGroup    | String  | Age category (Teen, Adult, Senior)   |
| Country     | String  | Country of residence                 |
| Verified    | Boolean | Whether the account is verified      |

---

### **Data**

Below is a snippet of the `posts.csv`,`users.csv` to illustrate the data structure. Ensure your dataset contains at least 100 records for meaningful analysis.

```
PostID,UserID,Content,Timestamp,Likes,Retweets,Hashtags,SentimentScore
101,4,Great performance on mobile.,2025-03-18 17:52:45,100,24,#UX,-0.78
102,6,Just another day...,2025-03-19 12:52:45,114,32,"#mood,#UX",0.45
103,10,Absolutely love the UX!,2025-03-17 18:52:45,110,5,"#social,#fail",0.12
104,10,Can’t stop using it!,2025-03-22 12:52:45,101,41,"#AI,#cleanUI,#UX",1.0
105,7,Worst experience ever.,2025-03-24 16:52:45,10,47,"#UX,#cleanUI",-0.45
```

---

```
UserID,Username,AgeGroup,Country,Verified
0,@stream_bot,Senior,Germany,False
1,@techie42,Adult,Brazil,True
2,@critic99,Teen,Germany,True
3,@daily_vibes,Teen,Canada,False
4,@designer_dan,Teen,US,True
```

---



## **Assignment Tasks**

Below are detailed explanations of how each task was approached and solved using PySpark DataFrame transformations, along with the resulting output.

---

### **1. Hashtag Trends**

**Objective:**  
Identify trending hashtags by analyzing their frequency of use across all posts.

**Approach:**

- The `Hashtags` column, which contains comma-separated strings, was first split into arrays using the `split()` function.
- These arrays were then flattened into individual rows using the `explode()` function, allowing each hashtag to be analyzed independently.
- A `groupBy` operation was applied to count the number of times each hashtag appears.
- Finally, the results were sorted in descending order by count to identify the most popular hashtags.

**Output:**

| Hashtag     | Count |
|-------------|-------|
| #cleanUI    | 24    |
| #UX         | 24    |
| #social     | 23    |
| #love       | 20    |
| #AI         | 19    |
| #design     | 19    |
| #fail       | 17    |
| #tech       | 16    |
| #bug        | 16    |
| #mood       | 15    |

---

### **2. Engagement by Age Group**

**Objective:**  
Understand how users from different age groups engage with content based on likes and retweets.

**Approach:**

- The `posts.csv` and `users.csv` datasets were loaded and joined on the `UserID` column to combine post-level engagement with user demographics.
- After the join, the data was grouped by `AgeGroup`.
- Aggregations were performed to calculate the average number of `Likes` and `Retweets` for each age group using the `avg()` function.
- Results were rounded to one decimal point for readability and sorted by average likes to highlight the most engaged group.

**Output:**

| Age Group | Avg Likes | Avg Retweets |
|-----------|-----------|--------------|
| Adult     | 92.5      | 24.5         |
| Teen      | 87.7      | 30.8         |
| Senior    | 70.8      | 26.8         |

---

### **3. Sentiment vs Engagement**

**Objective:**  
Evaluate how sentiment (positive, neutral, or negative) influences post engagement.

**Approach:**

- Posts were categorized into sentiment groups based on their `SentimentScore` using conditional logic:
  - **Positive**: score > 0.3  
  - **Neutral**: -0.3 ≤ score ≤ 0.3  
  - **Negative**: score < -0.3  
- The `withColumn()` and `when()` functions were used to derive a new `Sentiment` column reflecting these categories.
- Posts were then grouped by the `Sentiment` category and aggregated to calculate average likes and retweets.
- Results were sorted and rounded to provide insights into which sentiment group drives the most engagement.

**Output:**

| Sentiment | Avg Likes | Avg Retweets |
|-----------|-----------|--------------|
| Neutral   | 91.3      | 24.5         |
| Negative  | 87.8      | 28.2         |
| Positive  | 75.6      | 30.2         |

---

### **4. Top Verified Users by Reach**

**Objective:**  
Find the most influential verified users based on their post reach (likes + retweets).

**Approach:**

- Verified users were filtered from `users.csv` using the condition `Verified = True`.
- These users were then joined with post data using `UserID` to align engagement metrics.
- A new column `Reach` was created by summing `Likes` and `Retweets` for each post.
- Using `groupBy`, the total reach for each verified user was calculated and sorted in descending order.
- The top 5 verified users with the highest overall reach were selected as the final output.

**Output:**

| Username      | Total Reach |
|---------------|-------------|
| @techie42     | 1884        |
| @calm_mind    | 1508        |
| @meme_lord    | 976         |
| @designer_dan | 936         |
| @critic99     | 877         |

---


## **Grading Criteria**

| Task                        | Marks |
|-----------------------------|-------|
| Hashtag Trend Analysis      | 1     |
| Engagement by Age Group     | 1     |
| Sentiment vs Engagement     | 1     |
| Top Verified Users by Reach | 1     |
| **Total**                   | **1** |

---

## 📬 Submission Checklist

- [✅] PySpark scripts in the `src/` directory  
- [✅] Output files in the `outputs/` directory  
- [✅] Datasets in the `input/` directory  
- [✅] Completed `README.md`  
- [✅] Commit everything to GitHub Classroom  
- [✅] Submit your GitHub repo link on canvas

---

Now go uncover the trends behind the tweets 📊🐤✨

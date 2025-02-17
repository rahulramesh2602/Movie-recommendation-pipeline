---

### **📄 README.md**
```markdown
# 🎬 Movie Recommendation Pipeline with Apache Airflow

## 📌 Overview
This project builds an **end-to-end movie recommendation pipeline** using **Apache Airflow** and **AWS S3**. The pipeline automates:
1. **Uploading Raw Movie & Ratings Data** to S3.
2. **Preprocessing Data** (Merging & Cleaning) and storing it in S3.
3. **Training a Recommendation Model** using Singular Value Decomposition (SVD).
4. **Generating Movie Recommendations** based on user preferences.

---
## 🚀 Project Architecture
```
                     +--------------------------+
                     |  Dataset (movies.csv, ratings.csv) |
                     +--------------------------+
                                  |
                                  v
        +--------------------------------+
        | Upload to S3 (Raw Data)        |
        | Task: `upload_to_s3.py`        |
        +--------------------------------+
                                  |
                                  v
        +--------------------------------+
        | Preprocess Data (Merge & Clean)|
        | Task: `preprocess_data.py`     |
        +--------------------------------+
                                  |
                                  v
        +--------------------------------+
        | Train SVD Model (Collaborative)|
        | Task: `train_model.py`         |
        +--------------------------------+
                                  |
                                  v
        +--------------------------------+
        | Generate Movie Recommendations |
        | Task: `recommend_movies`       |
        +--------------------------------+

```
---
## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/Movie-recommendation-pipeline.git
cd Movie-recommendation-pipeline
```

### **2️⃣ Create a Virtual Environment**
```sh
python3 -m venv movie_rec
source movie_rec/bin/activate  # Mac/Linux
movie_rec\Scripts\activate     # Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Apache Airflow**
```sh
export AIRFLOW_HOME=~/airflow
pip install apache-airflow
airflow db init
airflow webserver --port 8080 &
airflow scheduler &
```

### **5️⃣ Configure AWS Credentials for S3 Access**
Ensure you have **AWS CLI configured** with IAM permissions to access S3:
```sh
aws configure
```
Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)

---
## 🎯 How the Pipeline Works
### **1️⃣ Upload Data to S3**
- The script `upload_to_s3.py` **uploads raw datasets** (`movies.csv`, `ratings.csv`) to an S3 bucket.

### **2️⃣ Preprocess Data**
- `preprocess_data.py` **downloads raw data from S3, merges, and cleans it**, and then **uploads processed data** back to S3.

### **3️⃣ Train the Recommendation Model**
- `train_model.py` **downloads preprocessed data** and trains an **SVD (Singular Value Decomposition) model**.
- The model is saved as `models/svd_recommender.pkl` inside the **Scripts folder**.

### **4️⃣ Generate Movie Recommendations**
- `recommend_movies.py` loads the trained model from **`Scripts/models/`** and **suggests movies** for a user.

---
## 🔥 Running the Pipeline in Airflow
### **1️⃣ Start Airflow**
```sh
airflow webserver --port 8080 &
airflow scheduler &
```
- Open **http://localhost:8080** in your browser.

### **2️⃣ Trigger the DAG Manually**
1. Navigate to the Airflow UI.
2. Find `movie_recommendation_pipeline`.
3. Click **Trigger DAG** ▶️ to start the pipeline.

---
## 📌 File Structure
```
├── Dataset/
│   ├── movies.csv
│   ├── ratings.csv
│
├── Scripts/
│   ├── upload_to_s3.py
│   ├── preprocess_data.py
│   ├── train_model.py
│   ├── models/                    # Trained model stored here
│   │   ├── svd_recommender.pkl
│
├── Dags/
│   ├── movie_recommendation.py  # Airflow DAG file
│
├── .flake8
├── .gitignore
├── requirements.txt
└── README.md
```

---
## 🔍 Example Output
```sh
🔄 Loading datasets...
✅ Data preprocessing complete! 100836 ratings loaded.
🚀 Training SVD model...
✅ Model training complete!
💾 Model saved to Scripts/models/svd_recommender.pkl
🔎 Generating recommendations for User 1...
🎬 Top recommended movies:
🎥 The Godfather (Movie ID: 858)
🎥 Die Hard (Movie ID: 1036)
🎥 The Godfather: Part II (Movie ID: 1221)
🎥 Jaws (Movie ID: 1387)
🎥 The Breakfast Club (Movie ID: 1968)
```

---
## 🔮 Future Enhancements
✅ **Enable Real-Time User Input** for Personalized Recommendations  
✅ **Deploy the Model as a REST API** (Using Flask or FastAPI)  
✅ **Integrate AWS Lambda & DynamoDB** for Scalable Data Storage  
✅ **Visualize Insights in a Web Dashboard**  

---
## 🤝 Contributing
Want to improve the project? Feel free to open **Issues** & **Pull Requests**!

### **🎬 Movie Recommendation Pipeline | Modern Data Engineering AWS Project**  

## **📌 Introduction**  
The goal of this project is to **build an end-to-end automated movie recommendation system** using **Apache Airflow** and **AWS**. The system ingests raw movie rating data, preprocesses it, trains a recommendation model, and generates personalized movie suggestions.  

This project follows a **modern data engineering approach**, leveraging tools such as **AWS S3, Apache Airflow, Python, Scikit-learn, and Boto3** to build a scalable and automated pipeline.  

---

## **🚀 Tools & Technologies Used**
- **Amazon S3** – Storage for raw and preprocessed datasets  
- **Apache Airflow** – Orchestration of the data pipeline  
- **Python** – Data processing and machine learning  
- **Scikit-Learn & SciPy** – Collaborative filtering using Singular Value Decomposition (SVD)  
- **Pandas & NumPy** – Data transformation and manipulation  
- **Boto3** – Interaction with AWS services  
- **Airflow XComs & Logs** – Task communication and monitoring  

---

## **📌 Project Workflow**
```
                 +--------------------------+
                 |  Dataset (movies.csv, ratings.csv) |
                 +--------------------------+
                                |
                                v
    +---------------------------------------------------+
    | Task 1: Upload Raw Data to S3                     |
    | Script: `upload_to_s3.py`                         |
    +---------------------------------------------------+
                                |
                                v
    +---------------------------------------------------+
    | Task 2: Preprocess Data (Merge & Clean)           |
    | Script: `preprocess_data.py`                      |
    | - Downloads raw data from S3                      |
    | - Merges ratings & movie metadata                 |
    | - Uploads processed data back to S3               |
    +---------------------------------------------------+
                                |
                                v
    +---------------------------------------------------+
    | Task 3: Train SVD Recommendation Model           |
    | Script: `train_model.py`                         |
    | - Downloads preprocessed data from S3            |
    | - Trains SVD-based collaborative filtering model |
    | - Saves model (`svd_recommender.pkl`)            |
    +---------------------------------------------------+
                                |
                                v
    +---------------------------------------------------+
    | Task 4: Generate Movie Recommendations           |
    | Script: `recommend_movies.py`                    |
    | - Loads trained model                             |
    | - Predicts top `n` movies for a given user       |
    | - Logs recommendations & stores in XCom          |
    +---------------------------------------------------+
```

---

## **📌 Pipeline Implementation in Apache Airflow**
The entire workflow is automated using **Apache Airflow**, ensuring **end-to-end orchestration** of the recommendation pipeline.  

**DAG Structure (`movie_recommendation_pipeline.py`)**
1️⃣ `upload_to_s3.py` – Uploads raw `movies.csv` & `ratings.csv` to S3  
2️⃣ `preprocess_data.py` – Merges, cleans data & uploads `preprocessed_data.csv` to S3  
3️⃣ `train_model.py` – Downloads preprocessed data & trains SVD model  
4️⃣ `recommend_movies.py` – Generates movie recommendations & stores results  

---

## **📌 Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/Movie-recommendation-pipeline.git
cd Movie-recommendation-pipeline
```

### **2️⃣ Create a Virtual Environment & Install Dependencies**
```sh
python3 -m venv movie_rec
source movie_rec/bin/activate  # Mac/Linux
movie_rec\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **3️⃣ Configure AWS Credentials**
Ensure your AWS CLI is configured to interact with S3:
```sh
aws configure
```

### **4️⃣ Start Apache Airflow**
```sh
export AIRFLOW_HOME=~/airflow
airflow db init
airflow webserver --port 8080 &
airflow scheduler &
```

### **5️⃣ Deploy the Airflow DAG**
Move the DAG to the Airflow DAGs directory:
```sh
mv movie_recommendation_pipeline.py ~/airflow/dags/
airflow dags reload
```

---

## **📌 Running the Pipeline in Airflow**
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

## **📌 File Structure**
```
├── Dataset/
│   ├── movies.csv
│   ├── ratings.csv
│
├── Scripts/
│   ├── upload_to_s3.py
│   ├── preprocess_data.py
│   ├── train_model.py
│   ├── recommend_movies.py
│   ├── models/                    # Trained model stored here
│   │   ├── svd_recommender.pkl
│
├── Dags/
│   ├── movie_recommendation_pipeline.py  # Airflow DAG file
│
├── .flake8
├── .gitignore
├── requirements.txt
└── README.md
```

---

## **📌 Example Output**
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

## **📌 Future Enhancements**
✅ **Enable Real-Time User Input for Personalized Recommendations**  
✅ **Deploy the Model as a REST API (Using Flask or FastAPI)**  
✅ **Store Predictions in a Database (PostgreSQL, DynamoDB, or S3 JSON)**  
✅ **Integrate AWS Lambda & DynamoDB for Scalable Data Storage**  
✅ **Visualize Insights in a Web Dashboard**  

---

## **📜 License**
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## **🤝 Contributing**
Want to improve the project? Feel free to open **Issues** & **Pull Requests**!

---

### **🚀 Next Steps**
🔹 **Add this `README.md` to your repository.**  
🔹 **Test your pipeline & monitor it in Apache Airflow.**  
🔹 **(Optional) Deploy as a REST API for real-time recommendations.**  

🔥 **Now your project is well-documented & production-ready!** 🚀  
Let me know if you need any refinements! 😊
import streamlit as st
import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Function to create the table if it doesn't exist
def create_table_if_not_exists(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        pclass INT,
        sex VARCHAR(10),
        age INT,
        sibsp INT,
        parch INT,
        embarked VARCHAR(50),
        title VARCHAR(20),
        survive BOOLEAN,
        proba FLOAT
    );
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

# Function to log prediction to database
def log_to_db(pclass, sex, age, sibsp, parch, embarked, title, survive, proba):
    try:
        connection = psycopg2.connect(
            host="database",
            port="5432",
            user="postgres",
            password="postgres",
            database="postgres"
        )
        create_table_if_not_exists(connection)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO predictions (pclass, sex, age, sibsp, parch, embarked, title, survive, proba)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (pclass, sex, age, sibsp, parch, embarked, title, survive, proba))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        st.error(f"Failed to log prediction to database: {e}")

# Streamlit form
st.title("Titanic Survival Prediction")
pclass = st.selectbox("Class", [1, 2, 3])
sex = st.selectbox("Sex", ["Erkek", "Kadın"])
title = st.selectbox("Title", ["Bay", "Hanım", "Bayan", "Usta", "Doktor", "Özgü"])
age = st.number_input("Age", min_value=1, max_value=100, value=30)
sibsp = st.number_input("Siblings/Spouses Aboard", min_value=0, max_value=10, value=0)
parch = st.number_input("Parents/Children Aboard", min_value=0, max_value=10, value=0)
embarked = st.selectbox("Embarked", ["Southampton, İngiltere", "Cherbourg, Fransa", "Queesntown, İrlanda"])

if st.button("Predict"):
    # Send request to FastAPI
    response = requests.post("http://fastapi:8000/predict", json={
        "pclass": pclass,
        "sex": sex,
        "age": age,
        "sibsp": sibsp,
        "parch": parch,
        "embarked": embarked,
        "title": title
    })
    if response.status_code == 200:
        result = response.json()
        st.write(f"Prediction: {result['survive']}")
        st.write(f"Probability: {result['proba']:.2f}%")
        # Log prediction to database
        log_to_db(pclass, sex, age, sibsp, parch, embarked, title, result['survive'], result['proba'])
    else:
        st.error("Error in prediction")

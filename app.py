import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PowerTransformer
from category_encoders import OneHotEncoder, OrdinalEncoder
def show_predict_pag():
    st.write("Software Developer Stroke Prediction")
    model = pickle.load(open("model.pkl", "rb"))


    with open('preprocessing_pipeline.pkl', 'rb') as file:
        pre = pickle.load(file)



    out = {}
    out['age']=st.slider("Age", 0, 100, 50)

    out['hypertension'] = 1 if st.radio("Hypertension", ["Yes", "NO"]) == "Yes" else 0
    out['heart_disease'] = 1 if st.radio("Heart Disease", ["Yes", "NO"]) == "Yes" else 0

    out['gender']=st.selectbox("Gender", ["Male", "Female"])

    out['ever_married']=st.radio("Ever Married", ["Yes", "NO"])

    work_type = ["children", "Self-employed", "Private", "Govt_job", "Never_worked"]

    out['work_type']=st.selectbox("Work Type", work_type)
    out['Residence_type']=st.radio("Residence Type", ["Urban", "Rural"])


    out['avg_glucose_level']=st.slider("Avg Glucose Level", 50, 300, 150)       

    out['bmi']=st.slider("BMI", 10, 100, 25)            
    smoking_status = ["formerly smoked", "never smoked", "smokes"]          
    out['smoking_status']=st.selectbox("Smoking Status", smoking_status)
    ok = st.button("Predict")
    data = pd.DataFrame([out])
    if ok:
        re = pre.transform(data)
        
        st.write("The predict: " + ("Potential Stroke" if model.predict(re)[0] else "Clear"))



def show_explore_pag():
    df = pd.read_csv("dataset.csv")
    num_cols = ["bmi", "avg_glucose_level", "age"]
    cat_cols = list(df.drop(columns=num_cols + ["stroke"]).columns)
    target_col = "stroke"

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    st.write("### Histogram for Stroke Numerical Columns")
    for i, col in enumerate(num_cols):
        sns.histplot(data=df, x=col, ax=ax[i], hue=target_col, kde=True, bins=50)
    st.pyplot(fig)

    st.write("### Countplot for Stroke Output")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="stroke", ax=ax)
    st.pyplot(fig)

    st.write("### Countplot for Smoking Status")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="smoking_status", ax=ax)
    st.pyplot(fig)

    st.write("### Countplot for Work Type")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="work_type", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45) 
    st.pyplot(fig)        
pag=st.sidebar.selectbox("Explore Or Prediction", ("Predict", "Explore"))
if pag == "Predict":

   show_predict_pag()
else:

    show_explore_pag()

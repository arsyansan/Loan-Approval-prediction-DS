import streamlit as st
import streamlit.components.v1 as stc
import pickle
import pandas as pd

with open("logistic_regression.pkl", "rb") as file:
    logistic_regression = pickle.load(file)

html_temp = """ <div style="background-color:#000;padding:10px;border-radius:10px;text-align:center">
                <h1 style="color:#fff;">Loan Eligibility Prediction App</h1>
                <h4 style="color:#fff;">Made for: Credit Team</h4>
                </div>
                """

desc_temp = """ ### Loan Prediction App
                This app is used by Credit Team for deciding Loan Application
                
                #### Data Source
                [Kaggle: Loan Prediction Dataset] (Masukkan Link)
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="background-color:#000;padding:10px;border-radius:10px;">
                    <h1 style="color:#fff;text-align:center;">Loan Eligibility Prediction</h1>
                </div>
                """
    
    st.markdown(design, unsafe_allow_html=True)

    left, right = st.columns((2,2))

    gender = left.selectbox("Gender", ("Male", "Female"))
    married = right.selectbox("Married", ("Yes", "No"))
    dependent = left.selectbox("Dependents", ("None", "One", "Two", "Three"))
    education = right.selectbox("Education", ("Graduate", "Non-Graduate"))
    self_employed = left.selectbox("Self-Employed", ("Yes", "No"))
    applicant_income = right.number_input("Applicant Income")
    coApplicant_income = left.number_input("co - Applicant Income")
    loan_amount = right.number_input("Loan Amount")
    loan_amount_term = left.number_input("Loan Tenor in Days")
    credit_history = right.number_input("Credit History", 0.0, 1.0)
    property_area = st.selectbox("Property Area", ("Semiurban", "Urban", "Rural"))

    button = st.button("Predict")

    #if button is clicked
    if button:
        result = predict(gender, married, dependent, education, self_employed,
                         applicant_income, coApplicant_income, loan_amount,
                         loan_amount_term, credit_history, property_area)

        if result == "Eligible":
            st.success(f"You are {result} for the loan.")
        
        else:
            st.warning(f"You are {result} for the loan.")

def predict(gender, married, dependent, education, self_employed,
            applicant_income, coApplicant_income, loan_amount,
            loan_amount_term, credit_history, property_area):
    
    #process user input
    gen = 0 if gender == "Male" else 1
    mar = 0 if married == "yes" else 1
    dep = float(0 if dependent == "None" else 1 if dependent == "One" else 2 if dependent == "Two" else 3)
    edu = 0 if education == "Graduate" else 1
    sem = 0 if self_employed == "Yes" else 1
    pro = 0 if property_area == "Semiurban" else 1 if property_area == "Urban" else 2
    lam = loan_amount/1000
    cap = coApplicant_income/1000

    features = pd.DataFrame({
        'Gender': [gen],
        'Married': [mar],
        'Dependents': [dep],
        'Education': [edu],
        'Self_Employed': [sem],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [cap],
        'LoanAmount': [lam],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Property_Area': [pro]
    })

        #making prediction
    prediction = logistic_regression.predict(features)

    result = "Not Eligible" if prediction == 0 else "Eligible"
    return result

if __name__ == "__main__":
    main()
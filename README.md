The main objective of this project was to develop a system that could automatically analyze and interpret Expected Credit Loss (ECL) for different categories of bank loans and assist decision-makers using an AI-based chatbot.

I began by studying the components of ECL — Probability of Default (PD), Loss Given Default (LGD), and Exposure at Default (EAD) — and realized that predicting PD using machine learning would be the key step.
For this, I used the Bank Loan Data from Kaggle, which contains borrower-level features like age, income, credit history, loan purpose, and amount.

The data was cleaned by handling missing values, encoding categorical variables, and creating a few new features such as the income-to-loan ratio and a risk factor derived from loan percent income and interest rate.

I then trained a Neural Network (NN) to predict the loan default probability (PD). The model achieved around 87% accuracy and a ROC-AUC score of 0.91, which indicated strong performance.
After obtaining PD, I computed ECL using the formula: ECL=PD×LGD×EAD

where LGD was fixed at 0.45 and EAD was taken as the loan amount. The ECL was aggregated by loan segment (like education, medical, venture, etc.) to identify which areas posed higher risk.

To make the analysis interactive, I built a FastAPI-based application with three main routes:

/auth – for login and role-based access (Analyst & CRO)

/ecl – for viewing and plotting ECL curves

/chat – for natural language interaction using Google Gemini 

The chatbot interprets ECL data and provides recommendations such as “increase interest for medical loans” or “reduce disbursement for venture loans.”

This approach combines machine learning for risk prediction and LLMs for interpretation, creating an end-to-end intelligent assistant that automates ECL analysis and supports faster, data-driven financial decisions.

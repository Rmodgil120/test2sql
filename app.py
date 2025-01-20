from dotenv import load_dotenv
load_dotenv()  

import pandasql as ps
import streamlit as st
import os
import pandas as pd
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function To execute SQL-like queries on a CSV file
def read_csv_query(sql, csv_file):
    try:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')
        sql = sql.replace('sales_data_sample', 'df')
        result = ps.sqldf(sql, locals()) 
        return result
    except Exception as e:
        return f"Error executing query: {e}"



# Define Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The CSV file has the name sales_data_sample and has the following columns: 
    ORDERNUMBER, QUANTITYORDERED, ORDERLINENUMBER, QTR_ID, MONTH_ID, YEAR_ID, PRICEEACH, SALES, STATUS, CONTACTFIRSTNAME, 
    COUNTRY, DEALSIZE, PRODUCTLINE. 

    For example:
    Example 1 - How many orders have been placed?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM sales_data_sample;
    Example 2 - Show all orders from customers in the USA, 
    the SQL command will be something like this: SELECT * FROM sales_data_sample WHERE COUNTRY = "USA";
    Example 3 - What is the total sales amount?, 
    the SQL command will be something like this: SELECT SUM(SALES) FROM sales_data_sample;

    The SQL code should not include ``` at the beginning or end, and the output should not contain the word "sql".
    """
]

# Streamlit App
st.set_page_config(page_title="Retrieve SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write("Generated SQL Query:", response)
    result = read_csv_query(response, "sales_data_sample.csv")
    st.subheader("The Response is")
    if isinstance(result, pd.DataFrame):
        st.dataframe(result)
    else:
        st.write(result)
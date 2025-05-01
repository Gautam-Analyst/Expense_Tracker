# Save this as expense_tracker_app.py and run using: streamlit run expense_tracker_app.py

import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💸 Group Expense Tracker")

# Excel file path
file_path = r"C:\Users\gowth\Downloads\Expense_Tracker\expenses.xlsx"

# Define members
members = ['Naresh', 'Jeevan', 'Bharath', 'Gowtham']

# Form input
with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        expense_date = st.date_input("Date", value=date.today())
        expense_name = st.text_input("Expense Name")
        remarks = st.text_input("Remarks")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        selected_members = st.multiselect("Select Members Involved", members)

    submitted = st.form_submit_button("💾 Save Expense")

# Load or create file
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=['Date', 'Expense Name', 'Amount', *members, 'Remarks'])

# Save data
if submitted:
    if not selected_members:
        st.warning("Please select at least one member.")
    else:
        split_amount = amount / len(selected_members)
        member_data = {member: (split_amount if member in selected_members else 0) for member in members}
        new_row = {
            'Date': expense_date,
            'Expense Name': expense_name,
            'Amount': amount,
            **member_data,
            'Remarks': remarks
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(file_path, index=False)
        st.success("Expense saved successfully!")

# Show previous records
st.markdown("---")
st.subheader("📜 Previous Expenses")
st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💸 Group Expense Tracker")

# Excel file path
file_path = r"C:\Users\gowth\Downloads\Expense_Tracker\expenses.xlsx"

# Define members
members = ['Naresh', 'Jeevan', 'Bharath', 'Gowtham']

# Load or create file
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=['Date', 'Expense Name', 'Amount', *members, 'Remarks'])

# --- Form input ---
with st.form("expense_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        expense_date = st.date_input("Date", value=date.today(), key="date")
        expense_name = st.text_input("Expense Name", key="name")
        remarks = st.text_input("Remarks", key="remarks")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, step=1.0, key="amount")
        selected_members = st.multiselect("Select Members Involved", members, key="sel")

    save_btn = st.form_submit_button("💾 Save Expense")
    clear_btn = st.form_submit_button("🗑️ Clear Form")

    if save_btn:
        if not selected_members:
            st.warning("Please select at least one member.")
        elif not expense_name:
            st.warning("Please enter an expense name.")
        elif amount <= 0:
            st.warning("Amount must be greater than zero.")
        else:
            split_amount = round(amount / len(selected_members), 2)
            new_data = {
                'Date': expense_date.strftime("%Y-%m-%d"),
                'Expense Name': expense_name,
                'Amount': amount,
                'Remarks': remarks
            }
            for m in members:
                new_data[m] = split_amount if m in selected_members else 0.0

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(file_path, index=False)
            st.success("Expense saved successfully!")

    if clear_btn:
        # reset session state keys
        for key in ("date","name","remarks","amount","sel"):
            if key in st.session_state:
                # for multiselect, reset to empty list
                st.session_state[key] = [] if key=="sel" else None
        st.experimental_rerun()

# --- Export Button ---
st.markdown("---")
export_buffer = BytesIO()
df.to_excel(export_buffer, index=False)
export_buffer.seek(0)
st.download_button(
    label="📥 Export All Expenses to Excel",
    data=export_buffer,
    file_name="expenses_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- Display history ---
st.subheader("📜 Previous Expenses")
st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

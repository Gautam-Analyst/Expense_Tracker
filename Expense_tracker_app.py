import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Group Expense Tracker")

# Constants
FILE_PATH = r"C:\Users\gowth\Downloads\Expense_Tracker\expenses.xlsx"
MEMBERS   = ['Naresh', 'Jeevan', 'Bharath', 'Gowtham']

# Load or initialize DataFrame
if os.path.exists(FILE_PATH):
    df = pd.read_excel(FILE_PATH)
else:
    df = pd.DataFrame(columns=['Date','Expense Name','Amount',*MEMBERS,'Remarks'])

st.markdown("---")
st.subheader("➕ Add New Expense")

# --- Add Form ---
with st.form("add_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        expense_date  = st.date_input("Date", value=date.today(), key="f_date")
        expense_name  = st.text_input("Expense Name", key="f_name")
        remarks       = st.text_input("Remarks", key="f_remarks")
    with c2:
        amount             = st.number_input("Amount (₹)", min_value=0.0, step=1.0, key="f_amount")
        selected_members   = st.multiselect("Select Members", MEMBERS, key="f_sel")

    save_btn = st.form_submit_button("💾 Save Expense")

    if save_btn:
        if not expense_name:
            st.warning("Enter expense name.")
        elif not selected_members:
            st.warning("Select at least one member.")
        elif amount <= 0:
            st.warning("Amount must be > 0.")
        else:
            split_amt = round(amount / len(selected_members), 2)
            new_row = {
                'Date': expense_date.strftime("%Y-%m-%d"),
                'Expense Name': expense_name,
                'Amount': amount,
                'Remarks': remarks
            }
            for m in MEMBERS:
                new_row[m] = split_amt if m in selected_members else 0.0

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(FILE_PATH, index=False)
            st.success("Expense saved!")

# --- Clear Form Button ---
if st.button("🗑️ Clear Form Inputs"):
    for key in ("f_date","f_name","f_remarks","f_amount","f_sel"):
        if key in st.session_state:
            # reset date to today, name/remarks to "", amount to 0.0, sel to []
            if key == "f_date":
                st.session_state[key] = date.today()
            elif key == "f_amount":
                st.session_state[key] = 0.0
            elif key == "f_sel":
                st.session_state[key] = []
            else:
                st.session_state[key] = ""
    st.experimental_rerun()

# --- Export Button ---
st.markdown("---")
export_buffer = BytesIO()
df.to_excel(export_buffer, index=False)
export_buffer.seek(0)
st.download_button(
    "📥 Export All to Excel",
    data=export_buffer,
    file_name="expenses_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- History Table ---
st.markdown("---")
st.subheader("📜 Previous Expenses")
st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

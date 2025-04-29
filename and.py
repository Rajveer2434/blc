import streamlit as st
import pandas as pd
import hashlib

# Function to hash patient name
def hash_name(name):
    return hashlib.sha256(name.encode()).hexdigest()

# Initialize session state
if 'patients' not in st.session_state:
    st.session_state.patients = []

st.title("🏥 Hospital Ledger (Fully Hashed)")

# Sidebar: Add new patient
st.sidebar.header("Add New Patient")
with st.sidebar.form("patient_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    reason = st.text_input("Reason for Admission")
    bill = st.number_input("Bill Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Patient")
    if submitted and name:
        name_hash = hash_name(name)
        st.session_state.patients.append({
            "NameHash": name_hash,
            "Age": age,
            "Reason": reason,
            "Bill": bill,
            "Discharged": False
        })
        st.success("Patient added with hashed ID.")

# Display patient ledger
st.subheader("Current Patient Ledger")
if st.session_state.patients:
    df = pd.DataFrame([
        {
            "Patient ID": p["NameHash"],
            "Age": p["Age"],
            "Reason": p["Reason"],
            "Bill": p["Bill"],
            "Discharged": p["Discharged"]
        }
        for p in st.session_state.patients
    ])
    st.dataframe(df)
else:
    st.info("No patients admitted yet.")

# Discharge a patient by hash input
st.subheader("Discharge a Patient")
hash_input = st.text_input("Enter Patient Hashed ID to Discharge")
if st.button("Discharge"):
    found = False
    for p in st.session_state.patients:
        if p["NameHash"] == hash_input and not p["Discharged"]:
            p["Discharged"] = True
            st.success("Patient discharged.")
            found = True
            break
    if not found:
        st.warning("Patient not found or already discharged.")

# Revenue summary
st.subheader("💰 Revenue Summary")
total_revenue = sum(p["Bill"] for p in st.session_state.patients if p["Discharged"])
st.metric("Total Revenue Collected", f"${total_revenue:.2f}")

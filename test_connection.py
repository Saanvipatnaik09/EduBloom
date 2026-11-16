
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="EduBloom Connection Test")

st.title("🌸 EduBloom Cloud Connection Test")

try:
    # Read credentials securely from Streamlit Secrets
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    # Connect to Supabase
    supabase = create_client(url, key)

    st.success("Connected to Supabase successfully!")

    # Test access to the students table
    response = (
        supabase
        .table("students")
        .select("id, roll_number, name")
        .limit(5)
        .execute()
    )

    st.success("Students table accessed successfully!")

    st.write("Sample database records:")

    if response.data:
        st.dataframe(response.data, use_container_width=True)
    else:
        st.info("Your students table is empty. That's okay!")

except Exception as e:
    st.error("Connection test failed.")
    st.exception(e)

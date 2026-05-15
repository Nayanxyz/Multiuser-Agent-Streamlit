import streamlit as st
import requests

# === 1. UI CONFIGURATION ===
st.set_page_config(page_title="Enterprise Swarm", page_icon="🐝", layout="wide")

# === 2. API CONNECTION (THE BRIDGE) ===
# We declare the base URL so we can route to both /chat and /upload-doc
BASE_API_URL = "https://swarm-api-super-agent-travily.onrender.com"

# === 3. SESSION MEMORY & IDENTITY ===
# Instead of a random UUID, we let you lock in a specific username.
if "username" not in st.session_state:
    st.session_state.username = "nayan_desktop"

if "messages" not in st.session_state:
    st.session_state.messages = []

# === 4. THE ADMIN VAULT (SIDEBAR) ===
with st.sidebar:
    st.header("⚙️ Admin Knowledge Vault")
    st.write("Securely upload rules, facts, or company data to the AI's Supabase brain.")

    upload_content = st.text_area("Document Content", height=150, placeholder="Type facts here...")

    # type="password" hides it with dots. Remove type="password" if you want to see the text!
    admin_password = st.text_input("Admin Password", type="password", placeholder="Enter secret...")

    if st.button("Upload to Brain", type="primary"):
        if not upload_content or not admin_password:
            st.error("⚠️ Missing content or password!")
        else:
            with st.spinner("Encrypting and Uploading..."):
                try:
                    response = requests.post(
                        f"{BASE_API_URL}/upload-doc",
                        json={"admin_password": admin_password, "content": upload_content}
                    )

                    if response.status_code == 200:
                        result = response.json()
                        if result.get("status") == "success":
                            st.success("✅ Knowledge secured in vault!")
                        else:
                            st.error(f"❌ Failed: {result.get('message', 'Unauthorized')}")
                    else:
                        st.error(f"❌ Server rejected request. Status: {response.status_code}")
                except Exception as e:
                    st.error("🔌 Network error. Is Render awake?")



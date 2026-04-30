import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import streamlit as st
import pandas as pd
from process_data import detect_churn

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Toddle Churn System", layout="wide")

# 🎨 STYLE
st.markdown("""
<style>
.stMetric {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Toddle Churn Detection Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
churned = detect_churn()

if churned is None or len(churned) == 0:
    st.warning("No data found.")
    st.stop()

# -------------------------
# EXTRA FIELDS
# -------------------------
churned["contact_email"] = churned["person_id"].apply(lambda x: f"user{x}@gmail.com")
churned["phone"] = churned["person_id"].apply(lambda x: f"+91-98{x:08d}")
churned["linkedin_url"] = churned["name"].apply(
    lambda x: f"https://www.linkedin.com/in/{x.lower().replace(' ', '-')}"
)
churned["status"] = churned["is_toddle_customer"].apply(
    lambda x: "🔴 Non-Toddle" if x == "No" else "🟢 Toddle"
)

# -------------------------
# FILTERS
# -------------------------
st.sidebar.header("🔍 Filters")

status_filter = st.sidebar.selectbox(
    "Filter by Status",
    ["All", "🔴 Non-Toddle", "🟢 Toddle"]
)

search_name = st.sidebar.text_input("Search by Name")

filtered_df = churned.copy()

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

if search_name:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search_name, case=False)
    ]

# -------------------------
# 🔥 KPI CARDS
# -------------------------
col1, col2, col3 = st.columns(3)

total = len(churned)
churn_count = (churned["is_toddle_customer"] == "No").sum()
toddle_count = total - churn_count

# -------------------------
# 🔥 INSIGHT
# -------------------------
action_df = filtered_df[filtered_df["is_toddle_customer"] == "No"]

if not action_df.empty:
    top_school = action_df["new_school"].value_counts().idxmax()
    st.info(f"🔥 Most teachers moved to: {top_school}")

# -------------------------
# MAIN TABLE
# -------------------------
st.subheader("📊 Teacher Movement Tracking")

st.dataframe(
    filtered_df[
        [
            "person_id",
            "name",
            "old_school",
            "new_school",
            "status",
            "contact_email",
            "phone",
            "linkedin_url"
        ]
    ],
    use_container_width=True
)

# ====================================================
# 🎯 FOLLOW-UP TRACKER (🔥 UNIQUE FEATURE)
# ====================================================
if "contacted_ids" not in st.session_state:
    st.session_state.contacted_ids = set()

# ====================================================
# 🎯 CONTACT PANEL
# ====================================================
st.markdown("---")
st.subheader("🎯 Contact Non-Toddle Teacher")

if action_df.empty:
    st.success("No Non-Toddle teachers 🎉")

else:
    colA, colB = st.columns([1, 2])

    # LEFT
    with colA:
        ids = action_df["person_id"].astype(int).unique().tolist()
        selected_id = st.selectbox("Select S. No", ids)

        teacher = action_df[action_df["person_id"] == selected_id].iloc[0]

    # RIGHT
    with colB:
        st.markdown("### 📌 Change Notice")
        st.warning(
            f"{teacher['name']} moved from "
            f"**{teacher['old_school']} → {teacher['new_school']}**"
        )

        st.markdown("### 👤 Details")
        st.write(f"📧 {teacher['contact_email']}")
        st.write(f"📞 {teacher['phone']}")
        st.markdown(f"[🔗 LinkedIn]({teacher['linkedin_url']})")

        # -------------------------
        # FOLLOW-UP STATUS
        # -------------------------
        if teacher["person_id"] in st.session_state.contacted_ids:
            st.success("✔️ Already Contacted")
        else:
            st.warning("⏳ Not Contacted Yet")

        if st.button("✅ Mark as Contacted"):
            st.session_state.contacted_ids.add(teacher["person_id"])

        # -------------------------
        # MESSAGE
        # -------------------------
        def generate_message(name, old_school, new_school):
            return f"""Hi {name},

We noticed your move from {old_school} to {new_school}.

We’d love to support you with Toddle.

Best regards,
Toddle Team"""

        msg = generate_message(
            teacher["name"],
            teacher["old_school"],
            teacher["new_school"]
        )

        st.markdown("### 📩 Outreach Message")
        st.text_area("Message", msg, height=130)

        # -------------------------
        # CONTACT BUTTONS
        # -------------------------
        st.markdown("### 📬 Contact")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.button("📧 Email")

        with col2:
            phone_num = teacher["phone"].replace("+", "").replace("-", "")
            st.markdown(f"[📱 WhatsApp](https://wa.me/{phone_num})")

        with col3:
            st.button("📞 Call")

        with col4:
            st.markdown(f"[🔗 LinkedIn]({teacher['linkedin_url']})")

# -------------------------
# INFO
# -------------------------
st.markdown("---")

st.subheader("🧠 System Design")

st.write("""
- Detects when teachers move to non-Toddle schools
- Highlights action-required users
- Provides direct outreach tools
- Tracks follow-up status (CRM-like feature)
""")
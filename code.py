import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
import plotly.graph_objects as go
import os

# --- HEADER SECTION ---
st.markdown("""
    <style>
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-align: center;
        padding-top: 10px;
        padding-bottom: 0px;
        margin-bottom: 0px;
    }
    .college-name {
        font-size: 42px;
        font-weight: 800;
        color: #1E3A8A; /* Deep Blue color */
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0px;
    }
    .dept-name {
        font-size: 24px;
        font-weight: 400;
        color: #64748B; /* Slate Gray color */
        margin-top: -10px;
        letter-spacing: 2px;
    }
    </style>
    
    <div class="main-header">
        <h1 class="college-name">ST. JOSEPH'S DEGREE COLLEGE</h1>
        <p class="dept-name">BCA DEPARTMENT</p>
    </div>
    <hr style="margin-top: 0px; margin-bottom: 25px; border: 0; border-top: 2px solid #eee;">
    """, unsafe_allow_html=True)


st.title("🎓 Student Academic Risk Detection System")
tab1, tab2, tab3 = st.tabs([
    "📘 Student Search",
    "📊 Risk Analysis",
    "📈 Visualizations"
])

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "Studentdata.csv"))
df["Student_ID"] = df["Student_ID"].astype(str).str.strip()
# Initialize session state for sidebar values
if "attendance" not in st.session_state:
    st.session_state.attendance = 75
    st.session_state.internal_marks = 40
    st.session_state.assignment_score = 60
    st.session_state.gpa = 6.5
    st.session_state.backlog = "No"

# st.write(df["Student_ID"].head(10))

# Encode categorical columns
df["Backlog_Status"] = df["Backlog_Status"].map({"Yes": 1, "No": 0})
df["Risk_Status"] = df["Risk_Status"].map({"At Risk": 1, "Not At Risk": 0})

# Feature selection
X = df.drop(["Student_ID", "Course", "Risk_Status"], axis=1)
y = df["Risk_Status"]

# Train Decision Tree model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Sidebar inputs (Manual Prediction)
# --- SIDEBAR: HIGH-LEVEL CONTROL PANEL ---
with st.sidebar:
    # 1. Branding / Logo Area
    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h2 style='color: #1E3A8A; margin-bottom: 0;'>⚙️ Control Panel</h2>
            <p style='color: #64748B; font-size: 0.8rem;'>STUDENT DATA MANAGEMENT</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # 2. Grouped Inputs using Expanders or Containers
    st.subheader("📝 Academic Parameters")
    
    with st.container(border=True):
        # Attendance with a more descriptive tooltip
        attendance = st.slider(
            "📈 Attendance (%)", 0, 100,
            st.session_state.attendance,
            help="Total percentage of classes attended in the current semester."
        )

        # Academic Performance Group
        internal_marks = st.number_input(
            "📝 Internal Marks", 0, 100, 
            value=st.session_state.internal_marks,
            step=1
        )
        
        assignment_score = st.number_input(
            "📂 Assignment Score", 0, 100, 
            value=st.session_state.assignment_score,
            step=1
        )

    st.subheader("🎓 History & Status")
    with st.container(border=True):
        gpa = st.slider(
            "⭐ Previous GPA", 4.0, 10.0,
            st.session_state.gpa,
            step=0.1
        )

        # Use a Radio button for a faster "one-click" choice than a selectbox
        backlog = st.radio(
            "❗ Backlog Status",
            ["No", "Yes"],
            index=0 if st.session_state.backlog == "No" else 1,
            horizontal=True
        )

    st.divider()
    
    # 3. Primary Action Button
    # Large, high-visibility button
    predict_btn = st.button(
        "⚡ RUN ANALYSIS", 
        use_container_width=True, 
        type="primary"
    )
    
    if predict_btn:
        st.toast("Processing data...", icon="⏳")

input_data = pd.DataFrame({
    "Attendance_Percentage": [attendance],
    "Internal_Marks": [internal_marks],
    "Assignment_Score": [assignment_score],
    "Previous_GPA": [gpa],
    "Backlog_Status": [1 if backlog == "Yes" else 0]
})


if st.button("Predict Academic Risk"):
    # 1. Run your model
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    risk_percentage = probability[0][1] * 100
    
    # 2. Save to session state
    st.session_state.prediction = prediction
    st.session_state.risk_percentage = risk_percentage
    st.session_state.prediction_run = True  # Added a flag to confirm we ran it

    # 3. Force a rerun so that line 289 (and the rest of the app) 
    # now sees the newly created risk_percentage
    st.rerun()

# --- DOWN NEAR LINE 289 ---
# Only try to access the variable if the prediction has actually been run
if st.session_state.get("prediction_run"):
    risk_val = st.session_state.risk_percentage
    
    # Now display your results based on the saved state
    if st.session_state.prediction[0] == 1:
        st.error(f"⚠️ Student is AT ACADEMIC RISK")
        st.write(f"📊 **Risk Probability:** {risk_val:.2f}%")
    else:
        st.success("✅ Student is NOT AT ACADEMIC RISK")
        st.write(f"📊 **Risk Probability:** {risk_val:.2f}%")

with tab1:
    st.subheader("🔍 Student Data Explorer")
    
    # 1. UI Upgrade: Clean Search Bar
    with st.container(border=True):
        col_search, col_btn = st.columns([3, 1])
        with col_search:
            search_id = st.selectbox(
                "Select Student ID",
                df["Student_ID"].unique(),
                label_visibility="collapsed"
            )
        with col_btn:
            # Use a unique key to prevent state conflicts
            search_clicked = st.button("🔎 Search Record", use_container_width=True, type="primary")

    # 2. Search Logic
    if search_clicked:
        student_record = df[df["Student_ID"] == search_id]

        if student_record.empty:
            st.error("❌ Student ID not found.")
        else:
            # SAVE to session_state so other tabs can see it
            st.session_state.attendance = int(student_record["Attendance_Percentage"].values[0])
            st.session_state.internal_marks = int(student_record["Internal_Marks"].values[0])
            st.session_state.assignment_score = int(student_record["Assignment_Score"].values[0])
            st.session_state.gpa = float(student_record["Previous_GPA"].values[0])
            st.session_state.backlog = "Yes" if student_record["Backlog_Status"].values[0] == 1 else "No"
            
            # This flag tells the app we have a record loaded
            st.session_state.record_loaded = True 
            
            st.toast(f"Record {search_id} Loaded!", icon="✅")
            
            # IMPORTANT: This forces Streamlit to refresh and show the data in the metrics/sidebar
            st.rerun() 

    # 3. Persistent Display: This shows the data even AFTER the button click is finished
    if st.session_state.get("record_loaded"):
        st.markdown("### 📄 Current Student Profile")
        # Displaying the record for the currently selected ID
        current_data = df[df["Student_ID"] == search_id]
        st.dataframe(current_data, use_container_width=True)
        
with tab2:
    st.markdown("### 📊 Performance Analytics & System Verdict")
    
    # KPI Row with cleaner formatting
    with st.container():
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Attendance", f"{st.session_state.attendance}%")
        m2.metric("Int. Marks", f"{st.session_state.internal_marks}/100")
        m3.metric("Assignment", f"{st.session_state.assignment_score}/100")
        m4.metric("GPA", st.session_state.gpa)
        m5.metric("Backlogs", st.session_state.backlog)

    st.divider()

    if "prediction" in st.session_state:
        # Create a clean side-by-side layout for Verdict and Advice
        col_verdict, col_advice = st.columns([1, 1])
        
        with col_verdict:
            st.markdown("#### 🎯 Prediction Outcome")
            risk_val = st.session_state.risk_percentage
            
            # Use colored "Status Cards" instead of standard error/success boxes
            if st.session_state.prediction[0] == 1:
                st.markdown(f"""
                    <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #d32f2f;">
                        <h3 style="color: #d32f2f; margin: 0;">STATUS: AT ACADEMIC RISK</h3>
                        <p style="color: #b71c1c; margin: 5px 0 0 0;">System Probability: {risk_val:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32;">
                        <h3 style="color: #2e7d32; margin: 0;">STATUS: ACADEMICALLY SECURE</h3>
                        <p style="color: #1b5e20; margin: 5px 0 0 0;">System Confidence: {100 - risk_val:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)

        with col_advice:
            st.markdown("#### 📝 Faculty Action Items")
            if st.session_state.prediction[0] == 1:
                st.info("📌 **Recommended Action**: Schedule a counseling session with the HOD.")
                st.warning("📌 **Observation**: Focus on increasing Attendance and Internal Marks.")
            else:
                st.info("✅ **Recommended Action**: Continue standard monitoring.")

with tab3:
    st.markdown("### 📈 Comprehensive Analysis")

if "attendance" in st.session_state and "risk_percentage" in st.session_state:        
        # Gauge Chart remains a top-level professional choice
        risk_val = st.session_state.risk_percentage
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_val,
            title={'text': "Risk Probability Index", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': "#1E3A8A"},
                'bar': {'color': "#1E3A8A"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#eeeeee",
                'steps': [
                    {'range': [0, 50], 'color': "#f1f8e9"},
                    {'range': [50, 100], 'color': "#fff5f5"}
                ],
            }
        ))
        
        fig_gauge.update_layout(height=350, margin=dict(t=50, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Performance comparison chart
        st.markdown("#### 📊 Comparative Metrics")
        chart_data = pd.DataFrame({
            "Category": ["Attendance", "Internals", "Assignment", "GPA (Scaled)"],
            "Score": [st.session_state.attendance, st.session_state.internal_marks, 
                      st.session_state.assignment_score, st.session_state.gpa * 10]
        })
        
        fig_bar = px.bar(chart_data, x="Category", y="Score", color="Score",
                         color_continuous_scale="Blues", template="plotly_white")
        fig_bar.update_layout(coloraxis_showscale=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

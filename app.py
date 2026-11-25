import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from optimizer import optimize_smart_classrooms, ELECTRICITY_RATE_PER_KWH

# Page Configuration
st.set_page_config(
    page_title="Smart Classroom Optimization | Presidency University",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File Paths
ROOMS_FILE = "data/classrooms.csv"
CLASSES_FILE = "data/classes.csv"
REPORT_FILE = "reports/smart_allocation_results.csv"

os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Helper function to load data safely without KeyError
def load_data(file_path, default_cols):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Defensive check for power columns in classrooms
        if "base_power_kw" not in df.columns:
            if "lighting_kw" in df.columns and "display_kw" in df.columns:
                df["base_power_kw"] = df["lighting_kw"] + df["display_kw"]
            else:
                df["base_power_kw"] = 1.5
        if "hvac_power_kw" not in df.columns:
            if "hvac_kw" in df.columns:
                df["hvac_power_kw"] = df["hvac_kw"]
            else:
                df["hvac_power_kw"] = 3.5
        if "facilities" not in df.columns and "smart_facilities" in df.columns:
            df["facilities"] = df["smart_facilities"]
        return df
    return pd.DataFrame(columns=default_cols)

rooms = load_data(ROOMS_FILE, ["room_id", "room_name", "block", "capacity", "facilities", "base_power_kw", "hvac_power_kw", "smart_tier"])
classes = load_data(CLASSES_FILE, ["class_id", "class_name", "department", "students", "day", "time_slot", "required_facility", "priority"])

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0b2545 0%, #134074 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #134074;
        padding: 15px;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #134074;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
    }
    .stButton>button:hover {
        background-color: #0b2545;
        color: #eef4f8;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Branding & Navigation
with st.sidebar:
    st.image("https://presidencyuniversity.in/wp-content/themes/pu/images/logo.png", width=220) if False else None
    st.markdown("### 🏫 PRESIDENCY UNIVERSITY")
    st.markdown("**School of Information Science**  \n*Department of Mathematics*  \n`MAT4002: Operations Research`")
    st.divider()
    page = st.radio(
        "Navigation",
        [
            "Dashboard Overview",
            "Smart Classroom Management",
            "Class Management",
            "Master Timetable",
            "OR Optimization Results",
            "IoT Energy & Green Analytics"
        ]
    )
    st.divider()
    st.caption("Developed for MCA Experiential Learning Mini Project  \nAcademic Year 2026-27")

# Banner Header
st.markdown("""
<div class="main-header">
    <h2 style='margin:0; color:#EEF4F8;'>PRESIDENCY UNIVERSITY</h2>
    <h3 style='margin:4px 0; color:#8DA9C4;'>Smart Classroom Resource & Energy Optimization System</h3>
    <p style='margin:0; font-size:14px; opacity:0.9;'>Operations Research (Linear Programming) Application using Python, PuLP & Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: DASHBOARD OVERVIEW
# ==========================================
if page == "Dashboard Overview":
    st.subheader("📊 Campus Infrastructure & Academic Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    total_rooms = len(rooms)
    total_classes = len(classes)
    total_students = int(classes["students"].sum()) if not classes.empty else 0
    total_capacity = int(rooms["capacity"].sum()) if not rooms.empty else 0
    total_power = float((rooms["base_power_kw"] + rooms["hvac_power_kw"]).sum()) if not rooms.empty else 0.0
    
    col1.metric("Smart Rooms", total_rooms)
    col2.metric("Scheduled Classes", total_classes)
    col3.metric("Total Students", total_students)
    col4.metric("Total Capacity", total_capacity)
    col5.metric("Peak Power Load", f"{total_power:.1f} kW")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if not rooms.empty:
            fig_cap = px.bar(
                rooms,
                x="room_name",
                y="capacity",
                color="block",
                title="Smart Classroom Seating Capacity by Building Block",
                labels={"capacity": "Seating Capacity", "room_name": "Classroom"},
                text="capacity"
            )
            fig_cap.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_cap, use_container_width=True)
            
    with c2:
        if not classes.empty:
            fig_dept = px.pie(
                classes,
                names="department",
                values="students",
                title="Student Distribution by Department",
                hole=0.4
            )
            st.plotly_chart(fig_dept, use_container_width=True)
            
    st.markdown("#### 📋 Current Scheduled Classes")
    st.dataframe(classes, use_container_width=True)


# ==========================================
# PAGE 2: SMART CLASSROOM MANAGEMENT
# ==========================================
elif page == "Smart Classroom Management":
    st.subheader("🏢 Smart Classroom Infrastructure Management")
    st.write("Manage smart classroom facilities, IoT equipment specifications, HVAC loads, and capacities.")
    
    st.dataframe(rooms, use_container_width=True)
    
    with st.expander("➕ Register New Smart Classroom", expanded=False):
        with st.form("add_room_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                r_name = st.text_input("Classroom Identifier / Room Name (e.g. Smart-CR-304)")
                r_block = st.selectbox("Campus Block", ["Block-A (Academic)", "Block-B (Computing)", "Block-C (Science & Tech)", "Management Block"])
                r_capacity = st.number_input("Seating Capacity", min_value=15, max_value=300, value=50, step=5)
                r_tier = st.selectbox("Smart Classroom Tier", ["Tier-1 (Advanced AI/Studio)", "Tier-2 (Interactive Standard)", "Tier-3 (Basic Smart)"])
            with col_b:
                r_facilities = st.multiselect(
                    "Smart Facilities & IoT Hardware",
                    ["Smart_Board", "IoT_HVAC", "Smart_Lighting", "Lecture_Capture", "AI_Workstations", "Audio_System", "High_Speed_WiFi"],
                    default=["Smart_Board", "IoT_HVAC", "Smart_Lighting"]
                )
                r_base_kw = st.number_input("Base Equipment Power Load (kW)", min_value=0.5, max_value=20.0, value=1.5, step=0.1)
                r_hvac_kw = st.number_input("HVAC / Air Conditioning Load (kW)", min_value=1.0, max_value=30.0, value=3.5, step=0.5)
                
            submit_room = st.form_submit_button("Register Classroom")
            
            if submit_room:
                if not r_name.strip():
                    st.error("Please enter a valid classroom name.")
                elif r_name.strip() in rooms["room_name"].astype(str).values:
                    st.error(f"Classroom '{r_name}' already exists.")
                else:
                    new_id = int(rooms["room_id"].max()) + 1 if not rooms.empty else 1
                    facilities_str = ",".join(r_facilities)
                    tier_clean = r_tier.split(" ")[0]
                    new_row = {
                        "room_id": new_id,
                        "room_name": r_name.strip(),
                        "block": r_block,
                        "capacity": r_capacity,
                        "facilities": facilities_str,
                        "base_power_kw": r_base_kw,
                        "hvac_power_kw": r_hvac_kw,
                        "smart_tier": tier_clean
                    }
                    rooms = pd.concat([rooms, pd.DataFrame([new_row])], ignore_index=True)
                    rooms.to_csv(ROOMS_FILE, index=False)
                    st.success(f"Classroom '{r_name.strip()}' successfully added to database!")
                    st.rerun()


# ==========================================
# PAGE 3: CLASS MANAGEMENT
# ==========================================
elif page == "Class Management":
    st.subheader("📚 Scheduled Classes & Curriculum Configuration")
    st.write("Maintain university course cohorts, student strengths, time slots, and smart facility requirements.")
    
    st.dataframe(classes, use_container_width=True)
    
    with st.expander("➕ Add Scheduled Class Cohort", expanded=False):
        with st.form("add_class_form"):
            col_x, col_y = st.columns(2)
            with col_x:
                c_name = st.text_input("Class Name (e.g. MCA_3rd_Sem_CyberSecurity)")
                c_dept = st.selectbox("Department", ["MCA", "BCA", "M.Tech", "B.Tech", "MBA", "B.Com"])
                c_students = st.number_input("Enrolled Student Strength", min_value=5, max_value=250, value=40, step=1)
                c_priority = st.selectbox("Academic Priority", ["High", "Medium", "Normal"])
            with col_y:
                c_day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
                c_slot = st.selectbox("Time Slot", [
                    "09:00-10:00", "10:00-11:00", "11:00-12:00",
                    "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"
                ])
                c_facility = st.selectbox(
                    "Mandatory Required Facility",
                    ["Smart_Board", "Lecture_Capture", "AI_Workstations", "Audio_System", "Standard"]
                )
                
            submit_class = st.form_submit_button("Add Scheduled Class")
            
            if submit_class:
                if not c_name.strip():
                    st.error("Please enter a valid class name.")
                elif c_name.strip() in classes["class_name"].astype(str).values:
                    st.error(f"Class '{c_name}' already exists.")
                elif not rooms.empty and c_students > rooms["capacity"].max():
                    st.error(f"No classroom on campus has capacity for {c_students} students (Max room capacity is {rooms['capacity'].max()}).")
                else:
                    new_cid = int(classes["class_id"].max()) + 1 if not classes.empty else 1
                    new_class = {
                        "class_id": new_cid,
                        "class_name": c_name.strip(),
                        "department": c_dept,
                        "students": c_students,
                        "day": c_day,
                        "time_slot": c_slot,
                        "required_facility": c_facility,
                        "priority": c_priority
                    }
                    classes = pd.concat([classes, pd.DataFrame([new_class])], ignore_index=True)
                    classes.to_csv(CLASSES_FILE, index=False)
                    st.success(f"Class '{c_name.strip()}' successfully scheduled!")
                    st.rerun()


# ==========================================
# PAGE 4: MASTER TIMETABLE
# ==========================================
elif page == "Master Timetable":
    st.subheader("📅 University Master Timetable Matrix")
    if os.path.exists(REPORT_FILE):
        alloc_data = pd.read_csv(REPORT_FILE)
        
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            sel_day = st.selectbox("Filter by Day", ["All Days"] + sorted(alloc_data["Day"].unique().tolist()))
        with col_f2:
            sel_dept = st.selectbox("Filter by Department", ["All Departments"] + sorted(alloc_data["Department"].unique().tolist()))
            
        filtered_df = alloc_data.copy()
        if sel_day != "All Days":
            filtered_df = filtered_df[filtered_df["Day"] == sel_day]
        if sel_dept != "All Departments":
            filtered_df = filtered_df[filtered_df["Department"] == sel_dept]
            
        st.dataframe(
            filtered_df[["Class", "Department", "Students", "Day", "Time", "Room", "Block", "Capacity", "Energy_kWh", "Energy_Cost_INR"]],
            use_container_width=True
        )
        
        st.download_button(
            label="📥 Download Master Timetable CSV",
            data=filtered_df.to_csv(index=False),
            file_name="master_smart_timetable.csv",
            mime="text/csv"
        )
    else:
        st.info("⚠️ Please run the optimization engine from the 'OR Optimization Results' tab first to generate the timetable.")


# ==========================================
# PAGE 5: OR OPTIMIZATION RESULTS
# ==========================================
elif page == "OR Optimization Results":
    st.subheader("⚡ Mixed-Integer Linear Programming Optimization Engine")
    st.write("Formulates and solves the assignment problem using PuLP with CBC branch-and-cut solver.")
    
    with st.expander("⚙️ Optimizer Weight Tuning (Sensitivity)", expanded=False):
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            w_energy = st.slider("Energy Minimization Weight (α)", 0.0, 5.0, 1.5, 0.1)
        with col_w2:
            w_capacity = st.slider("Unused Capacity Penalty Weight (β)", 0.0, 5.0, 0.5, 0.1)
            
    if st.button("🚀 Run Smart Classroom Optimization", type="primary"):
        with st.spinner("Formulating mathematical constraints and solving via PuLP..."):
            try:
                results_df = optimize_smart_classrooms(energy_weight=w_energy, capacity_weight=w_capacity)
                if results_df is not None and not results_df.empty:
                    st.session_state["opt_results"] = results_df
                    st.success("✅ Optimal allocation found! Constraints satisfied without clashes.")
                else:
                    st.error("❌ Problem is infeasible. Check classroom capacities or facility requirements.")
            except Exception as e:
                st.error(f"Solver Error: {str(e)}")
                
    if os.path.exists(REPORT_FILE):
        results_df = pd.read_csv(REPORT_FILE)
        
        st.markdown("#### 🎯 Optimal Assignment Summary")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Allocated Classes", len(results_df))
        m2.metric("Total Students", int(results_df["Students"].sum()))
        m3.metric("Unused Seats", int(results_df["Empty_Seats"].sum()))
        m4.metric("Avg Utilization", f"{results_df['Utilization_Pct'].mean():.1f}%")
        m5.metric("Total Cost", f"₹ {results_df['Energy_Cost_INR'].sum():.2f}")
        
        st.markdown("---")
        st.markdown("#### 📋 Optimal Assignment Matrix")
        st.dataframe(results_df, use_container_width=True)
        
        # Plot Class vs Capacity colored by Room
        fig_alloc = px.bar(
            results_df,
            x="Class",
            y="Capacity",
            color="Room",
            hover_data=["Students", "Empty_Seats", "Energy_kWh"],
            title="Classroom Capacity vs Scheduled Class Allocation",
            text="Students"
        )
        fig_alloc.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_alloc, use_container_width=True)
        
        st.download_button(
            label="📥 Download Allocation Report (CSV)",
            data=results_df.to_csv(index=False),
            file_name="smart_classroom_allocation_report.csv",
            mime="text/csv"
        )


# ==========================================
# PAGE 6: IOT ENERGY & GREEN ANALYTICS
# ==========================================
elif page == "IoT Energy & Green Analytics":
    st.subheader("🌱 Smart Campus Green Energy & IoT Analytics")
    
    if os.path.exists(REPORT_FILE):
        data = pd.read_csv(REPORT_FILE)
        total_energy = data["Energy_kWh"].sum()
        total_cost = data["Energy_Cost_INR"].sum()
        total_students = data["Students"].sum()
        total_capacity = data["Capacity"].sum()
        seat_util_pct = (total_students / total_capacity) * 100
        
        # Environmental calculation: Central Electricity Authority of India emission factor ~0.82 kg CO2 per kWh
        co2_emissions_kg = total_energy * 0.82
        # Baseline comparison: if scheduled randomly in max capacity halls (e.g. 100 capacity halls @ 12 kW)
        baseline_energy = len(data) * 12.0
        saved_energy = baseline_energy - total_energy
        saved_cost = saved_energy * ELECTRICITY_RATE_PER_KWH
        saved_co2 = saved_energy * 0.82
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Energy Consumed", f"{total_energy:.1f} kWh", delta=f"-{saved_energy:.1f} kWh vs Baseline", delta_color="inverse")
        kpi2.metric("Operational Cost", f"₹ {total_cost:.2f}", delta=f"-₹ {saved_cost:.2f} Saved", delta_color="inverse")
        kpi3.metric("Capacity Utilization", f"{seat_util_pct:.1f}%", delta="High Efficiency")
        kpi4.metric("Carbon Footprint", f"{co2_emissions_kg:.1f} kg CO₂", delta=f"-{saved_co2:.1f} kg CO₂ Reduced", delta_color="inverse")
        
        st.markdown("---")
        
        g1, g2 = st.columns(2)
        with g1:
            room_energy = data.groupby("Room")["Energy_kWh"].sum().reset_index()
            fig_energy = px.bar(
                room_energy,
                x="Room",
                y="Energy_kWh",
                title="Total Energy Consumption by Smart Classroom (kWh)",
                color="Energy_kWh",
                color_continuous_scale="Tealgrn"
            )
            st.plotly_chart(fig_energy, use_container_width=True)
            
        with g2:
            room_util = data.groupby("Room").apply(
                lambda g: (g["Students"].sum() / g["Capacity"].sum()) * 100
            ).reset_index(name="Utilization (%)")
            fig_util = px.bar(
                room_util,
                x="Room",
                y="Utilization (%)",
                title="Room-Wise Seating Utilization Efficiency (%)",
                color="Utilization (%)",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_util, use_container_width=True)
            
        st.markdown("#### 📈 Department-wise Energy Footprint")
        dept_energy = data.groupby("Department")[["Students", "Energy_kWh", "Energy_Cost_INR"]].sum().reset_index()
        st.dataframe(dept_energy, use_container_width=True)
        
    else:
        st.info("⚠️ No optimization records found. Please run the optimization engine to view analytics.")

# Footer
st.markdown("---")
st.caption("Presidency University, Bengaluru | Department of Mathematics | Course: MAT4002 Operations Research | Technology: Python • Streamlit • Pandas • PuLP (CBC Solver) • Plotly")

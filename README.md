# 🏫 Smart Classroom Energy Optimization System
### Operations Research Experiential Learning Project (MAT4002)
**Institution:** Presidency University, Bengaluru  
**School:** School of Information Science | **Department:** Department of Mathematics  
**Program:** MCA (Master of Computer Applications) — Semester 3  

---

## 📌 Project Overview
The **Smart Classroom Energy Optimization System** applies **Linear Programming (LP / Mixed-Integer Linear Programming)** to solve the multi-criteria classroom assignment and energy scheduling challenge in higher educational institutions.

By integrating empirical data from **Electricity Bills** (commercial high-tension BESCOM HT-2b tariffs, Time-of-Day pricing, and contract sanctioned demand caps) alongside departmental **Classroom Schedules**, the system optimizes class-to-room allocations to:
1. Minimize total electrical energy consumption ($kWh$) and utility bills ($INR$).
2. Eliminate unused seating capacity and spatial wastage.
3. Guarantee zero timetable clashes and 100% smart technological facility compatibility.

---

## 🚀 Key Features
* **Linear Programming Engine:** Formulated using Python's `PuLP` library and solved with the `COIN-OR CBC` branch-and-cut solver.
* **Empirical Energy Billing Model:** Uses realistic BESCOM institutional tariff rates (Peak: ₹10.50/kWh, Normal: ₹8.50/kWh) and power demand caps (250 kVA).
* **Interactive Web Dashboard:** Built with `Streamlit` and `Plotly` featuring 6 comprehensive modules:
  - 📊 **Dashboard Overview:** Real-time campus infrastructure KPIs and distribution charts.
  - ⚡ **Electricity Bill & Tariff Analysis:** Tariff breakdowns and sanctioned demand tracking.
  - 🏢 **Smart Classroom Management:** Room hardware, capacities, and electrical ratings (Lighting, IFP, HVAC).
  - 📚 **Class Management:** Course cohorts, enrolled strengths, and time slots.
  - 📅 **Master Timetable Matrix:** Filterable schedule with CSV export.
  - 🌱 **Green Campus & Energy Analytics:** Carbon reduction metrics ($kg\ CO_2$), cost savings, and efficiency benchmarks.

---

## 📊 Optimal Results Achieved
* **Solver Status:** Optimal (0.04s execution)
* **Allocation Success:** 12 of 12 classes scheduled (100%)
* **Seating Capacity Utilization:** **90.97%** (48 empty seats across 12 sessions, 66.2% reduction vs baseline)
* **Total Energy Consumed:** **68.40 kWh** (24.75% energy reduction)
* **Financial Savings:** ₹191.25 saved per 12 hours of instruction

---

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Mathematical Modeling:** PuLP 2.9.0 (COIN-OR CBC Solver)
* **Web UI Framework:** Streamlit
* **Data Processing:** Pandas
* **Data Visualization:** Plotly Express & Plotly Graph Objects
* **Documentation:** python-docx

---

## 💻 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/spandanama27/<repository-name>.git
   cd <repository-name>
   ```

2. **Install required dependencies:**
   ```bash
   pip install pulp plotly pandas streamlit python-docx
   ```

3. **Run the Operations Research Optimizer:**
   ```bash
   python optimizer.py
   ```

4. **Launch the Interactive Web Dashboard:**
   ```bash
   streamlit run app.py
   ```
   Or double-click `run_app.bat` on Windows. Open your browser at `http://localhost:8501`.

---

## 📁 Repository Structure
```
├── app.py                                            # Streamlit web dashboard
├── optimizer.py                                      # PuLP Linear Programming optimization engine
├── generate_word_report.py                           # Word document generator
├── run_app.bat                                       # Windows one-click launcher
├── PROJECT_REPORT.md                                 # Full academic project report (Markdown)
├── Smart_Classroom_Energy_Optimization_Report.docx   # Academic project report (Word Document)
├── data/
│   ├── classrooms.csv                                # Smart rooms, capacities, and power ratings
│   ├── classes.csv                                   # Academic classes and time slots
│   ├── classroom_schedules.csv                       # Timetable roster
│   └── electricity_bills.csv                         # BESCOM institutional energy bills
└── reports/
    └── smart_allocation_results.csv                  # Solver output allocation matrix
```

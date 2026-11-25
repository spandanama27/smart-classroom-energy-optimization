import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_table(table, header_bg="0B2545", row_bg_even="F8F9FA", row_bg_odd="FFFFFF"):
    """Applies modern academic formatting to a docx table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Format header row
    for cell in table.rows[0].cells:
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(9.5)
                run.font.name = "Calibri"

    # Format body rows
    for i, row in enumerate(table.rows[1:], start=1):
        bg = row_bg_even if i % 2 == 0 else row_bg_odd
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9.5)
                    run.font.name = "Calibri"

def add_heading_with_spacing(doc, text, level, space_before=12, space_after=6, color=(11, 37, 69)):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.color.rgb = RGBColor(*color)
    return h

def generate_report():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # COVER / HEADER SECTION
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("PRESIDENCY UNIVERSITY\n")
    r_inst1.font.size = Pt(18)
    r_inst1.font.bold = True
    r_inst1.font.color.rgb = RGBColor(11, 37, 69)

    r_inst2 = p_inst.add_run("SCHOOL OF INFORMATION SCIENCE\nDEPARTMENT OF MATHEMATICS\n")
    r_inst2.font.size = Pt(13)
    r_inst2.font.bold = True
    r_inst2.font.color.rgb = RGBColor(19, 64, 116)

    r_inst3 = p_inst.add_run("EXPERIENTIAL LEARNING MINI PROJECT (CA3)\nAcademic Year: 2026-27\n")
    r_inst3.font.size = Pt(11)
    r_inst3.font.italic = True
    r_inst3.font.color.rgb = RGBColor(100, 116, 139)

    r_course = p_inst.add_run("Course Code: MAT4002  |  Course Name: INTRODUCTION TO OPERATIONS RESEARCH\n")
    r_course.font.size = Pt(11)
    r_course.font.bold = True
    r_course.font.color.rgb = RGBColor(11, 37, 69)

    doc.add_paragraph() # Spacer

    # Project Title Banner
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("SMART CLASSROOM OPTIMIZATION SYSTEM\n")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(11, 37, 69)

    r_sub = p_title.add_run("Multi-Factor Resource Allocation and Green Energy Scheduling using Mixed-Integer Linear Programming")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # Student Details Table
    stud_table = doc.add_table(rows=9, cols=2)
    stud_data = [
        ("Student Names", "Joyceria Gonsalves, Ranjitha K J, Prerana R"),
        ("Registration Number 1", "20252MCA0110"),
        ("Registration Number 2", "20252MCA0132"),
        ("Registration Number 3", "20252MCA0142"),
        ("Program", "MCA (Master of Computer Applications)"),
        ("Semester", "Third Semester"),
        ("Section", "3MCA04"),
        ("Project Title", "SMART CLASSROOM OPTIMIZATION SYSTEM"),
        ("Date of Submission", "24/11/2026")
    ]
    for row_idx, (k, v) in enumerate(stud_data):
        row = stud_table.rows[row_idx]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[1].paragraphs[0].add_run(v)
    format_table(stud_table, header_bg="134074")

    doc.add_paragraph()

    # Evaluation Scheme Table
    eval_table = doc.add_table(rows=5, cols=3)
    eval_headers = ["Component", "Maximum Marks", "Marks Obtained"]
    for c_idx, h_text in enumerate(eval_headers):
        eval_table.rows[0].cells[c_idx].paragraphs[0].add_run(h_text)
    eval_rows = [
        ("Project Report", "10", ""),
        ("Presentation", "5", ""),
        ("Viva-Voce", "5", ""),
        ("Total Marks", "20", "")
    ]
    for r_idx, row_data in enumerate(eval_rows, start=1):
        for c_idx, val in enumerate(row_data):
            run = eval_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
            if r_idx == 4:
                run.bold = True
    format_table(eval_table, header_bg="0B2545")

    doc.add_paragraph()
    p_sig = doc.add_paragraph()
    p_sig.add_run("Student 1 Signature: _______________          Student 2 Signature: _______________\n")
    p_sig.add_run("Student 3 Signature: _______________          Faculty Signature: __________________\n")
    p_sig.runs[0].font.size = Pt(10)
    p_sig.runs[1].font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "ABSTRACT", level=1, color=(11, 37, 69))
    p_abs = doc.add_paragraph(
        "Modern educational institutions are actively modernizing instructional spaces into digitally equipped "
        "Smart Classrooms. In universities such as Presidency University, instructional facilities feature interactive "
        "flat panel (IFP) displays, automated Internet of Things (IoT) HVAC climate controls, motorized audio-visual lecture "
        "capture systems, and high-performance AI computing workstations. While smart classrooms substantially elevate pedagogical "
        "engagement, they introduce significant scheduling complexity and operational costs. Manual classroom assignment by "
        "departmental committees frequently fails to balance multiple conflicting criteria: matching student strength with room "
        "capacities, fulfilling specialized technological requirements, avoiding timetable double-bookings, and curtailing excessive "
        "electricity consumption. Large smart lecture halls and laboratories equipped with high-tonnage HVAC systems consume between "
        "6 kW and 12 kW per hour; assigning small cohorts to such spaces causes severe electrical wastage, inflated utility bills, "
        "and higher carbon emissions."
    )
    p_abs.paragraph_format.line_spacing = 1.15

    doc.add_paragraph(
        "This experiential learning project formulates and implements an Operations Research (OR) framework to systematically "
        "solve the Smart Classroom Optimization problem. The system formulates the allocation challenge as a Mixed-Integer Linear "
        "Programming (MILP) model. The primary objective is to minimize a weighted multi-criteria function that concurrently curtails "
        "total campus electrical energy consumption (kilowatt-hours, kWh) and minimizes unused classroom seating capacity, while strictly "
        "enforcing hard constraints: single room assignment per cohort, sufficient seating capacity, mandatory IoT facility matching, "
        "and non-overlapping time-slot occupancy."
    )

    doc.add_paragraph(
        "The software application is engineered using Python, Streamlit, Pandas, PuLP (leveraging the COIN-OR CBC branch-and-cut solver), "
        "and Plotly for interactive visual analytics. Computational validation on a benchmark dataset of 12 classes across 10 smart classrooms "
        "demonstrated an optimal allocation achieving 90.97% average seating utilization, zero scheduling conflicts, 100% facility compliance, "
        "and a 24.75% reduction in total energy consumption compared to heuristic baseline allocations."
    )

    p_kw = doc.add_paragraph()
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.bold = True
    p_kw.add_run("Smart Classroom Optimization, Operations Research, Mixed-Integer Linear Programming (MILP), PuLP, CBC Solver, IoT Energy Efficiency, Resource Allocation, Streamlit, Python.")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "TABLE OF CONTENTS", level=1, color=(11, 37, 69))
    toc_table = doc.add_table(rows=12, cols=2)
    toc_data = [
        ("Chapter", "Title"),
        ("1", "Introduction and Problem Identification"),
        ("2", "Literature Review and Conceptual Background"),
        ("3", "Objectives, Scope and Proposed Solution"),
        ("4", "Mathematical Formulation"),
        ("5", "Methodology and System Workflow"),
        ("6", "Data Collection and Preparation"),
        ("7", "Software Implementation and System Modules"),
        ("8", "Illustrative Results and Discussion"),
        ("9", "Testing, Validation and Limitations"),
        ("10", "Conclusion and Future Enhancements"),
        ("—", "References and Appendix")
    ]
    for r_idx, (ch, tit) in enumerate(toc_data):
        toc_table.rows[r_idx].cells[0].paragraphs[0].add_run(ch)
        toc_table.rows[r_idx].cells[1].paragraphs[0].add_run(tit)
    format_table(toc_table, header_bg="134074")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # LIST OF ABBREVIATIONS
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "LIST OF ABBREVIATIONS", level=1, color=(11, 37, 69))
    abbr_table = doc.add_table(rows=12, cols=2)
    abbr_data = [
        ("Abbreviation", "Meaning"),
        ("OR", "Operations Research"),
        ("LP", "Linear Programming"),
        ("MILP", "Mixed-Integer Linear Programming"),
        ("IoT", "Internet of Things"),
        ("IFP", "Interactive Flat Panel Display"),
        ("HVAC", "Heating, Ventilation, and Air Conditioning"),
        ("CBC", "COIN-OR Branch and Cut Solver"),
        ("CSV", "Comma-Separated Values"),
        ("kWh", "Kilowatt-hour"),
        ("BESCOM", "Bangalore Electricity Supply Company Limited"),
        ("X_ij", "Binary class-to-classroom assignment decision variable")
    ]
    for r_idx, (ab, me) in enumerate(abbr_data):
        abbr_table.rows[r_idx].cells[0].paragraphs[0].add_run(ab)
        abbr_table.rows[r_idx].cells[1].paragraphs[0].add_run(me)
    format_table(abbr_table, header_bg="0B2545")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION AND PROBLEM IDENTIFICATION
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 1: INTRODUCTION AND PROBLEM IDENTIFICATION", level=1)
    
    add_heading_with_spacing(doc, "1.1 Introduction", level=2)
    doc.add_paragraph(
        "Higher educational institutions worldwide manage numerous academic programs, student cohorts, faculty schedules, and "
        "physical learning environments. At Presidency University, instructional facilities have expanded beyond traditional lecture "
        "rooms into technologically sophisticated smart classrooms. These spaces incorporate Interactive Flat Panel (IFP) displays, "
        "integrated audio systems, automated PTZ lecture-capture cameras for hybrid learning, and centralized Internet of Things (IoT) "
        "HVAC climate controls."
    )
    doc.add_paragraph(
        "While smart classrooms significantly elevate the educational experience, their administrative scheduling and energy management "
        "present complex operational problems. Each academic department (such as MCA, BCA, M.Tech, and B.Tech) conducts specialized "
        "courses requiring specific technological infrastructure. For example, an Advanced AI or Deep Learning session requires specialized "
        "AI workstations, an MCA project review requires multimedia recording and audio amplification, while a mathematical foundations "
        "course requires only an interactive whiteboard."
    )
    doc.add_paragraph(
        "From an Operations Research perspective, smart classrooms represent heterogeneous, scarce, and energy-intensive physical resources. "
        "Unlike conventional rooms, smart spaces draw significant power. An unoptimized schedule that assigns a 25-student cohort to a "
        "100-seater multimedia auditorium equipped with dual 4-ton HVAC units wastes considerable electrical energy and seats, incurring "
        "substantial financial expenditure and unnecessary carbon emissions. The Smart Classroom Optimization System applies mathematical "
        "programming to automate, optimize, and harmonize this multi-criteria resource allocation process."
    )

    add_heading_with_spacing(doc, "1.2 Identification of the Problem", level=2)
    doc.add_paragraph(
        "Presidency University operates multiple departments with hundreds of enrolled students across diverse academic batches. "
        "Classroom scheduling is traditionally handled manually or through decentralized departmental spreadsheets. This fragmented "
        "approach exhibits fundamental flaws:"
    )
    doc.add_paragraph("• Academic coordinators lack real-time visibility into campus-wide power consumption and HVAC loads.")
    doc.add_paragraph("• Room assignments prioritize spatial proximity rather than technological requirement matching or energy conservation.")
    doc.add_paragraph("• Classrooms frequently experience severe capacity mismatches, where small elective courses occupy large auditoriums, forcing larger core cohorts into cramped spaces.")
    doc.add_paragraph("• Rooms are susceptible to double-booking during peak morning academic slots (09:00 AM – 12:00 PM).")

    add_heading_with_spacing(doc, "1.3 Problems in Manual Allocation", level=2)
    doc.add_paragraph("• Severe Energy Wastage: Running large HVAC chillers and high-wattage smart displays for small cohorts incurs unnecessary electrical loads (wasting up to 5–8 kWh per hour per room).")
    doc.add_paragraph("• Technological Facility Mismatch: Classes needing specialized hardware (e.g., AI workstations or lecture capture cameras) are inadvertently assigned to rooms lacking these assets.")
    doc.add_paragraph("• Wasted Seating Capacity: Large percentage of unoccupied seats in oversized lecture theatres while other cohorts lack suitable spaces.")
    doc.add_paragraph("• Timetable Clashes and Double Booking: Simultaneous scheduling of multiple batches into the same smart room during identical periods.")
    doc.add_paragraph("• Administrative Burden: Hundreds of administrative hours spent by timetable committees manually drafting, revising, and troubleshooting room timetables each semester.")

    add_heading_with_spacing(doc, "1.4 Formal Problem Statement", level=2)
    p_stat = doc.add_paragraph()
    r_stat = p_stat.add_run(
        "To design, formulate, and develop an Operations Research-driven Smart Classroom Optimization System that systematically "
        "assigns scheduled academic classes to available smart classrooms such that combined electrical energy consumption (kWh) "
        "and unused seating capacity are minimized, while strictly satisfying student capacity thresholds, smart facility requirements, "
        "and timetable non-clash constraints."
    )
    r_stat.italic = True
    r_stat.bold = True

    # -------------------------------------------------------------
    # CHAPTER 2: LITERATURE REVIEW AND CONCEPTUAL BACKGROUND
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 2: LITERATURE REVIEW AND CONCEPTUAL BACKGROUND", level=1)
    
    add_heading_with_spacing(doc, "2.1 Operations Research in Resource and Energy Allocation", level=2)
    doc.add_paragraph(
        "Operations Research (OR) provides mathematical and analytical methodologies for optimal decision-making under resource scarcity. "
        "Originating during World War II for military logistics, OR has expanded into industrial scheduling, transportation networks, supply chains, "
        "and facility operations. In educational institutions, timetable and room allocation problems are traditionally treated as NP-hard combinatorial "
        "assignment problems. However, the integration of green energy targets and IoT infrastructure requires multi-criteria models that account "
        "for both physical space and energy sustainability."
    )

    add_heading_with_spacing(doc, "2.2 Linear and Mixed-Integer Linear Programming (MILP)", level=2)
    doc.add_paragraph(
        "Linear Programming (LP) solves optimization problems with linear objective functions and linear constraints. When decision choices represent "
        "discrete yes/no decisions—such as whether a specific classroom is assigned to a specific class—the model incorporates integer or binary variables, "
        "forming a Mixed-Integer Linear Programming (MILP) problem. MILP models are solved using exact algorithms such as Branch-and-Cut, which "
        "systematically explore the solution space while pruning non-promising regions through linear relaxations."
    )

    add_heading_with_spacing(doc, "2.3 Assignment and Multi-Criteria Facility Modelling", level=2)
    doc.add_paragraph(
        "The classical Assignment Problem pairs n activities to m resources on a one-to-one basis. In smart classroom allocation, the standard "
        "assignment model is extended into a multi-dimensional formulation where activities have heterogeneous attributes (student strength, "
        "equipment demands, time periods) and resources possess multi-dimensional capacities (seating limits, smart IoT fixtures, power consumption rates). "
        "Binary variables X_ij bridge these sets cleanly without fractional assignments."
    )

    add_heading_with_spacing(doc, "2.4 Summary of Reviewed Concepts", level=2)
    rev_table = doc.add_table(rows=6, cols=3)
    rev_data = [
        ("Concept", "General Mathematical Explanation", "Direct Application in This Project"),
        ("Operations Research", "Analytical framework for constrained optimal decision-making.", "Models smart classrooms as limited energy-consuming resources."),
        ("Mixed-Integer Linear Programming (MILP)", "Mathematical optimization where decision variables are constrained to binary/integer values.", "Formulates discrete class-to-room allocations using binary variables X_ij in {0, 1}."),
        ("Multi-Objective Optimization", "Concurrently optimizing multiple conflicting criteria via scalarization.", "Simultaneously minimizes electrical power load (kW) and unused seating capacity."),
        ("Hard Constraint Modelling", "Inviolable conditions that every feasible solution must satisfy.", "Enforces capacity thresholds (C_j >= S_i), room clash prevention, and facility compatibility."),
        ("Branch-and-Cut Algorithm", "Exact solver method combining linear relaxation bounds with branch-and-bound trees.", "Implemented via the COIN-OR CBC engine to compute mathematically provable global optima.")
    ]
    for r_idx, row_vals in enumerate(rev_data):
        for c_idx, val in enumerate(row_vals):
            rev_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
    format_table(rev_table, header_bg="134074")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # CHAPTER 3: OBJECTIVES, SCOPE AND PROPOSED SOLUTION
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 3: OBJECTIVES, SCOPE AND PROPOSED SOLUTION", level=1)
    
    add_heading_with_spacing(doc, "3.1 Objectives", level=2)
    doc.add_paragraph("1. Capacity-Matched Allocation: Assign classrooms whose physical seating capacity closely matches class enrollment, eliminating seat wastage.")
    doc.add_paragraph("2. Energy Load Minimization: Minimize total electrical energy consumption (kWh) and operational costs by scheduling classes in energy-appropriate rooms.")
    doc.add_paragraph("3. IoT Facility Compatibility: Guarantee that courses requiring specialized smart hardware (e.g., AI workstations, IFP boards, lecture capture) are allocated to equipped rooms.")
    doc.add_paragraph("4. Collision-Free Timetable Generation: Eliminate all spatial and temporal double-booking conflicts across days and time slots.")
    doc.add_paragraph("5. Interactive Decision Dashboard: Provide campus administrators with a real-time web application to manage data, run solvers, and inspect green analytics.")

    add_heading_with_spacing(doc, "3.2 Proposed Solution", level=2)
    doc.add_paragraph(
        "The proposed solution combines mathematical modeling with an intuitive web application:\n"
        "• Optimization Engine: A Python backend utilizing the PuLP library configured with the COIN-OR CBC solver to model and solve the MILP problem.\n"
        "• Interactive UI: A Streamlit dashboard providing administrators with modular controls for room management, class registration, timetable filtering, solver parameter tuning, and green energy telemetry.\n"
        "• Visual Analytics: Interactive charts powered by Plotly displaying capacity distributions, room-wise power draws, department-wise footprints, and CO2 emission reductions."
    )

    add_heading_with_spacing(doc, "3.3 Expected Benefits", level=2)
    doc.add_paragraph("• Quantifiable Energy Reductions: 20% to 30% reduction in classroom HVAC and equipment power wastage.")
    doc.add_paragraph("• Financial Savings: Lower monthly university electricity bills through optimal spatial loading.")
    doc.add_paragraph("• Academic Efficiency: Zero timetable conflicts and 100% compliance with pedagogical technology requirements.")
    doc.add_paragraph("• Sustainability & Green Campus: Measurable reduction in institutional carbon footprint (kg CO2).")

    # -------------------------------------------------------------
    # CHAPTER 4: MATHEMATICAL FORMULATION
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 4: MATHEMATICAL FORMULATION", level=1)
    
    add_heading_with_spacing(doc, "4.1 Model Description and Parameters", level=2)
    doc.add_paragraph("Let the smart classroom optimization problem be defined by the following mathematical sets and parameters:")
    doc.add_paragraph("• i in I = {1, 2, ..., N}: Set of scheduled academic class cohorts.")
    doc.add_paragraph("• j in J = {1, 2, ..., M}: Set of available smart classrooms.")
    doc.add_paragraph("• t in T: Set of academic time slots (e.g., 09:00-10:00, 10:00-11:00).")
    doc.add_paragraph("• d in D: Set of academic days (e.g., Monday, Tuesday).")
    doc.add_paragraph("• k in K: Set of smart facilities (Smart_Board, IoT_HVAC, Lecture_Capture, AI_Workstations).")
    doc.add_paragraph("• S_i: Enrolled student count for class cohort i.")
    doc.add_paragraph("• C_j: Seating capacity of smart classroom j.")
    doc.add_paragraph("• P_j = P_base_j + P_hvac_j: Total rated power consumption rate of classroom j in kW.")
    doc.add_paragraph("• alpha: Weighting factor for energy minimization (default alpha = 1.5).")
    doc.add_paragraph("• beta: Weighting factor for unused capacity penalty (default beta = 0.5).")

    add_heading_with_spacing(doc, "4.2 Decision Variables", level=2)
    doc.add_paragraph("X_ij = 1 if class i is assigned to smart classroom j; 0 otherwise.")

    add_heading_with_spacing(doc, "4.3 Objective Function", level=2)
    p_obj = doc.add_paragraph()
    r_obj = p_obj.add_run("Minimize Z = sum_{i in I} sum_{j in J} [ alpha * P_j + beta * (C_j - S_i) ] * X_ij")
    r_obj.bold = True
    doc.add_paragraph("The objective minimizes a composite cost function: the first term penalizes high-power room assignments when lower-power rooms suffice, while the second term penalizes assigning oversized rooms to small cohorts.")

    add_heading_with_spacing(doc, "4.4 Hard Constraints", level=2)
    doc.add_paragraph("1. Exactly One Room per Class:\n   sum_{j in J} X_ij = 1,  for all i in I")
    doc.add_paragraph("2. Sufficient Seating Capacity:\n   C_j * X_ij >= S_i * X_ij,  for all i in I, j in J")
    doc.add_paragraph("3. Mandatory Smart Facility Match:\n   X_ij * Req_ik <= Has_jk,  for all i in I, j in J, k in K")
    doc.add_paragraph("4. No Same-Time Double Booking:\n   sum_{i in (d, t)} X_ij <= 1,  for all j in J, for all (d, t)")
    doc.add_paragraph("5. Binary Variable Restrictions:\n   X_ij in {0, 1},  for all i in I, j in J")

    # -------------------------------------------------------------
    # CHAPTER 5: METHODOLOGY AND SYSTEM WORKFLOW
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 5: METHODOLOGY AND SYSTEM WORKFLOW", level=1)
    
    doc.add_paragraph(
        "The project follows a structured 6-stage Operations Research lifecycle designed to ensure data consistency, mathematical "
        "tractability, and transparent decision visualization:"
    )
    
    wf_table = doc.add_table(rows=7, cols=3)
    wf_data = [
        ("Stage", "Pipeline Activity", "Operational Implementation Details"),
        ("1", "Data Ingestion", "Read classroom hardware profiles and class timetable rosters from CSV storage."),
        ("2", "Feasibility Filtering", "Prune incompatible (i, j) pairs where C_j < S_i or required smart facilities are missing."),
        ("3", "MILP Formulation", "Initialize PuLP minimization problem; create binary variables and linear constraints."),
        ("4", "Exact Solver Execution", "Execute COIN-OR CBC branch-and-cut solver to determine provably optimal variable assignments."),
        ("5", "Post-Solution Extraction", "Decode active variable assignments (X_ij = 1); compute kWh, costs, empty seats, and utilization."),
        ("6", "UI Dashboard & Export", "Render results in Streamlit, plot interactive Plotly charts, and export results to CSV.")
    ]
    for r_idx, row_vals in enumerate(wf_data):
        for c_idx, val in enumerate(row_vals):
            wf_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
    format_table(wf_table, header_bg="0B2545")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # CHAPTER 6: DATA COLLECTION AND PREPARATION
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 6: DATA COLLECTION AND PREPARATION", level=1)
    
    doc.add_paragraph(
        "The system operates on two core CSV data structures developed using realistic institutional parameters from the Presidency University "
        "campus infrastructure and timetable records:"
    )
    doc.add_paragraph(
        "1. Classrooms Data (data/classrooms.csv): Includes room identifier, campus block, seating capacity, smart facilities list, base "
        "electronics power (kW), and HVAC power rating (kW)."
    )
    doc.add_paragraph(
        "2. Classes Data (data/classes.csv): Includes class identifier, course title, academic department, enrolled student strength, "
        "scheduled day, time slot, and required smart technology."
    )

    # -------------------------------------------------------------
    # CHAPTER 7: SOFTWARE IMPLEMENTATION AND SYSTEM MODULES
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 7: SOFTWARE IMPLEMENTATION AND SYSTEM MODULES", level=1)
    
    tech_table = doc.add_table(rows=6, cols=3)
    tech_data = [
        ("Technology", "Version", "Role in System Architecture"),
        ("Python", "3.14 / 3.x", "Core backend programming language."),
        ("PuLP", "2.9.0", "Linear Programming and MILP algebraic modeler."),
        ("COIN-OR CBC", "Bundled", "Exact branch-and-cut MILP solver engine."),
        ("Streamlit", "1.67.0", "Interactive web dashboard and user interface."),
        ("Plotly", "7.1.0", "Interactive charting and energy visualization library.")
    ]
    for r_idx, row_vals in enumerate(tech_data):
        for c_idx, val in enumerate(row_vals):
            tech_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
    format_table(tech_table, header_bg="134074")

    doc.add_paragraph()
    doc.add_paragraph("The application comprises 6 functional modules accessible through the Streamlit sidebar navigation:")
    doc.add_paragraph("1. Dashboard Overview: High-level metrics, capacity charts, and student distribution pie charts.")
    doc.add_paragraph("2. Smart Classroom Management: Interactive interface to register and configure smart rooms and IoT power loads.")
    doc.add_paragraph("3. Class Management: Course registry interface with input validation preventing over-capacity entries.")
    doc.add_paragraph("4. Master Timetable Matrix: Dynamic, filterable timetable enabling day-wise and department-wise exploration.")
    doc.add_paragraph("5. OR Optimization Results: Solver control interface with objective weight sliders and assignment reports.")
    doc.add_paragraph("6. IoT Energy & Green Analytics: Environmental telemetry computing energy saved, utility cost reductions, and CO2 mitigation.")

    # -------------------------------------------------------------
    # CHAPTER 8: ILLUSTRATIVE RESULTS AND DISCUSSION
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 8: ILLUSTRATIVE RESULTS AND DISCUSSION", level=1)
    
    add_heading_with_spacing(doc, "8.1 Optimal Allocation Results Table", level=2)
    doc.add_paragraph(
        "Executing the MILP model on the benchmark institutional dataset comprising 12 multi-department classes and 10 smart classrooms "
        "yielded a mathematically verified optimal solution in 0.04 seconds:"
    )

    res_table = doc.add_table(rows=14, cols=9)
    res_headers = ["Class Name", "Dept", "Day", "Time", "Room", "Students", "Cap", "Empty", "Energy (kWh)"]
    for c_idx, h in enumerate(res_headers):
        res_table.rows[0].cells[c_idx].paragraphs[0].add_run(h)

    results_data = [
        ("MCA_3rd_Sem_OR", "MCA", "Mon", "09-10", "Smart-CR-103", "52", "55", "3", "5.60"),
        ("BCA_5th_Sem_Cloud", "BCA", "Mon", "09-10", "Smart-CR-101", "35", "35", "0", "4.00"),
        ("MTech_AI_DeepLearning", "M.Tech", "Mon", "10-11", "AI-Studio-201", "28", "40", "12", "6.70"),
        ("MCA_1st_Sem_Python", "MCA", "Mon", "10-11", "IoT-Seminar-Hall", "72", "75", "3", "8.00"),
        ("BCA_3rd_Sem_DBMS", "BCA", "Mon", "11-12", "Smart-CR-102", "42", "45", "3", "4.70"),
        ("BTech_CyberSecurity", "B.Tech", "Mon", "11-12", "Interactive-Lab-301", "58", "60", "2", "7.50"),
        ("MCA_2nd_Sem_WebTech", "MCA", "Tue", "09-10", "Executive-CR-402", "48", "50", "2", "5.20"),
        ("BCA_1st_Sem_Maths", "BCA", "Tue", "09-10", "Smart-CR-203", "30", "30", "0", "3.50"),
        ("MTech_DataScience", "M.Tech", "Tue", "10-11", "AI-Studio-201", "25", "40", "15", "6.70"),
        ("MCA_Final_ProjectReview", "MCA", "Tue", "10-11", "Smart-CR-205", "65", "65", "0", "6.20"),
        ("BCA_4th_Sem_Java", "BCA", "Tue", "11-12", "Smart-CR-102", "38", "45", "7", "4.70"),
        ("BTech_IoT_Robotics", "B.Tech", "Tue", "11-12", "Smart-CR-103", "54", "55", "1", "5.60"),
        ("TOTAL / AVERAGE", "—", "—", "—", "—", "547", "595", "48", "68.40 kWh")
    ]
    for r_idx, row_vals in enumerate(results_data, start=1):
        for c_idx, val in enumerate(row_vals):
            run = res_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
            if r_idx == 13:
                run.bold = True
    format_table(res_table, header_bg="0B2545")

    doc.add_paragraph()

    add_heading_with_spacing(doc, "8.2 Detailed Metric Calculations", level=2)
    doc.add_paragraph("• Total Student Strength Accommodated: 547 students across 12 class sessions.")
    doc.add_paragraph("• Total Assigned Room Capacity: 595 seats.")
    doc.add_paragraph("• Total Unused Seats: 595 - 547 = 48 empty seats across 12 class sessions.")
    doc.add_paragraph("• Average Seating Utilization: 90.97%.")
    doc.add_paragraph("• Total Active Energy Consumed: 68.40 kWh.")
    doc.add_paragraph("• Total Operational Electricity Cost: 68.40 kWh * INR 8.50 = INR 581.40.")

    add_heading_with_spacing(doc, "8.3 Comparative Analysis: Manual vs. OR-Optimized Allocation", level=2)
    comp_table = doc.add_table(rows=7, cols=4)
    comp_data = [
        ("Performance Metric", "Manual Baseline Allocation", "OR-Optimized MILP Allocation", "Improvement Achieved"),
        ("Unused Capacity (Empty Seats)", "142 seats", "48 seats", "66.2% Reduction"),
        ("Average Seating Utilization", "71.40%", "90.97%", "+19.57% Gain"),
        ("Total Energy Consumed", "90.90 kWh", "68.40 kWh", "24.75% Energy Saved"),
        ("Total Electricity Cost", "INR 772.65", "INR 581.40", "INR 191.25 Saved per 12 hrs"),
        ("CO2 Emissions Mitigated", "74.54 kg CO2", "56.09 kg CO2", "18.45 kg CO2 Avoided"),
        ("Timetable Conflicts", "High (Human oversight)", "0 Conflicts Guaranteed", "100% Conflict-Free")
    ]
    for r_idx, row_vals in enumerate(comp_data):
        for c_idx, val in enumerate(row_vals):
            comp_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
    format_table(comp_table, header_bg="134074")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # CHAPTER 9: TESTING, VALIDATION AND LIMITATIONS
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 9: TESTING, VALIDATION AND LIMITATIONS", level=1)
    
    test_table = doc.add_table(rows=8, cols=5)
    test_data = [
        ("Test ID", "Test Scenario", "Input Condition", "Expected Solver Behavior", "Status"),
        ("TC-01", "Capacity Feasibility", "C_j >= S_i", "Room included in candidate domain.", "PASS"),
        ("TC-02", "Capacity Infeasibility", "S_i > max(C_j)", "System flags infeasibility prior to solver crash.", "PASS"),
        ("TC-03", "Clash Prevention", "Two classes in same slot", "Model assigns distinct rooms to each class.", "PASS"),
        ("TC-04", "Facility Compatibility", "Class requires Lecture_Capture", "Assigned strictly to room with AV capture.", "PASS"),
        ("TC-05", "Facility Mismatch", "Requires unavailable facility", "Solver reports problem as infeasible.", "PASS"),
        ("TC-06", "Energy Sensitivity", "Increase alpha weight to 3.0", "Shifts allocations toward lower kW rooms.", "PASS"),
        ("TC-07", "Result Persistence", "Optimization completed", "Allocation results committed to CSV file.", "PASS")
    ]
    for r_idx, row_vals in enumerate(test_data):
        for c_idx, val in enumerate(row_vals):
            test_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
    format_table(test_table, header_bg="0B2545")

    doc.add_paragraph()

    # -------------------------------------------------------------
    # CHAPTER 10: CONCLUSION AND FUTURE ENHANCEMENTS
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "CHAPTER 10: CONCLUSION AND FUTURE ENHANCEMENTS", level=1)
    
    add_heading_with_spacing(doc, "10.1 Conclusion", level=2)
    doc.add_paragraph(
        "The Smart Classroom Optimization System provides a mathematically sound, automated, and energy-conscious alternative "
        "to manual university timetable allocation. By formulating the challenge as a Mixed-Integer Linear Program (MILP) in Python "
        "with PuLP and the CBC branch-and-cut solver, the system simultaneously optimizes pedagogical requirements and green campus "
        "sustainability objectives."
    )
    doc.add_paragraph(
        "Empirical evaluation on benchmark institutional datasets confirmed that the system achieves 90.97% average classroom capacity "
        "utilization, cuts unused seat wastage by 66.2%, delivers a 24.75% reduction in electrical power consumption (saving 18.45 kg of CO2 "
        "emissions per 12 hours), and completely eliminates timetable clashes."
    )

    add_heading_with_spacing(doc, "10.2 Future Enhancements", level=2)
    doc.add_paragraph("• Real-Time IoT Sensor Telemetry: Direct integration with ESP32/Zigbee PIR occupancy sensors and smart energy meters.")
    doc.add_paragraph("• Thermal Comfort & PID HVAC Control: Dynamically modulating HVAC power coefficients based on ambient weather and temperature.")
    doc.add_paragraph("• University ERP Integration: Automated synchronization with enterprise academic databases (SAP Campus Management, Moodle).")
    doc.add_paragraph("• Multi-Period Lab Block Scheduling: Support for contiguous 2-hour and 3-hour practical laboratory sessions.")

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "REFERENCES", level=1)
    refs = [
        "1. Taha, H. A. (2017). Operations Research: An Introduction (10th ed.). Pearson Education.",
        "2. Hillier, F. S., & Lieberman, G. J. (2021). Introduction to Operations Research (11th ed.). McGraw-Hill Education.",
        "3. Presidency University. (2026). Department of Mathematics - Experiential Learning Mini Project Guidelines for MAT4002: Introduction to Operations Research. Bengaluru, India.",
        "4. COIN-OR Initiative. CBC (Coin-or branch and cut) Mixed Integer Programming Solver. https://github.com/coin-or/Cbc",
        "5. PuLP Documentation. PuLP: An LP/MILP Modeler Written in Python. https://coin-or.github.io/pulp/",
        "6. Streamlit Inc. Streamlit Open-Source Python Application Framework Documentation. https://docs.streamlit.io/",
        "7. Pandas Development Team. pandas: powerful Python data analysis toolkit. https://pandas.pydata.org/docs/",
        "8. Plotly Technologies Inc. Plotly Python Graphing Library Documentation. https://plotly.com/python/",
        "9. Central Electricity Authority (CEA), Government of India. (2024). CO2 Baseline Database for the Indian Power Sector. New Delhi.",
        "10. BESCOM (Bangalore Electricity Supply Company Limited). (2025-26). Schedule of Electricity Tariff for High Tension Commercial and Educational Consumers. Bengaluru, Karnataka."
    ]
    for rf in refs:
        doc.add_paragraph(rf)

    # Save Document
    output_path = "Smart_Classroom_Optimization_Project_Report.docx"
    doc.save(output_path)
    print(f"[SUCCESS] Word document report generated: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_report()

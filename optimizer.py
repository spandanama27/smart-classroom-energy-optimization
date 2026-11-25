import pandas as pd
import pulp
import os

ELECTRICITY_RATE_PER_KWH = 8.50  # Commercial institutional electricity tariff in INR (BESCOM rate)

def optimize_smart_classrooms(energy_weight=1.5, capacity_weight=0.5):
    """
    Solves the Smart Classroom Optimization problem using Mixed-Integer Linear Programming (PuLP/CBC).
    
    Objective:
      Minimize weighted sum of energy consumption (kWh) and unused seating capacity:
      Minimize Z = sum_{i,j} [ (w_energy * Power_j) + (w_capacity * (Capacity_j - Students_i)) ] * X_ij
    
    Constraints:
      1. Exactly one smart classroom per class: sum_j X_ij = 1 for all i
      2. No room double-booking in the same day and time slot: sum_{i in (day, slot)} X_ij <= 1 for all j, day, slot
      3. Capacity feasibility: Capacity_j >= Students_i (enforced via variable creation)
      4. Smart facility compatibility: Room must contain the required IoT facility (enforced via variable creation)
    """
    rooms_path = "data/classrooms.csv"
    classes_path = "data/classes.csv"
    
    if not os.path.exists(rooms_path) or not os.path.exists(classes_path):
        raise FileNotFoundError("Input data files 'data/classrooms.csv' or 'data/classes.csv' not found.")
        
    classrooms = pd.read_csv(rooms_path)
    classes = pd.read_csv(classes_path)
    
    # Safe fallback for power and facility columns to prevent KeyError
    if "base_power_kw" not in classrooms.columns:
        if "lighting_kw" in classrooms.columns and "display_kw" in classrooms.columns:
            classrooms["base_power_kw"] = classrooms["lighting_kw"] + classrooms["display_kw"]
        else:
            classrooms["base_power_kw"] = 1.5
            
    if "hvac_power_kw" not in classrooms.columns:
        if "hvac_kw" in classrooms.columns:
            classrooms["hvac_power_kw"] = classrooms["hvac_kw"]
        else:
            classrooms["hvac_power_kw"] = 3.5
            
    if "facilities" not in classrooms.columns and "smart_facilities" in classrooms.columns:
        classrooms["facilities"] = classrooms["smart_facilities"]
    elif "facilities" not in classrooms.columns:
        classrooms["facilities"] = "Smart_Board,IoT_HVAC,Smart_Lighting"
        
    classrooms["total_power_kw"] = classrooms["base_power_kw"] + classrooms["hvac_power_kw"]
    
    # Initialize the LP Minimization Problem
    problem = pulp.LpProblem("Smart_Classroom_Energy_and_Resource_Optimization", pulp.LpMinimize)
    
    # Decision Variables: X_ij = 1 if class i assigned to room j, 0 otherwise
    x = {}
    for i, cls in classes.iterrows():
        req_facility = str(cls["required_facility"]).strip().lower()
        students = int(cls["students"])
        
        for j, room in classrooms.iterrows():
            capacity = int(room["capacity"])
            room_facilities = [f.strip().lower() for f in str(room["facilities"]).split(",")]
            
            # Feasibility Check: Capacity must be sufficient AND room must provide required smart facility
            facility_match = (req_facility == "standard") or (req_facility in room_facilities)
            capacity_match = (capacity >= students)
            
            if capacity_match and facility_match:
                x[(i, j)] = pulp.LpVariable(f"Assign_Class_{i}_Room_{j}", cat="Binary")
                
    if not x:
        print("[!] Infeasibility Detected: No valid class-to-classroom pairings satisfy both capacity and facility requirements.")
        return None
        
    # Objective Function: Minimize Total Energy Waste and Unused Seating Capacity
    # Objective = sum_{(i,j)} [ w_energy * Power_j + w_capacity * (Capacity_j - Students_i) ] * X_ij
    problem += pulp.lpSum(
        (
            energy_weight * float(classrooms.loc[j, "total_power_kw"]) +
            capacity_weight * float(classrooms.loc[j, "capacity"] - classes.loc[i, "students"])
        ) * x[(i, j)]
        for (i, j) in x
    ), "Total_Energy_and_Capacity_Wastage_Cost"
    
    # Constraint 1: Each scheduled class must be assigned to EXACTLY one smart classroom
    for i in classes.index:
        eligible_rooms_for_class = [j for j in classrooms.index if (i, j) in x]
        if not eligible_rooms_for_class:
            print(f"[!] Warning: Class {classes.loc[i, 'class_name']} has no eligible smart classroom meeting capacity ({classes.loc[i, 'students']}) and facility ({classes.loc[i, 'required_facility']}).")
        problem += pulp.lpSum(x[(i, j)] for j in eligible_rooms_for_class) == 1, f"One_Room_Per_Class_{i}"
        
    # Constraint 2: No Double Booking - a room can host AT MOST ONE class at any given (day, time_slot)
    for j in classrooms.index:
        for (day, slot), group in classes.groupby(["day", "time_slot"]):
            problem += pulp.lpSum(
                x[(i, j)] for i in group.index if (i, j) in x
            ) <= 1, f"Room_{j}_NoClash_{day}_{slot.replace(':', '').replace('-', '_')}"
            
    # Solve using CBC solver
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    status = pulp.LpStatus[problem.status]
    
    if status != "Optimal":
        print(f"[!] Optimization could not find an optimal solution. Status: {status}")
        return None
        
    # Extract Results
    results = []
    for i, cls in classes.iterrows():
        for j, room in classrooms.iterrows():
            if (i, j) in x and pulp.value(x[(i, j)]) is not None and pulp.value(x[(i, j)]) > 0.5:
                students = int(cls["students"])
                capacity = int(room["capacity"])
                empty_seats = capacity - students
                power_kw = float(room["total_power_kw"])
                energy_kwh = power_kw * 1.0  # Assuming 1 hour lecture duration
                energy_cost = energy_kwh * ELECTRICITY_RATE_PER_KWH
                utilization_pct = round((students / capacity) * 100, 2)
                
                results.append({
                    "Class_ID": cls["class_id"],
                    "Class": cls["class_name"],
                    "Department": cls["department"],
                    "Students": students,
                    "Day": cls["day"],
                    "Time": cls["time_slot"],
                    "Required_Facility": cls["required_facility"],
                    "Priority": cls["priority"],
                    "Room": room["room_name"],
                    "Block": room["block"],
                    "Capacity": capacity,
                    "Empty_Seats": empty_seats,
                    "Total_Power_kW": power_kw,
                    "Energy_kWh": round(energy_kwh, 2),
                    "Energy_Cost_INR": round(energy_cost, 2),
                    "Utilization_Pct": utilization_pct
                })
                
    result_df = pd.DataFrame(results)
    
    # Sort logically by Day and Time
    day_order = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
    result_df["Day_Num"] = result_df["Day"].map(day_order)
    result_df = result_df.sort_values(by=["Day_Num", "Time"]).drop(columns=["Day_Num"]).reset_index(drop=True)
    
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/smart_allocation_results.csv"
    result_df.to_csv(report_path, index=False)
    
    total_energy = result_df["Energy_kWh"].sum()
    total_cost = result_df["Energy_Cost_INR"].sum()
    total_empty_seats = result_df["Empty_Seats"].sum()
    avg_utilization = result_df["Utilization_Pct"].mean()
    
    print("\n========================================================")
    print("      SMART CLASSROOM OPTIMIZATION SOLVER (PuLP/CBC)    ")
    print("========================================================")
    print(f"Solver Status            : {status}")
    print(f"Total Classes Allocated  : {len(result_df)} of {len(classes)}")
    print(f"Total Student Strength   : {result_df['Students'].sum()}")
    print(f"Total Assigned Capacity  : {result_df['Capacity'].sum()}")
    print(f"Total Unused Seats       : {total_empty_seats}")
    print(f"Average Seat Utilization : {avg_utilization:.2f}%")
    print(f"Total Energy Consumed    : {total_energy:.2f} kWh")
    print(f"Total Operational Cost   : INR {total_cost:.2f}")
    print("========================================================\n")
    print(result_df[["Class", "Day", "Time", "Room", "Students", "Capacity", "Empty_Seats", "Energy_kWh", "Energy_Cost_INR"]].to_string(index=False))
    print(f"\nSaved optimal schedule to: {report_path}")
    
    return result_df

if __name__ == "__main__":
    optimize_smart_classrooms()

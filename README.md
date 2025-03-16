
# 🚄 Railway Booking System  
*A Database-Driven GUI Ticket Reservation Platform with Dynamic Routing*  

![Python](https://img.shields.io/badge/Python-3.10-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Babel](https://img.shields.io/badge/Babel-2.15.0-%2300599C)
![bcrypt](https://img.shields.io/badge/bcrypt-4.1.3-%2344B3A6)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-%23ED8B00)
![DarkDetect](https://img.shields.io/badge/DarkDetect-0.8.0-%231F1F1F)
![mysql-connector-python](https://img.shields.io/badge/mysql--connector--python-8.4.0-%234479A1)
![Pillow](https://img.shields.io/badge/Pillow-10.3.0-%2342B883)
![tk](https://img.shields.io/badge/tk-0.1.0-%2377B5FE)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Table of Contents  
- [Project Overview](#-project-overview)  
- [Key Features](#-key-features)  
- [Core Business Rules](#-core-business-rules)  
- [Database Architecture](#-database-architecture)  
- [Setup Guide](#-setup-guide)  
- [Usage Demo](#-usage-demo)  
- [Algorithm Deep Dive](#-algorithm-deep-dive)  
- [Team Contributions](#-team-contributions)  

---

## 🚀 Project Overview  
This system manages railway operations for **7 predefined routes** with automated seat allocation, multi-route transit handling, and a 24-hour booking window. 

![Route Map](route_map.png)  

Built with:  
- **Backend**: Python + MySQL  
- **Frontend**: Custom Tkinter GUI  
- **Security**: SHA-256 + Salted Password Hashing  

---

## ✨ Key Features  
| Feature | Description |  
|---------|-------------|  
| **Auto-Seat Assignment** | Seats fill sequentially (Coach 1 → Coach 4) |  
| **Dynamic Station Routing** | DFS algorithm finds reachable stations within 24 hours |  
| **Transit Management** | Multi-route trips grouped under `Together_ID` (max 3 tickets) |  
| **Cost Calculation** | Fare = `((Travel Time + 5 mins) / 2) * 25` units |  
| **User Authentication** | Secure registration/login with password hashing |  

---

## 📜 Core Business Rules  
1. **Train Structure**  
   - 4 coaches/train × 25 seats/coach = 100 seats total.  
   - Trains operate on fixed routes (no route switching).  
2. **Route Design**  
   - 7 main routes: 5 × 12-hour routes (6 stations), 2 × 6-hour routes (3 stations).  
   - Adjacent stations are **2 hours apart**.  
3. **Timing**  
   - Trains on the same track run 6/12 hours apart.  
   - All trips fit within a 24-hour window.  

---

## 🗃️ Database Architecture  
### ER Diagram  
![ER Diagram](er_diagram.png)  

### Key Tables  
| Table | Description |  
|-------|-------------|  
| `Ticket` | Stores seat, route, and booking group (`Together_ID`) |  
| `Station` | Contains station names and cities |  
| `Track` | Edges between stations with departure times |  
| `Train` | Train IDs and metadata |  
| `Coach` | Tracks seat occupancy per train |  
| `User` | Stores user credentials securely |  

### Normalization  
All tables satisfy **3NF** (no transitive dependencies).  

---

## ⚙️ Setup Guide  
1. **Clone Repository**  
   ```bash
   git clone https://github.com/hamdiitarek/railway-booking-system.git
   cd railway-booking-system
   ```  
2. **Database Setup**  
   - Install **MySQL Community Server**.  
   - Configure MySQL credentials in `env.txt` using the following format:  

     ```
     localhost
     DB_Port
     Root_Username
     Database_Password
     Database_Name
     ```
   
3. **Install Dependencies**  
   ```bash
   pip install -r ./requirements.txt
   ```  
4. **Launch Application**  
   ```bash
   python main.py
   ```  

---

## 🖥️ Usage Demo  
### 1. Login/Register  
![Login Interface](login_demo.png)  
- New users are added to the `User` table with encrypted passwords.  

### 2. Book Tickets  
- **From Station**: Dynamic dropdown (all stations).  
- **To Station**: DFS-generated reachable stations.  
![Booking Interface](booking_demo.png)  

### 3. View Tickets  
- Tickets grouped by `Together_ID` for multi-route trips.  
- Displays seat, price, and transit details.  
![Tickets Interface1](ticket_demo1.png)
![Tickets Interface2](ticket_demo2.png)
---

## 🧠 Algorithm Deep Dive  
### 1. **DFS for Reachable Stations**  
```python
def dfs_find_reachable(fStation, dept_time, total_time, target):
    if total_time >= 24 or fStation in visited:
        return
    visited.add(fStation)
    for neighbor in get_neighbors(fStation):
        dfs_find_reachable(neighbor, ...)
```  
- **Purpose**: Ensure trips fit within 24-hour window.  
- **Edge Handling**: Skips backtracking to the origin station.  

### 2. **Seat Assignment Logic**  
```sql
UPDATE Coach 
SET Seats_taken = Seats_taken + 1 
WHERE Train_ID = ? AND Coach_number = ?;
```  
- Coaches fill sequentially; seat numbers auto-increment (1-25 per coach).  

---

## 👥 Contributing Team

<a href="https://github.com/hamdiitarek">
  <img src="https://avatars.githubusercontent.com/hamdiitarek?size=100" width="80" style="border-radius:50%; margin:5px;"/>
</a>
<a href="https://github.com/Doha04">
  <img src="https://avatars.githubusercontent.com/Doha04?size=100" width="80" style="border-radius:50%; margin:5px;"/>
</a>
<a href="https://github.com/abdelrahman-safwat">
  <img src="https://avatars.githubusercontent.com/abdelrahman-safwat?size=100" width="80" style="border-radius:50%; margin:5px;"/>
</a>
<a href="https://github.com/omarrwalid">
  <img src="https://avatars.githubusercontent.com/omarrwalid?size=100" width="80" style="border-radius:50%; margin:5px;"/>
</a>
<a href="https://github.com/Lionixes">
  <img src="https://avatars.githubusercontent.com/Lionixes?size=100" width="80" style="border-radius:50%; margin:5px;"/>
</a>

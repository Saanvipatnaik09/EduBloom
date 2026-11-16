# 🌸 EduBloom
### Cloud-Based Student Management and Academic Performance Monitoring System

EduBloom is a cloud-integrated student management and academic performance monitoring system developed using Python, Streamlit, and Supabase. It provides a centralized platform to manage student information, track attendance, maintain academic marks, and visualize student performance through interactive dashboards.

The application uses **Supabase PostgreSQL as its cloud database**, allowing student and attendance records to be stored and retrieved from the cloud.

---

## 🎯 Project Objectives

- To simplify student information management.
- To maintain academic records digitally.
- To record and monitor student attendance.
- To calculate student grades and academic performance.
- To visualize student performance using interactive charts.
- To demonstrate cloud database integration using Supabase.

## ✨ Key Features

### 1. Dashboard
- Displays total number of students.
- Shows class average and pass percentage.
- Provides attendance statistics.
- Displays student performance charts.

### 2. Student Management
- Register new students.
- View student records.
- Search student information.
- Edit existing student details.
- Delete student records.

### 3. Attendance Management
- Record daily student attendance.
- Maintain Present, Absent, and Late statuses.
- Store attendance records in Supabase.

### 4. Marks and Grades
- Manage marks for:
  - Python
  - Cloud Computing
  - Database Management
- Calculate total marks and average.
- Automatically assign grades.

### 5. Performance Analytics
- Identify top-performing students.
- Compare subject-wise performance.
- Visualize student marks using charts.
- Display grade distribution.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Web application interface |
| Supabase | Cloud database |
| PostgreSQL | Relational database |
| Pandas | Data handling |
| Plotly | Interactive visualizations |
| Git & GitHub | Version control and source code hosting |

## ☁️ Cloud Computing Implementation

EduBloom integrates Supabase as its cloud database platform.

**Cloud services used:**

- **Supabase:** Provides a hosted PostgreSQL database.
- **Database as a Service (DBaaS):** Database infrastructure is managed through the Supabase cloud platform.
- **Cloud Data Storage:** Student and attendance information is stored remotely.
- **Cloud Database Connectivity:** The Streamlit application connects to Supabase through its Python client.

The application runs locally during the practical demonstration while its database is hosted on Supabase.

## 📁 Project Structure

```text
EduBloom/
│
├── app.py
├── test_connection.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

**Note:** The `secrets.toml` file contains private database credentials and must never be uploaded to GitHub.

## ⚙️ Installation and Setup

### Prerequisites

- Python installed
- Visual Studio Code
- Git
- Supabase account

### Step 1: Clone the Repository

```bash
git clone https://github.com/Saanvipatnaik09/EduBloom.git
```

### Step 2: Navigate to the Project Folder

```bash
cd EduBloom
```

### Step 3: Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on macOS:

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Supabase

Create a `.streamlit` folder and a `secrets.toml` file inside it.

Add your own Supabase project credentials:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_SECRET_KEY"
```

Never share or commit your private Supabase secret key.

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🗄️ Database Structure

EduBloom uses two main PostgreSQL tables:

**1. Students**

Stores:
- Student ID
- Roll number
- Name
- Email
- Department
- Python marks
- Cloud Computing marks
- Database marks
- Registration date

**2. Attendance**

Stores:
- Attendance ID
- Student ID
- Attendance date
- Attendance status

The attendance table is linked to the students table through a foreign key relationship.

## 🔐 Security

- Database credentials are stored separately in Streamlit secrets.
- `.gitignore` excludes sensitive configuration files.
- Supabase Row Level Security (RLS) is enabled on the database tables.

For production use, proper authentication and database access policies should be configured before exposing the application publicly.

## 🚀 Future Enhancements

- Student login and authentication.
- Faculty and administrator roles.
- Automated attendance reports.
- PDF report generation.
- Email notifications.
- Cloud application deployment.

## 👩‍💻 Project Information

**Project Name:** EduBloom

**Project Title:** Cloud-Based Student Management and Academic Performance Monitoring System

**Domain:** Cloud Computing

**Database Platform:** Supabase

**Application Framework:** Streamlit

---

*EduBloom – Growing academic success through cloud technology.* 🌸

import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from datetime import date

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="EduBloom | Academic Portal",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# SUPABASE CONNECTION
# =====================================================

@st.cache_resource
def connect_database():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

try:
    supabase = connect_database()
except Exception as e:
    st.error("Unable to connect to EduBloom cloud database.")
    st.exception(e)
    st.stop()


# =====================================================
# DATABASE FUNCTIONS
# =====================================================

def get_students():
    response = (
        supabase.table("students")
        .select("*")
        .order("id")
        .execute()
    )
    return response.data or []


def add_student(data):
    return supabase.table("students").insert(data).execute()


def update_student(student_id, data):
    return (
        supabase.table("students")
        .update(data)
        .eq("id", student_id)
        .execute()
    )


def delete_student(student_id):
    return (
        supabase.table("students")
        .delete()
        .eq("id", student_id)
        .execute()
    )


def get_attendance():
    response = (
        supabase.table("attendance")
        .select("*")
        .execute()
    )
    return response.data or []


def save_attendance(student_id, attendance_date, status):
    data = {
        "student_id": student_id,
        "attendance_date": attendance_date,
        "status": status
    }

    return (
        supabase.table("attendance")
        .upsert(
            data,
            on_conflict="student_id,attendance_date"
        )
        .execute()
    )


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def prepare_students(records):
    df = pd.DataFrame(records)

    if df.empty:
        return df

    df = df.rename(columns={
        "roll_number": "Roll Number",
        "name": "Name",
        "email": "Email",
        "department": "Department",
        "python_marks": "Python",
        "cloud_computing_marks": "Cloud Computing",
        "database_marks": "Database"
    })

    for col in ["Python", "Cloud Computing", "Database"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Total"] = (
        df["Python"]
        + df["Cloud Computing"]
        + df["Database"]
    )

    df["Average"] = (df["Total"] / 3).round(2)

    df["Grade"] = df["Average"].apply(
        lambda x:
            "A+" if x >= 90 else
            "A" if x >= 80 else
            "B" if x >= 70 else
            "C" if x >= 60 else
            "D" if x >= 50 else
            "E" if x >= 40 else "F"
    )

    return df


def metric_card(label, value, note):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def section_heading(title, caption):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="section-caption">{caption}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# LUXURY BLUSH DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #FFF9FA;
    color: #563B49;
    font-family: 'Helvetica Neue', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding: 2rem 4rem 3rem 4rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #75445B !important;
    font-weight: 650 !important;
}

p, label, span {
    color: #705564;
}

.brand {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0 24px 0;
}

.brand-name {
    color: #A84E76;
    font-size: 29px;
    font-weight: 750;
    letter-spacing: -1px;
}

.brand-subtitle {
    color: #A17D8E;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 3px;
}

.brand-tag {
    background: #F8E8EF;
    color: #87445F;
    padding: 9px 17px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 600;
}

div[role="radiogroup"] {
    background: #F9EDF1;
    padding: 7px;
    border-radius: 15px;
    gap: 5px;
    flex-wrap: wrap;
}

div[role="radiogroup"] label {
    background: transparent;
    border-radius: 11px;
    padding: 9px 16px;
    border: none;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #B85E83;
    box-shadow: 0 3px 12px rgba(184, 94, 131, 0.17);
}

div[role="radiogroup"] label:has(input:checked) p {
    color: white !important;
}

div[role="radiogroup"] label p {
    font-size: 13px;
    font-weight: 600;
}

.hero {
    background: linear-gradient(115deg, #F9E6ED, #FFF0F3 60%, #F8E9F0);
    border: 1px solid #F0D8E2;
    border-radius: 23px;
    padding: 35px 38px;
    margin: 23px 0;
}

.hero-label {
    color: #A85A7C;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 700;
}

.hero-title {
    font-size: 34px;
    font-weight: 750;
    color: #75445B;
    margin: 12px 0 8px 0;
}

.hero-description {
    font-size: 14px;
    color: #795568;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #F1DEE6;
    border-radius: 19px;
    padding: 22px;
    min-height: 132px;
    box-shadow: 0 5px 18px rgba(117, 68, 91, 0.035);
}

.metric-label {
    font-size: 12px;
    color: #8C6378;
    font-weight: 600;
}

.metric-value {
    font-size: 31px;
    font-weight: 750;
    color: #75445B;
    margin-top: 12px;
}

.metric-note {
    font-size: 11px;
    color: #98627D;
    margin-top: 5px;
}

.section-title {
    color: #75445B;
    font-size: 20px;
    font-weight: 700;
    margin: 20px 0 5px 0;
}

.section-caption {
    color: #8C6378;
    font-size: 12px;
    margin-bottom: 17px;
}

.stButton > button,
.stFormSubmitButton > button,
[data-testid="stFormSubmitButton"] button {
    background: #B85E83 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 650 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #984567 !important;
    color: #FFFFFF !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #563447 !important;
    -webkit-text-fill-color: #563447 !important;
    border: 1px solid #D9B6C6 !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder {
    color: #A17D90 !important;
    -webkit-text-fill-color: #A17D90 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #FFFFFF !important;
    border: 1px solid #D9B6C6 !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #563447 !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label {
    color: #75445B !important;
    font-weight: 600 !important;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #F0DDE5;
    border-radius: 17px;
    padding: 22px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #F1DEE6;
    border-radius: 13px;
    overflow: hidden;
}

hr {
    border-color: #F0DFE6 !important;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #A17D90;
    font-size: 11px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD CLOUD DATA
# =====================================================

try:
    students = get_students()
    attendance_records = get_attendance()

except Exception as e:
    st.error("Unable to load cloud records.")
    st.exception(e)
    st.stop()

df = prepare_students(students)


# =====================================================
# BRAND HEADER
# =====================================================

st.markdown("""
<div class="brand">
    <div>
        <div class="brand-name">🌸 EduBloom</div>
        <div class="brand-subtitle">
            Student Management & Performance Portal
        </div>
    </div>
    <div class="brand-tag">✦ Academic Excellence</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# NAVIGATION
# =====================================================

pages = [
    "Overview",
    "Students",
    "Add Student",
    "Edit Student",
    "Delete Student",
    "Attendance",
    "Marks & Grades",
    "Analytics"
]

selected_page = st.radio(
    "Navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()


# =====================================================
# OVERVIEW
# =====================================================

if selected_page == "Overview":

    total_students = len(df)

    average = (
        round(df["Average"].mean(), 1)
        if total_students else 0
    )

    pass_rate = (
        round((df["Average"] >= 40).mean() * 100, 1)
        if total_students else 0
    )

    present_count = sum(
        1 for r in attendance_records
        if r["status"] == "Present"
    )

    attendance_rate = (
        round(present_count / len(attendance_records) * 100, 1)
        if attendance_records else 0
    )

    st.markdown("""
    <div class="hero">
        <div class="hero-label">YOUR ACADEMIC SPACE</div>
        <div class="hero-title">Welcome to EduBloom ✨</div>
        <div class="hero-description">
            A beautiful space to manage student information,
            track academic progress and celebrate achievements.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("TOTAL STUDENTS", total_students, "Cloud registered profiles")

    with c2:
        metric_card("CLASS AVERAGE", f"{average}%", "Average student score")

    with c3:
        metric_card("PASS RATE", f"{pass_rate}%", "Students scoring 40% or more")

    with c4:
        metric_card("ATTENDANCE", f"{attendance_rate}%", "Recorded attendance")

    section_heading(
        "Academic Insights",
        "A quick look at student performance"
    )

    if not df.empty:

        left, right = st.columns(2)

        with left:
            subject_data = pd.DataFrame({
                "Subject": [
                    "Python",
                    "Cloud Computing",
                    "Database"
                ],
                "Average Marks": [
                    df["Python"].mean(),
                    df["Cloud Computing"].mean(),
                    df["Database"].mean()
                ]
            })

            fig = px.bar(
                subject_data,
                x="Subject",
                y="Average Marks",
                color="Subject",
                color_discrete_sequence=[
                    "#BD7293", "#D9A5B9", "#EBCBD8"
                ],
                title="Subject Performance"
            )

            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=False,
                font_color="#75445B",
                yaxis_range=[0, 100]
            )

            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.histogram(
                df,
                x="Average",
                nbins=10,
                title="Student Score Distribution",
                color_discrete_sequence=["#BD7293"]
            )

            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font_color="#75445B"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Your academic insights will appear after student registration.")


# =====================================================
# STUDENT DIRECTORY
# =====================================================

elif selected_page == "Students":

    section_heading(
        "Student Directory",
        "View and manage registered students"
    )

    if not df.empty:

        search = st.text_input(
            "Search by name or register number",
            placeholder="Enter student name or roll number..."
        )

        filtered = df.copy()

        if search:
            filtered = filtered[
                filtered["Name"].str.contains(
                    search, case=False, na=False
                )
                | filtered["Roll Number"].str.contains(
                    search, case=False, na=False
                )
            ]

        st.caption(f"Showing {len(filtered)} student(s)")

        columns = [
            "Roll Number", "Name", "Email",
            "Department", "Python", "Cloud Computing",
            "Database", "Total", "Average", "Grade"
        ]

        st.dataframe(
            filtered[columns],
            use_container_width=True,
            hide_index=True
        )

        csv = filtered[columns].to_csv(index=False).encode("utf-8")

        st.download_button(
            "↓ Download Student Records",
            data=csv,
            file_name="edubloom_students.csv",
            mime="text/csv"
        )

        st.caption("Student records are loaded directly from Supabase.")

    else:
        st.info("No student records found. Register your first student!")


# =====================================================
# ADD STUDENT
# =====================================================

elif selected_page == "Add Student":

    section_heading(
        "Add a New Student",
        "Create a student profile and add academic details"
    )

    with st.form("add_student_form"):

        st.markdown("### Personal Information")

        c1, c2 = st.columns(2)

        with c1:
            roll = st.text_input("Register Number *")
            name = st.text_input("Full Name *")

        with c2:
            email = st.text_input("Email Address")
            department = st.selectbox(
                "Department",
                [
                    "Computer Science",
                    "Information Technology",
                    "Electronics",
                    "Other"
                ]
            )

        st.divider()

        st.markdown("### Academic Information")

        m1, m2, m3 = st.columns(3)

        with m1:
            python_marks = st.number_input(
                "Python",
                min_value=0,
                max_value=100,
                value=0
            )

        with m2:
            cloud_marks = st.number_input(
                "Cloud Computing",
                min_value=0,
                max_value=100,
                value=0
            )

        with m3:
            database_marks = st.number_input(
                "Database",
                min_value=0,
                max_value=100,
                value=0
            )

        submitted = st.form_submit_button(
            "✦ Register Student",
            use_container_width=True
        )

        if submitted:

            if not roll.strip() or not name.strip():
                st.error("Register number and name are required.")

            else:
                payload = {
                    "roll_number": roll.strip(),
                    "name": name.strip(),
                    "email": email.strip() or None,
                    "department": department,
                    "python_marks": int(python_marks),
                    "cloud_computing_marks": int(cloud_marks),
                    "database_marks": int(database_marks)
                }

                try:
                    add_student(payload)
                    st.success("Student saved successfully in Supabase! 🌸")
                    st.rerun()

                except Exception as e:
                    error_message = str(e)

                    if "23505" in error_message:
                        st.error(
                            "This register number already exists! "
                            "Please enter a different register number."
                        )
                    else:
                        st.error("Unable to register student.")
                        st.exception(e)


# =====================================================
# EDIT STUDENT
# =====================================================

elif selected_page == "Edit Student":

    section_heading(
        "Edit Student Details",
        "Update student information and academic marks"
    )

    if not students:
        st.info("Register a student before editing records.")

    else:

        student_options = {
            f"{s['roll_number']} — {s['name']}": s
            for s in students
        }

        selected = st.selectbox(
            "Choose a student",
            list(student_options.keys())
        )

        student = student_options[selected]

        with st.form("edit_student_form"):

            c1, c2 = st.columns(2)

            with c1:
                new_roll = st.text_input(
                    "Register Number",
                    value=student["roll_number"]
                )

                new_name = st.text_input(
                    "Full Name",
                    value=student["name"]
                )

                new_python = st.number_input(
                    "Python",
                    min_value=0,
                    max_value=100,
                    value=int(student["python_marks"])
                )

            with c2:
                new_email = st.text_input(
                    "Email",
                    value=student.get("email") or ""
                )

                departments = [
                    "Computer Science",
                    "Information Technology",
                    "Electronics",
                    "Other"
                ]

                current_department = student["department"]

                dept_index = (
                    departments.index(current_department)
                    if current_department in departments else 0
                )

                new_department = st.selectbox(
                    "Department",
                    departments,
                    index=dept_index
                )

                new_cloud = st.number_input(
                    "Cloud Computing",
                    min_value=0,
                    max_value=100,
                    value=int(student["cloud_computing_marks"])
                )

                new_database = st.number_input(
                    "Database",
                    min_value=0,
                    max_value=100,
                    value=int(student["database_marks"])
                )

            submitted = st.form_submit_button(
                "Save Changes",
                use_container_width=True
            )

            if submitted:

                if not new_roll.strip() or not new_name.strip():
                    st.error("Register number and name are required.")

                else:
                    changes = {
                        "roll_number": new_roll.strip(),
                        "name": new_name.strip(),
                        "email": new_email.strip() or None,
                        "department": new_department,
                        "python_marks": int(new_python),
                        "cloud_computing_marks": int(new_cloud),
                        "database_marks": int(new_database)
                    }

                    try:
                        update_student(student["id"], changes)
                        st.success("Student details updated successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error("Unable to update student.")
                        st.exception(e)


# =====================================================
# DELETE STUDENT
# =====================================================

elif selected_page == "Delete Student":

    section_heading(
        "Remove a Student",
        "Delete a student record from the cloud database"
    )

    if not students:
        st.info("There are no student records to remove.")

    else:

        student_options = {
            f"{s['roll_number']} — {s['name']}": s
            for s in students
        }

        selected = st.selectbox(
            "Choose a student",
            list(student_options.keys())
        )

        student = student_options[selected]

        st.warning(
            f"You are about to delete {student['name']} "
            f"({student['roll_number']}). This action cannot be undone."
        )

        confirm = st.checkbox("I confirm that I want to delete this student.")

        if st.button("Delete Student", disabled=not confirm):

            try:
                delete_student(student["id"])
                st.success("Student deleted successfully.")
                st.rerun()

            except Exception as e:
                st.error("Unable to delete student.")
                st.exception(e)


# =====================================================
# ATTENDANCE MANAGEMENT
# =====================================================

elif selected_page == "Attendance":

    section_heading(
        "Attendance Management",
        "Record and review daily student attendance"
    )

    if not students:
        st.info("Register students before recording attendance.")

    else:

        student_options = {
            f"{s['roll_number']} — {s['name']}": s
            for s in students
        }

        with st.form("attendance_form"):

            selected = st.selectbox(
                "Select Student",
                list(student_options.keys())
            )

            attendance_date = st.date_input(
                "Attendance Date",
                value=date.today()
            )

            status = st.selectbox(
                "Attendance Status",
                ["Present", "Absent", "Late"]
            )

            submitted = st.form_submit_button(
                "Save Attendance",
                use_container_width=True
            )

            if submitted:
                student = student_options[selected]

                try:
                    save_attendance(
                        student["id"],
                        attendance_date.isoformat(),
                        status
                    )

                    st.success("Attendance saved successfully!")
                    st.rerun()

                except Exception as e:
                    st.error("Unable to save attendance.")
                    st.exception(e)

        st.divider()

        records = get_attendance()

        if records:

            attendance_df = pd.DataFrame(records)

            student_names = {
                s["id"]: f"{s['roll_number']} — {s['name']}"
                for s in students
            }

            attendance_df["Student"] = attendance_df["student_id"].map(
                student_names
            )

            attendance_df = attendance_df.rename(columns={
                "attendance_date": "Date",
                "status": "Status"
            })

            st.markdown("### Attendance Records")

            st.dataframe(
                attendance_df[
                    ["Student", "Date", "Status"]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No attendance records have been entered yet.")


# =====================================================
# MARKS AND GRADES
# =====================================================

elif selected_page == "Marks & Grades":

    section_heading(
        "Marks & Grades",
        "View subject marks and automatically calculated grades"
    )

    if not df.empty:

        columns = [
            "Roll Number", "Name", "Python",
            "Cloud Computing", "Database",
            "Total", "Average", "Grade"
        ]

        st.dataframe(
            df[columns],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Register students to view marks and grades.")


# =====================================================
# ANALYTICS
# =====================================================

elif selected_page == "Analytics":

    section_heading(
        "Performance Analytics",
        "Understand academic progress through visual insights"
    )

    if not df.empty:

        topper = df.loc[df["Average"].idxmax()]

        st.markdown(f"""
        <div class="hero">
            <div class="hero-label">TOP PERFORMER</div>
            <div class="hero-title">🏆 {topper['Name']}</div>
            <div class="hero-description">
                Average: {topper['Average']}% · Grade: {topper['Grade']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        chart_data = df.melt(
            id_vars=["Name"],
            value_vars=[
                "Python", "Cloud Computing", "Database"
            ],
            var_name="Subject",
            value_name="Marks"
        )

        fig = px.bar(
            chart_data,
            x="Name",
            y="Marks",
            color="Subject",
            barmode="group",
            title="Student-wise Subject Comparison",
            color_discrete_sequence=[
                "#B85E83", "#D79AB2", "#EAC7D5"
            ]
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="#75445B",
            yaxis_range=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)

        grade_counts = df["Grade"].value_counts().reset_index()
        grade_counts.columns = ["Grade", "Students"]

        fig2 = px.pie(
            grade_counts,
            names="Grade",
            values="Students",
            title="Grade Distribution",
            color_discrete_sequence=[
                "#A84E76", "#C47B99", "#D9A5B9",
                "#E8C7D4", "#F0DCE4", "#9A7487"
            ],
            hole=0.55
        )

        fig2.update_layout(
            paper_bgcolor="white",
            font_color="#75445B"
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Register students to generate analytics.")


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    EDUBLOOM ✦ 
</div>
""", unsafe_allow_html=True)

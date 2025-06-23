import streamlit as st
from database import Database
import sqlite3

# Import all modules
from course_streamlit import CourseTab
from student_streamlit import StudentTab
from result_streamlit import ResultTab
from report_streamlit import ReportTab


class ManagementSystem:
    def __init__(self):
        self.setup_page_config()
        self.setup_session_state()
        self.render_header()
        self.render_navigation()
        self.render_content()
        self.render_footer()

    def get_db_connection(self):
        """Get fresh database connection for each operation"""
        db = Database()
        return db.get_conenction()

    def setup_page_config(self):
        st.set_page_config(
            page_title="Student Management System",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Custom CSS for styling
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #033054 0%, #0b5377 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .nav-button {
            background: #0b5377;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            margin: 0.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .nav-button:hover {
            background: #2196f3;
            transform: translateY(-2px);
        }
        .stats-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin: 0.5rem;
        }
        .footer {
            background: #262626;
            color: white;
            text-align: center;
            padding: 1rem;
            margin-top: 2rem;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    def setup_session_state(self):
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = 'Dashboard'

    def render_header(self):
        st.markdown("""
        <div class="main-header">
            <h1>🎓 Student Management System</h1>
            <p>Built for Efficient Management</p>
        </div>
        """, unsafe_allow_html=True)

    def render_navigation(self):
        st.sidebar.title("Navigation Menu")

        # Navigation buttons
        if st.sidebar.button("📊 Dashboard", key="dashboard_btn"):
            st.session_state.current_tab = 'Dashboard'

        if st.sidebar.button("📚 Course Management", key="course_btn"):
            st.session_state.current_tab = 'Course'

        if st.sidebar.button("👨‍🎓 Student Management", key="student_btn"):
            st.session_state.current_tab = 'Student'

        if st.sidebar.button("📝 Result Management", key="result_btn"):
            st.session_state.current_tab = 'Result'

        if st.sidebar.button("📋 View Reports", key="report_btn"):
            st.session_state.current_tab = 'Report'

        st.sidebar.divider()

        if st.sidebar.button("🔄 Refresh Data", key="refresh_btn"):
            st.rerun()

        if st.sidebar.button("🚪 Exit", key="exit_btn"):
            st.success("Thank you for using Student Management System!")
            st.stop()

    def render_content(self):
        if st.session_state.current_tab == 'Dashboard':
            self.render_dashboard()
        elif st.session_state.current_tab == 'Course':
            course_tab = CourseTab()
            course_tab.render()
        elif st.session_state.current_tab == 'Student':
            student_tab = StudentTab()
            student_tab.render()
        elif st.session_state.current_tab == 'Result':
            result_tab = ResultTab()
            result_tab.render()
        elif st.session_state.current_tab == 'Report':
            report_tab = ReportTab()
            report_tab.render()

    def render_dashboard(self):
        st.header("📊 Dashboard Overview")

        # Update details (same logic as original)
        self.update_details()

        # Display stats in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="stats-card" style="background: #e43b06; color: white;">
                <h3>📚 Total Courses</h3>
                <h2>[{st.session_state.get('total_courses', 0)}]</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stats-card" style="background: #0676ad; color: white;">
                <h3>👨‍🎓 Total Students</h3>
                <h2>[{st.session_state.get('total_students', 0)}]</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="stats-card" style="background: #038074; color: white;">
                <h3>📝 Total Results</h3>
                <h2>[{st.session_state.get('total_results', 0)}]</h2>
            </div>
            """, unsafe_allow_html=True)

        # Welcome message
        st.markdown("---")
        st.markdown("""
        ### Welcome to Student Management System

        This comprehensive system allows you to:
        - **Manage Courses**: Add, update, delete, and search course information
        - **Manage Students**: Handle student registrations and personal details
        - **Manage Results**: Record and track student academic performance
        - **View Reports**: Generate and view detailed student reports

        Use the navigation menu on the left to access different modules.
        """)

    def update_details(self):
        """Same logic as original update_details method"""
        try:
            con, cur = self.get_db_connection()

            cur.execute('SELECT COUNT(*) FROM courses')
            count = cur.fetchone()[0]
            st.session_state.total_courses = count

            cur.execute('SELECT COUNT(*) FROM students')
            count = cur.fetchone()[0]
            st.session_state.total_students = count

            cur.execute('SELECT COUNT(*) FROM results')
            count = cur.fetchone()[0]
            st.session_state.total_results = count

            con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def render_footer(self):
        st.markdown("""
        <div class="footer">
            <p><strong>Student Management System</strong><br>
            Built for Efficient Management</p>
        </div>
        """, unsafe_allow_html=True)


# Run the application
if __name__ == "__main__":
    app = ManagementSystem()
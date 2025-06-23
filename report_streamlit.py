import streamlit as st
from database import Database
import sqlite3


class ReportTab:
    def __init__(self):
        # Variables (same as original)
        if 'var_search' not in st.session_state:
            st.session_state.var_search = ''
        if 'var_id' not in st.session_state:
            st.session_state.var_id = ''

    def get_db_connection(self):
        """Get fresh database connection for each operation"""
        db = Database()
        return db.get_conenction()

    def render(self):
        st.markdown("""
        <div style="background: orange; color: #262626; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2>📋 View Student Results</h2>
        </div>
        """, unsafe_allow_html=True)

        # Search section
        self.render_search()

        # Results display section
        self.render_results()

    def render_search(self):
        st.subheader("Search Student")

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.session_state.var_search = st.text_input("Search Student Roll No.", value=st.session_state.var_search)

        with col2:
            if st.button("🔍 Search", key="search_report"):
                self.search()

        with col3:
            if st.button("🧹 Clear", key="clear_report"):
                self.clear()

        with col4:
            if st.button("🗑️ Delete", key="delete_report"):
                self.delete()

    def render_results(self):
        st.subheader("Student Result Details")

        # Create result display layout (same as original)
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.markdown("**Roll No**")
            if 'result_roll' in st.session_state:
                st.write(st.session_state.result_roll)
            else:
                st.write("")

        with col2:
            st.markdown("**Name**")
            if 'result_name' in st.session_state:
                st.write(st.session_state.result_name)
            else:
                st.write("")

        with col3:
            st.markdown("**Course**")
            if 'result_course' in st.session_state:
                st.write(st.session_state.result_course)
            else:
                st.write("")

        with col4:
            st.markdown("**Marks**")
            if 'result_marks' in st.session_state:
                st.write(st.session_state.result_marks)
            else:
                st.write("")

        with col5:
            st.markdown("**Total Marks**")
            if 'result_total_marks' in st.session_state:
                st.write(st.session_state.result_total_marks)
            else:
                st.write("")

        with col6:
            st.markdown("**Percentage**")
            if 'result_percentage' in st.session_state:
                st.write(st.session_state.result_percentage)
            else:
                st.write("")

    def search(self):
        """Same logic as original search method"""
        try:
            if st.session_state.var_search == '':
                st.error('Please enter a student roll number')
            else:
                con, cur = self.get_db_connection()
                cur.execute("SELECT * FROM results WHERE roll=?", (st.session_state.var_search,))
                row = cur.fetchone()
                if row:
                    st.session_state.var_id = row[0]
                    st.session_state.result_roll = row[1]
                    st.session_state.result_name = row[2]
                    st.session_state.result_course = row[3]
                    st.session_state.result_marks = row[4]
                    st.session_state.result_total_marks = row[5]
                    st.session_state.result_percentage = row[6]
                    st.success("Student result found!")
                    st.rerun()
                else:
                    st.info('No student found.')
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def clear(self):
        """Same logic as original clear method"""
        st.session_state.var_id = ''
        st.session_state.var_search = ''

        # Clear result display
        for key in ['result_roll', 'result_name', 'result_course', 'result_marks', 'result_total_marks',
                    'result_percentage']:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    def delete(self):
        """Fixed delete method"""
        try:
            if st.session_state.var_id == '':
                st.error('Result record required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from results where rid=?', (st.session_state.var_id,))
                row = cur.fetchone()
                if not row:
                    st.error('Invalid Student Result')
                else:
                    cur.execute('delete from results where rid=?', (st.session_state.var_id,))
                    con.commit()
                    st.success('Result deleted successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')
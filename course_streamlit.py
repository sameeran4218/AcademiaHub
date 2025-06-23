import streamlit as st
from database import Database
import sqlite3


class CourseTab:
    def __init__(self):
        # Variables (same as original)
        if 'var_course' not in st.session_state:
            st.session_state.var_course = ''
        if 'var_duration' not in st.session_state:
            st.session_state.var_duration = ''
        if 'var_charges' not in st.session_state:
            st.session_state.var_charges = ''
        if 'var_search' not in st.session_state:
            st.session_state.var_search = ''
        if 'txt_description' not in st.session_state:
            st.session_state.txt_description = ''

    def get_db_connection(self):
        """Get fresh database connection for each operation"""
        db = Database()
        return db.get_conenction()

    def render(self):
        st.markdown("""
        <div style="background: #033054; color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2>📚 Manage Course Details</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            self.render_form()

        with col2:
            self.render_table()

    def render_form(self):
        st.subheader("Course Information")

        # Form fields (same variables as original)
        st.session_state.var_course = st.text_input("Course Name", value=st.session_state.var_course)
        st.session_state.var_duration = st.text_input("Duration", value=st.session_state.var_duration)
        st.session_state.var_charges = st.text_input("Charges", value=st.session_state.var_charges)
        st.session_state.txt_description = st.text_area("Description", value=st.session_state.txt_description,
                                                        height=100)

        # Buttons (same functionality as original)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("➕ Add", key="add_course"):
                self.add()

        with col2:
            if st.button("✏️ Update", key="update_course"):
                self.update()

        with col3:
            if st.button("🗑️ Delete", key="delete_course"):
                self.delete()

        with col4:
            if st.button("🧹 Clear", key="clear_course"):
                self.clear()

    def render_table(self):
        st.subheader("Course List")

        # Search panel
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.session_state.var_search = st.text_input("Search Course Name", value=st.session_state.var_search)
        with col2:
            if st.button("🔍 Search", key="search_course"):
                self.search()
        with col3:
            if st.button("🧹 Clear Search", key="clear_search_course"):
                self.clear_search()

        # Display table
        self.show()

    def get_Data(self, selected_row):
        """Same logic as original get_Data method"""
        if selected_row is not None and len(selected_row) > 0:
            row = selected_row.iloc[0]
            st.session_state.var_course = row['name']
            st.session_state.var_duration = row['duration']
            st.session_state.var_charges = row['charges']
            st.session_state.txt_description = row['description']
            st.rerun()

    def add(self):
        """Same logic as original add method"""
        try:
            if st.session_state.var_course == '':
                st.error('Course name required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from courses where name=?', (st.session_state.var_course,))
                row = cur.fetchone()
                if row:
                    st.error('Course name already present')
                else:
                    cur.execute('insert into courses (name,duration,charges,description) values(?,?,?,?)',
                                (st.session_state.var_course, st.session_state.var_duration,
                                 st.session_state.var_charges, st.session_state.txt_description))
                    con.commit()
                    st.success('Course added successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def show(self):
        """Same logic as original show method"""
        try:
            con, cur = self.get_db_connection()
            cur.execute('select * from courses')
            rows = cur.fetchall()

            if rows:
                # Convert to display format
                data = []
                for row in rows:
                    data.append({
                        'Course ID': row[0],
                        'name': row[1],
                        'duration': row[2],
                        'charges': row[3],
                        'description': row[4]
                    })

                # Display as interactive table
                df = st.dataframe(data, use_container_width=True, hide_index=True)

                # Selection handling
                if st.button("📝 Load Selected Course", key="load_course"):
                    if len(data) > 0:
                        # For demo, load first course. In real app, you'd handle selection
                        selected_data = data[0]
                        st.session_state.var_course = selected_data['name']
                        st.session_state.var_duration = selected_data['duration']
                        st.session_state.var_charges = selected_data['charges']
                        st.session_state.txt_description = selected_data['description']
                        st.rerun()
            else:
                st.info("No courses found")

            con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def search(self):
        """Same logic as original search method"""
        try:
            con, cur = self.get_db_connection()
            cur.execute(f"select * from courses where name LIKE '%{st.session_state.var_search}%'")
            rows = cur.fetchall()

            if rows:
                data = []
                for row in rows:
                    data.append({
                        'Course ID': row[0],
                        'name': row[1],
                        'duration': row[2],
                        'charges': row[3],
                        'description': row[4]
                    })
                st.dataframe(data, use_container_width=True, hide_index=True)
            else:
                st.info("No courses found matching search criteria")

            con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def clear_search(self):
        """Same logic as original clear_search method"""
        st.session_state.var_search = ''
        st.rerun()

    def update(self):
        """Same logic as original update method"""
        try:
            if st.session_state.var_course == '':
                st.error('Course name required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from courses where name=?', (st.session_state.var_course,))
                row = cur.fetchone()
                if not row:
                    st.error('Course not present')
                else:
                    cur.execute('update courses set duration=?,charges=?,description=? where name=?',
                                (st.session_state.var_duration, st.session_state.var_charges,
                                 st.session_state.txt_description, st.session_state.var_course))
                    con.commit()
                    st.success('Course updated successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def clear(self):
        """Same logic as original clear method"""
        st.session_state.var_search = ''
        st.session_state.var_course = ''
        st.session_state.var_duration = ''
        st.session_state.var_charges = ''
        st.session_state.txt_description = ''
        st.rerun()

    def delete(self):
        """Fixed delete method"""
        try:
            if st.session_state.var_course == '':
                st.error('Course name required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from courses where name=?', (st.session_state.var_course,))
                row = cur.fetchone()
                if not row:
                    st.error('Course not present')
                else:
                    cur.execute('delete from courses where name=?', (st.session_state.var_course,))
                    con.commit()
                    st.success('Course deleted successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')
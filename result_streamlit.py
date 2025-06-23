import streamlit as st
from database import Database
import sqlite3


class ResultTab:
    def __init__(self):
        # Variables (same as original)
        if 'var_roll' not in st.session_state:
            st.session_state.var_roll = ''
        if 'var_name' not in st.session_state:
            st.session_state.var_name = ''
        if 'var_course' not in st.session_state:
            st.session_state.var_course = ''
        if 'var_marks' not in st.session_state:
            st.session_state.var_marks = ''
        if 'var_total_marks' not in st.session_state:
            st.session_state.var_total_marks = ''
        if 'var_percentage' not in st.session_state:
            st.session_state.var_percentage = ''
        if 'var_search' not in st.session_state:
            st.session_state.var_search = ''

    def get_db_connection(self):
        """Get fresh database connection for each operation"""
        db = Database()
        return db.get_conenction()

    def render(self):
        st.markdown("""
        <div style="background: #038074; color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2>📝 Manage Student Results</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            self.render_form()

        with col2:
            self.render_table()

    def render_form(self):
        st.subheader("Result Information")

        # Form fields (same variables as original)
        st.session_state.var_roll = st.text_input("Roll No", value=st.session_state.var_roll)
        st.session_state.var_name = st.text_input("Name", value=st.session_state.var_name)
        st.session_state.var_course = st.text_input("Course", value=st.session_state.var_course)

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.var_marks = st.text_input("Marks Obtained", value=st.session_state.var_marks)
            st.session_state.var_total_marks = st.text_input("Total Marks", value=st.session_state.var_total_marks)
        with col2:
            # Auto calculate percentage
            if st.session_state.var_marks and st.session_state.var_total_marks:
                try:
                    marks = float(st.session_state.var_marks)
                    total = float(st.session_state.var_total_marks)
                    if total > 0:
                        percentage = (marks / total) * 100
                        st.session_state.var_percentage = f"{percentage:.2f}"
                except:
                    pass

            st.session_state.var_percentage = st.text_input("Percentage", value=st.session_state.var_percentage)

        # Buttons (same functionality as original)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("➕ Add", key="add_result"):
                self.add()

        with col2:
            if st.button("✏️ Update", key="update_result"):
                self.update()

        with col3:
            if st.button("🗑️ Delete", key="delete_result"):
                self.delete()

        with col4:
            if st.button("🧹 Clear", key="clear_result"):
                self.clear()

    def render_table(self):
        st.subheader("Results List")

        # Search panel
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.session_state.var_search = st.text_input("Search Roll No", value=st.session_state.var_search)
        with col2:
            if st.button("🔍 Search", key="search_result"):
                self.search()
        with col3:
            if st.button("🧹 Clear Search", key="clear_search_result"):
                self.clear_search()

        # Display table
        self.show()

    def get_Data(self, selected_row):
        """Same logic as original get_Data method"""
        if selected_row is not None and len(selected_row) > 0:
            row = selected_row.iloc[0]
            st.session_state.var_roll = row['roll']
            st.session_state.var_name = row['name']
            st.session_state.var_course = row['course']
            st.session_state.var_marks = row['marks']
            st.session_state.var_total_marks = row['total_marks']
            st.session_state.var_percentage = row['percentage']
            st.rerun()

    def add(self):
        """Same logic as original add method"""
        try:
            if st.session_state.var_roll == '' or st.session_state.var_name == '':
                st.error('Roll No and Name are required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from results where roll=?', (st.session_state.var_roll,))
                row = cur.fetchone()
                if row:
                    st.error('Result for this Roll No already exists')
                else:
                    cur.execute(
                        'insert into results (roll,name,course,marks,total_marks,percentage) values(?,?,?,?,?,?)',
                        (st.session_state.var_roll, st.session_state.var_name, st.session_state.var_course,
                         st.session_state.var_marks, st.session_state.var_total_marks, st.session_state.var_percentage))
                    con.commit()
                    st.success('Result added successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def show(self):
        """Same logic as original show method"""
        try:
            con, cur = self.get_db_connection()
            cur.execute('select * from results')
            rows = cur.fetchall()

            if rows:
                # Convert to display format
                data = []
                for row in rows:
                    data.append({
                        'Result ID': row[0],
                        'roll': row[1],
                        'name': row[2],
                        'course': row[3],
                        'marks': row[4],
                        'total_marks': row[5],
                        'percentage': row[6]
                    })

                # Display as interactive table
                df = st.dataframe(data, use_container_width=True, hide_index=True)

                # Selection handling
                if st.button("📝 Load Selected Result", key="load_result"):
                    if len(data) > 0:
                        # For demo, load first result. In real app, you'd handle selection
                        selected_data = data[0]
                        st.session_state.var_roll = selected_data['roll']
                        st.session_state.var_name = selected_data['name']
                        st.session_state.var_course = selected_data['course']
                        st.session_state.var_marks = selected_data['marks']
                        st.session_state.var_total_marks = selected_data['total_marks']
                        st.session_state.var_percentage = selected_data['percentage']
                        st.rerun()
            else:
                st.info("No results found")

            con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def search(self):
        """Same logic as original search method"""
        try:
            con, cur = self.get_db_connection()
            cur.execute(f"select * from results where roll LIKE '%{st.session_state.var_search}%'")
            rows = cur.fetchall()

            if rows:
                data = []
                for row in rows:
                    data.append({
                        'Result ID': row[0],
                        'roll': row[1],
                        'name': row[2],
                        'course': row[3],
                        'marks': row[4],
                        'total_marks': row[5],
                        'percentage': row[6]
                    })
                st.dataframe(data, use_container_width=True, hide_index=True)
            else:
                st.info("No results found matching search criteria")

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
            if st.session_state.var_roll == '':
                st.error('Roll No required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from results where roll=?', (st.session_state.var_roll,))
                row = cur.fetchone()
                if not row:
                    st.error('Result not present')
                else:
                    cur.execute('update results set name=?,course=?,marks=?,total_marks=?,percentage=? where roll=?',
                                (st.session_state.var_name, st.session_state.var_course, st.session_state.var_marks,
                                 st.session_state.var_total_marks, st.session_state.var_percentage,
                                 st.session_state.var_roll))
                    con.commit()
                    st.success('Result updated successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def clear(self):
        """Same logic as original clear method"""
        st.session_state.var_search = ''
        st.session_state.var_roll = ''
        st.session_state.var_name = ''
        st.session_state.var_course = ''
        st.session_state.var_marks = ''
        st.session_state.var_total_marks = ''
        st.session_state.var_percentage = ''
        st.rerun()

    def delete(self):
        """Fixed delete method"""
        try:
            if st.session_state.var_roll == '':
                st.error('Roll No required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from results where roll=?', (st.session_state.var_roll,))
                row = cur.fetchone()
                if not row:
                    st.error('Result not present')
                else:
                    cur.execute('delete from results where roll=?', (st.session_state.var_roll,))
                    con.commit()
                    st.success('Result deleted successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')
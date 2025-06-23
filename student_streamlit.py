import streamlit as st
from database import Database
import sqlite3


class StudentTab:
    def __init__(self):
        # Variables (same as original)
        if 'var_roll' not in st.session_state:
            st.session_state.var_roll = ''
        if 'var_name' not in st.session_state:
            st.session_state.var_name = ''
        if 'var_email' not in st.session_state:
            st.session_state.var_email = ''
        if 'var_gender' not in st.session_state:
            st.session_state.var_gender = ''
        if 'var_dob' not in st.session_state:
            st.session_state.var_dob = ''
        if 'var_contact' not in st.session_state:
            st.session_state.var_contact = ''
        if 'var_admission' not in st.session_state:
            st.session_state.var_admission = ''
        if 'var_course' not in st.session_state:
            st.session_state.var_course = ''
        if 'var_state' not in st.session_state:
            st.session_state.var_state = ''
        if 'var_city' not in st.session_state:
            st.session_state.var_city = ''
        if 'var_pin' not in st.session_state:
            st.session_state.var_pin = ''
        if 'txt_address' not in st.session_state:
            st.session_state.txt_address = ''
        if 'var_search' not in st.session_state:
            st.session_state.var_search = ''

    def get_db_connection(self):
        """Get fresh database connection for each operation"""
        db = Database()
        return db.get_conenction()

    def render(self):
        st.markdown("""
        <div style="background: #0676ad; color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2>👨‍🎓 Manage Student Details</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            self.render_form()

        with col2:
            self.render_table()

    def render_form(self):
        st.subheader("Student Information")

        # Form fields (same variables as original)
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.var_roll = st.text_input("Roll No", value=st.session_state.var_roll)
            st.session_state.var_email = st.text_input("Email", value=st.session_state.var_email)
            st.session_state.var_dob = st.text_input("Date of Birth", value=st.session_state.var_dob)
            st.session_state.var_admission = st.text_input("Admission Date", value=st.session_state.var_admission)
            st.session_state.var_state = st.text_input("State", value=st.session_state.var_state)
            st.session_state.var_pin = st.text_input("PIN Code", value=st.session_state.var_pin)

        with col2:
            st.session_state.var_name = st.text_input("Name", value=st.session_state.var_name)
            st.session_state.var_gender = st.selectbox("Gender", ["", "Male", "Female", "Other"],
                                                      index=0 if st.session_state.var_gender == '' else
                                                      ["", "Male", "Female", "Other"].index(st.session_state.var_gender))
            st.session_state.var_contact = st.text_input("Contact", value=st.session_state.var_contact)
            st.session_state.var_course = st.text_input("Course", value=st.session_state.var_course)
            st.session_state.var_city = st.text_input("City", value=st.session_state.var_city)

        st.session_state.txt_address = st.text_area("Address", value=st.session_state.txt_address, height=100)

        # Buttons (same functionality as original)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("➕ Add", key="add_student"):
                self.add()

        with col2:
            if st.button("✏️ Update", key="update_student"):
                self.update()

        with col3:
            if st.button("🗑️ Delete", key="delete_student"):
                self.delete()

        with col4:
            if st.button("🧹 Clear", key="clear_student"):
                self.clear()

    def render_table(self):
        st.subheader("Student List")

        # Search panel
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.session_state.var_search = st.text_input("Search Roll No", value=st.session_state.var_search)
        with col2:
            if st.button("🔍 Search", key="search_student"):
                self.search()
        with col3:
            if st.button("🧹 Clear Search", key="clear_search_student"):
                self.clear_search()

        # Display table
        self.show()

    def get_Data(self, selected_row):
        """Same logic as original get_Data method"""
        if selected_row is not None and len(selected_row) > 0:
            row = selected_row.iloc[0]
            st.session_state.var_roll = row['roll']
            st.session_state.var_name = row['name']
            st.session_state.var_email = row['email']
            st.session_state.var_gender = row['gender']
            st.session_state.var_dob = row['dob']
            st.session_state.var_contact = row['contact']
            st.session_state.var_admission = row['admission']
            st.session_state.var_course = row['course']
            st.session_state.var_state = row['state']
            st.session_state.var_city = row['city']
            st.session_state.var_pin = row['pin']
            st.session_state.txt_address = row['address']
            st.rerun()

    def add(self):
        """Same logic as original add method"""
        try:
            if st.session_state.var_roll == '' or st.session_state.var_name == '':
                st.error('Roll No and Name are required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from students where roll=?', (st.session_state.var_roll,))
                row = cur.fetchone()
                if row:
                    st.error('Roll No already present')
                else:
                    cur.execute('insert into students (roll,name,email,gender,dob,contact,admission,course,state,city,pin,address) values(?,?,?,?,?,?,?,?,?,?,?,?)',
                                (st.session_state.var_roll, st.session_state.var_name, st.session_state.var_email,
                                 st.session_state.var_gender, st.session_state.var_dob, st.session_state.var_contact,
                                 st.session_state.var_admission, st.session_state.var_course, st.session_state.var_state,
                                 st.session_state.var_city, st.session_state.var_pin, st.session_state.txt_address))
                    con.commit()
                    st.success('Student added successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def show(self):
        """Same logic as original show method"""
        try:
            con, cur = self.get_db_connection()
            cur.execute('select * from students')
            rows = cur.fetchall()

            if rows:
                # Convert to display format
                data = []
                for row in rows:
                    data.append({
                        'roll': row[0],
                        'name': row[1],
                        'email': row[2],
                        'gender': row[3],
                        'dob': row[4],
                        'contact': row[5],
                        'admission': row[6],
                        'course': row[7],
                        'state': row[8],
                        'city': row[9],
                        'pin': row[10],
                        'address': row[11]
                    })

                # Display as interactive table
                df = st.dataframe(data, use_container_width=True, hide_index=True)

                # Selection handling
                if st.button("📝 Load Selected Student", key="load_student"):
                    if len(data) > 0:
                        # For demo, load first student. In real app, you'd handle selection
                        selected_data = data[0]
                        st.session_state.var_roll = selected_data['roll']
                        st.session_state.var_name = selected_data['name']
                        st.session_state.var_email = selected_data['email']
                        st.session_state.var_gender = selected_data['gender']
                        st.session_state.var_dob = selected_data['dob']
                        st.session_state.var_contact = selected_data['contact']
                        st.session_state.var_admission = selected_data['admission']
                        st.session_state.var_course = selected_data['course']
                        st.session_state.var_state = selected_data['state']
                        st.session_state.var_city = selected_data['city']
                        st.session_state.var_pin = selected_data['pin']
                        st.session_state.txt_address = selected_data['address']
                        st.rerun()
            else:
                st.info("No students found")

            con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def search(self):
        """Same logic as original search method"""
        try:
            con, cur = self.get_db_connection()
            cur.execute(f"select * from students where roll LIKE '%{st.session_state.var_search}%'")
            rows = cur.fetchall()

            if rows:
                data = []
                for row in rows:
                    data.append({
                        'roll': row[0],
                        'name': row[1],
                        'email': row[2],
                        'gender': row[3],
                        'dob': row[4],
                        'contact': row[5],
                        'admission': row[6],
                        'course': row[7],
                        'state': row[8],
                        'city': row[9],
                        'pin': row[10],
                        'address': row[11]
                    })
                st.dataframe(data, use_container_width=True, hide_index=True)
            else:
                st.info("No students found matching search criteria")

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
                cur.execute('select * from students where roll=?', (st.session_state.var_roll,))
                row = cur.fetchone()
                if not row:
                    st.error('Student not present')
                else:
                    cur.execute('update students set name=?,email=?,gender=?,dob=?,contact=?,admission=?,course=?,state=?,city=?,pin=?,address=? where roll=?',
                                (st.session_state.var_name, st.session_state.var_email, st.session_state.var_gender,
                                 st.session_state.var_dob, st.session_state.var_contact, st.session_state.var_admission,
                                 st.session_state.var_course, st.session_state.var_state, st.session_state.var_city,
                                 st.session_state.var_pin, st.session_state.txt_address, st.session_state.var_roll))
                    con.commit()
                    st.success('Student updated successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')

    def clear(self):
        """Same logic as original clear method"""
        st.session_state.var_search = ''
        st.session_state.var_roll = ''
        st.session_state.var_name = ''
        st.session_state.var_email = ''
        st.session_state.var_gender = ''
        st.session_state.var_dob = ''
        st.session_state.var_contact = ''
        st.session_state.var_admission = ''
        st.session_state.var_course = ''
        st.session_state.var_state = ''
        st.session_state.var_city = ''
        st.session_state.var_pin = ''
        st.session_state.txt_address = ''
        st.rerun()

    def delete(self):
        """Fixed delete method"""
        try:
            if st.session_state.var_roll == '':
                st.error('Roll No required')
            else:
                con, cur = self.get_db_connection()
                cur.execute('select * from students where roll=?', (st.session_state.var_roll,))
                row = cur.fetchone()
                if not row:
                    st.error('Student not present')
                else:
                    cur.execute('delete from students where roll=?', (st.session_state.var_roll,))
                    con.commit()
                    st.success('Student deleted successfully')
                    self.clear()
                con.close()
        except Exception as e:
            st.error(f'Error: {str(e)}')
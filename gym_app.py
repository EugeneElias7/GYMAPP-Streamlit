import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
import random

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Bengaluru Fitness Hub",
    page_icon="🏋️‍♂️",
    layout="wide",
)

# --- MOCK DATABASE WITH PRELOADED VALUES ---
def initialize_data():
    """Initializes the session state with sample data if it doesn't exist."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Preloaded Admin & Trainer Credentials
        st.session_state.admins = [{'username': 'admin', 'password': 'password123', 'name': 'Adarsh'}]
        st.session_state.trainers = [
            {'ID': 101, 'Name': 'Karthik Murali', 'Specialization': 'CrossFit', 'username': 'karthik', 'password': 'pass'},
            {'ID': 102, 'Name': 'Lakshmi Devi', 'Specialization': 'Yoga & Pilates', 'username': 'lakshmi', 'password': 'pass'},
        ]
        
        # Preloaded Member Data with South Indian Names & Detailed Profiles
        st.session_state.members = [
            {'ID': 1, 'Name': 'Priya Kumar', 'username': 'priyak', 'Password': 'pass', 'Email': 'priya@email.com', 'Phone': '9876543210', 'DOB': date(1995, 5, 20), 'Address': '123 Koramangala, Bengaluru', 'Photo URL': 'https://api.dicebear.com/8.x/avataaars/svg?seed=Priya', 'Plan': 'Gold', 'Status': 'Active', 'Join Date': date(2024, 1, 15), 'Expiry Date': date(2025, 1, 15), 'Trainer ID': 101, 'Uploaded Photo': None},
            {'ID': 2, 'Name': 'Vikram Reddy', 'username': 'vikramr', 'Password': 'pass', 'Email': 'vikram@email.com', 'Phone': '9876543211', 'DOB': date(1990, 11, 30), 'Address': '456 Indiranagar, Bengaluru', 'Photo URL': 'https://api.dicebear.com/8.x/avataaars/svg?seed=Vikram', 'Plan': 'Silver', 'Status': 'Active', 'Join Date': date(2024, 3, 1), 'Expiry Date': date(2025, 8, 1), 'Trainer ID': 102, 'Uploaded Photo': None},
            {'ID': 3, 'Name': 'Ananya Iyer', 'username': 'ananyai', 'Password': 'pass', 'Email': 'ananya@email.com', 'Phone': '9876543212', 'DOB': date(2000, 8, 10), 'Address': '789 Jayanagar, Bengaluru', 'Photo URL': 'https://api.dicebear.com/8.x/avataaars/svg?seed=Ananya', 'Plan': 'Bronze', 'Status': 'Expired', 'Join Date': date(2023, 5, 20), 'Expiry Date': date(2024, 5, 20), 'Trainer ID': 101, 'Uploaded Photo': None},
        ]
        
        # Preloaded Plans and Payments in Rupees
        st.session_state.plans = {'Bronze': {'price': 1500, 'duration': 30}, 'Silver': {'price': 2500, 'duration': 30}, 'Gold': {'price': 4000, 'duration': 30}}
        st.session_state.payments = [{'Member ID': 1, 'Amount': 4000, 'Date': date(2024, 1, 15), 'Plan': 'Gold'}, {'Member ID': 2, 'Amount': 2500, 'Date': date(2024, 3, 1), 'Plan': 'Silver'}]

        # Preloaded Classes
        st.session_state.classes = [
            {'ID': 1001, 'Name': 'Morning CrossFit', 'Trainer': 'Karthik Murali', 'Date': date.today() + timedelta(days=1), 'Time': '06:00', 'Capacity': 10, 'Booked': [1, 2]},
            {'ID': 1002, 'Name': 'Evening Yoga', 'Trainer': 'Lakshmi Devi', 'Date': date.today() + timedelta(days=1), 'Time': '18:00', 'Capacity': 15, 'Booked': [3]},
            {'ID': 1003, 'Name': 'Pilates Core', 'Trainer': 'Lakshmi Devi', 'Date': date.today() + timedelta(days=2), 'Time': '12:00', 'Capacity': 12, 'Booked': []},
        ]
        
        st.session_state.announcements = ["Maintenance alert: The swimming pool will be closed this weekend.", "Ganesha Chaturthi Promotion: Get 20% off on all 'Gold' annual plans!"]
        
        st.session_state.workout_library = [
            # Leg Workouts
            {'Name': 'Barbell Squat', 'Muscle Group': 'Legs', 'Difficulty': 'Intermediate', 'Equipment': 'Barbell, Squat Rack', 'Video': 'https://www.youtube.com/watch?v=U3mC6_o2_C4'},
            {'Name': 'Leg Press', 'Muscle Group': 'Legs', 'Difficulty': 'Beginner', 'Equipment': 'Leg Press Machine', 'Video': 'https://www.youtube.com/watch?v=s0-zB1qfVzI'},
            {'Name': 'Romanian Deadlift (RDL)', 'Muscle Group': 'Legs', 'Difficulty': 'Intermediate', 'Equipment': 'Barbell or Dumbbells', 'Video': 'https://www.youtube.com/watch?v=jW2tK9c4f7k'},
            
            # Chest Workouts
            {'Name': 'Push-up', 'Muscle Group': 'Chest', 'Difficulty': 'Beginner', 'Equipment': 'None', 'Video': 'https://www.youtube.com/watch?v=IODxDxX7oi4'},
            {'Name': 'Dumbbell Bench Press', 'Muscle Group': 'Chest', 'Difficulty': 'Intermediate', 'Equipment': 'Dumbbells, Bench', 'Video': 'https://www.youtube.com/watch?v=fJz0t4tDq3Q'},
            {'Name': 'Cable Flys', 'Muscle Group': 'Chest', 'Difficulty': 'Intermediate', 'Equipment': 'Cable Machine', 'Video': 'https://www.youtube.com/watch?v=rtJ-E3qYl7M'},
            
            # Back Workouts
            {'Name': 'Pull-up', 'Muscle Group': 'Back', 'Difficulty': 'Advanced', 'Equipment': 'Pull-up Bar', 'Video': 'https://www.youtube.com/watch?v=eGo4IYFdUsw'},
            {'Name': 'Bent-Over Dumbbell Rows', 'Muscle Group': 'Back', 'Difficulty': 'Intermediate', 'Equipment': 'Dumbbells', 'Video': 'https://www.youtube.com/watch?v=ZfA1yE72F_c'},
            {'Name': 'Lat Pulldown', 'Muscle Group': 'Back', 'Difficulty': 'Beginner', 'Equipment': 'Lat Pulldown Machine', 'Video': 'https://www.youtube.com/watch?v=0saN0G0Xg4o'},

            # Arms Workouts
            {'Name': 'Bicep Curls', 'Muscle Group': 'Arms', 'Difficulty': 'Beginner', 'Equipment': 'Dumbbells or Barbell', 'Video': 'https://www.youtube.com/watch?v=tQ11T6z1J48'},
            {'Name': 'Tricep Dips', 'Muscle Group': 'Arms', 'Difficulty': 'Intermediate', 'Equipment': 'Bench or Dip Station', 'Video': 'https://www.youtube.com/watch?v=s-tT1C2y_mE'},
            
            # Core Workouts
            {'Name': 'Plank', 'Muscle Group': 'Core', 'Difficulty': 'Beginner', 'Equipment': 'None', 'Video': 'https://www.youtube.com/watch?v=ASdvfQjU7F0'},
            {'Name': 'Leg Raises', 'Muscle Group': 'Core', 'Difficulty': 'Beginner', 'Equipment': 'None', 'Video': 'https://www.youtube.com/watch?v=W0y_oBq_Q_E'},
        ]

        st.session_state.member_workouts = {
            1: [{'Date': date(2025, 7, 10), 'Exercise': 'Barbell Squat', 'Weight': 60, 'Sets': 3, 'Reps': 10}],
            2: [], 3: []
        }
        
        # New Feature Data
        st.session_state.equipment = [
            {'ID': 201, 'Name': 'Treadmill #1', 'Status': 'Working', 'Last Service': date(2024, 1, 1)},
            {'ID': 202, 'Name': 'Treadmill #2', 'Status': 'Maintenance', 'Last Service': date(2024, 6, 1)},
        ]
        st.session_state.nutrition = {
            1: [{'Date': date.today(), 'Meal': 'Breakfast', 'Food': 'Idli and Sambar', 'Calories': 350, 'Macronutrients': 'High carb, low protein'}],
            2: [], 3: [],
        }
        st.session_state.community_posts = [
            {'user': 'Priya Kumar', 'text': 'Just hit a new PR on my squat! Feeling great 💪', 'date': datetime.now()},
            {'user': 'Vikram Reddy', 'text': 'Yoga class with Lakshmi Devi was amazing today!', 'date': datetime.now() - timedelta(hours=2)},
        ]
        st.session_state.badges = {
            1: ['First Workout Logged', '5 Classes Booked'],
            2: ['First Class Booked'],
            3: [],
        }
        st.session_state.challenges = {
            '30-Day Squat Challenge': {'participants': [{'ID': 1, 'Name': 'Priya Kumar', 'reps': 500}, {'ID': 2, 'Name': 'Vikram Reddy', 'reps': 450}]},
            'July Cardio King': {'participants': [{'ID': 1, 'Name': 'Priya Kumar', 'distance': 25.5}, {'ID': 2, 'Name': 'Vikram Reddy', 'distance': 22.0}]},
        }
        st.session_state.body_metrics = {
            1: [{'date': date.today(), 'weight': 65, 'body_fat': 22}, {'date': date.today() - timedelta(days=30), 'weight': 67, 'body_fat': 23}],
        }
        st.session_state.progress_photos = {
            1: [],
            2: [],
            3: [],
        }
        
        st.session_state.member_plans = {
            1: [{'exercise': 'Barbell Squat', 'sets': 3, 'reps': 10, 'notes': 'Focus on form.'}],
            2: [],
            3: [],
        }
        
        # New data structure for trainer requests
        st.session_state.trainer_requests = {t['ID']: [] for t in st.session_state.trainers}
        
# --- LOGIN & REGISTRATION PAGE ---
def login_register_page(role):
    st.title("🏋️‍♂️ Bengaluru Fitness Hub")
    st.markdown(f"*{datetime.now().strftime('%A, %d %B %Y')}*")

    login_tab, register_tab = st.tabs(["**Login**", "**Register as Member**"])

    with login_tab:
        st.header("Login to Your Account")

        if role == "Admin":
            with st.form("admin_login_form"):
                username = st.text_input("Admin Username")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login as Admin", use_container_width=True):
                    admin = next((a for a in st.session_state.admins if a['username'] == username and a['password'] == password), None)
                    if admin:
                        st.session_state.logged_in = True
                        st.session_state.role = "Admin"
                        st.session_state.admin_name = admin.get("name", "Admin")
                        st.rerun()
                    else:
                        st.error("Invalid admin username or password.")
        
        elif role == "Member":
            with st.form("member_login_form"):
                username = st.text_input("Username")
                password = st.text_input("Your Password", type="password")
                if st.form_submit_button("Login as Member", use_container_width=True):
                    member = next((m for m in st.session_state.members if m['username'] == username and m['Password'] == password), None)
                    if member:
                        st.session_state.logged_in = True
                        st.session_state.role = "Member"
                        st.session_state.current_user_id = member['ID']
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        elif role == "Trainer":
            with st.form("trainer_login_form"):
                username = st.text_input("Trainer Username")
                password = st.text_input("Password", type="password") # Mock password, should be stored securely
                if st.form_submit_button("Login as Trainer", use_container_width=True):
                    trainer = next((t for t in st.session_state.trainers if t['username'] == username and t['password'] == password), None)
                    if trainer:
                        st.session_state.logged_in = True
                        st.session_state.role = "Trainer"
                        st.session_state.current_trainer_id = trainer['ID']
                        st.rerun()
                    else:
                        st.error("Invalid trainer username or password.")

    with register_tab:
        st.header("Create a New Member Account")
        with st.form("registration_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.form_submit_button("Register", use_container_width=True):
                if password == confirm_password and email and name:
                    # Simple username generation (e.g., first name + first letter of last name)
                    username = name.lower().split(' ')[0] + name.lower().split(' ')[-1][0]
                    if any(m['Email'] == email for m in st.session_state.members):
                        st.error("An account with this email already exists.")
                    elif any(m['username'] == username for m in st.session_state.members):
                        # Handle potential username conflicts
                        st.warning("Generated username already exists. Please try a different name.")
                    else:
                        new_id = max(m['ID'] for m in st.session_state.members) + 1 if st.session_state.members else 1
                        new_member = {
                            "ID": new_id, "Name": name, "username": username, "Password": password, "Email": email, "Phone": phone,
                            "DOB": date(1999, 1, 1), "Address": "Bengaluru, Karnataka", 
                            "Photo URL": f"https://api.dicebear.com/8.x/avataaars/svg?seed={name.split(' ')[0]}",
                            "Plan": "Bronze", "Status": "Active", "Join Date": date.today(), 
                            "Expiry Date": date.today() + timedelta(days=30), 'Trainer ID': None, 'Uploaded Photo': None
                        }
                        st.session_state.members.append(new_member)
                        st.session_state.member_workouts[new_id] = []
                        st.session_state.nutrition[new_id] = []
                        st.session_state.badges[new_id] = []
                        st.session_state.body_metrics[new_id] = []
                        st.session_state.progress_photos[new_id] = []
                        st.success(f"Registration successful! Your new Member ID is {new_id} and your username is '{username}'. Please log in.")
                        st.rerun()
                else:
                    st.warning("Please fill all fields and ensure passwords match.")


# --- ADMIN VIEW ---
def admin_view():
    admin_name = st.session_state.get('admin_name', 'Admin')
    st.sidebar.title(f"Welcome, {admin_name}")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigate", ["Dashboard", "My Profile", "Member Management", "Class & Schedule", "Trainer Management", "Equipment Management", "Reports", "Post Announcement"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if page == "Dashboard":
        admin_dashboard()
    elif page == "My Profile":
        admin_profile()
    elif page == "Member Management":
        membership_management()
    elif page == "Class & Schedule":
        class_schedule_management()
    elif page == "Trainer Management":
        trainer_management()
    elif page == "Equipment Management":
        equipment_management()
    elif page == "Reports":
        reporting()
    elif page == "Post Announcement":
        post_announcement()


def admin_dashboard():
    st.title("📊 Admin Dashboard")
    total_members = len(st.session_state.members)
    active_members = sum(1 for m in st.session_state.members if m['Status'] == 'Active')
    total_revenue = sum(p['Amount'] for p in st.session_state.payments)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members", total_members)
    col2.metric("Active Members", active_members)
    col3.metric("Total Revenue", f"₹{total_revenue:,.0f}")

    st.header("Visualizations")
    members_df = pd.DataFrame(st.session_state.members)
    if not members_df.empty:
        members_df['Join Month'] = pd.to_datetime(members_df['Join Date']).dt.to_period('M').astype(str)
        growth = members_df.groupby('Join Month').size().reset_index(name='New Sign-ups')
        fig_growth = px.line(growth, x='Join Month', y='New Sign-ups', title='Membership Growth Over Time', markers=True)
        st.plotly_chart(fig_growth, use_container_width=True)

    # --- Predictive Analytics (Mock) ---
    st.header("📈 Predictive Analytics")
    st.info("This section would use an algorithm to predict trends. For this mock, it's placeholder.")
    st.markdown("Based on current trends, we predict a **15% increase** in demand for our Yoga classes next quarter.")

def admin_profile():
    st.title("Admin Profile")
    admin_data = st.session_state.admins[0] # Assuming only one admin for this app
    
    st.subheader("Edit Your Profile")
    with st.form("admin_profile_form"):
        new_name = st.text_input("Name", value=admin_data['name'])
        new_username = st.text_input("Username", value=admin_data['username'])
        if st.form_submit_button("Update Profile"):
            admin_data['name'] = new_name
            admin_data['username'] = new_username
            st.session_state.admin_name = new_name
            st.success("Admin profile updated successfully!")
            st.rerun()

def membership_management():
    st.title("👥 Member Management")
    members_df = pd.DataFrame(st.session_state.members)
    
    # Create editable data editor
    st.subheader("Edit Member Details")
    edited_df = st.data_editor(
        members_df,
        column_config={
            "ID": st.column_config.Column("ID", disabled=True),
            "Photo URL": st.column_config.Column("Photo", disabled=True),
            "Password": st.column_config.Column("Password", disabled=True),
            "DOB": st.column_config.DateColumn("Date of Birth"),
            "Join Date": st.column_config.DateColumn("Join Date", disabled=True),
            "Expiry Date": st.column_config.DateColumn("Expiry Date"),
            "Plan": st.column_config.SelectboxColumn("Plan", options=list(st.session_state.plans.keys())),
            "Trainer ID": st.column_config.SelectboxColumn("Trainer ID", options=[t['ID'] for t in st.session_state.trainers]),
        },
        hide_index=True,
    )
    
    if st.button("Save Changes"):
        st.session_state.members = edited_df.to_dict('records')
        st.success("Member details updated successfully!")
        st.rerun()

    # Admin can change user's profile image
    with st.expander("🖼️ Change Member Profile Photo"):
        member_options = {m['ID']: m['Name'] for m in st.session_state.members}
        member_id_to_change = st.selectbox("Select Member", options=list(member_options.keys()), format_func=lambda x: member_options[x], key="admin_change_photo_select")
        uploaded_photo = st.file_uploader("Upload new profile photo", type=["png", "jpg", "jpeg"], key="admin_photo_uploader")
        
        if uploaded_photo:
            if st.button("Update Photo"):
                for member in st.session_state.members:
                    if member['ID'] == member_id_to_change:
                        member['Uploaded Photo'] = uploaded_photo.getvalue()
                        st.success(f"Profile photo for {member['Name']} updated!")
                        st.rerun()
                else:
                    st.error("Member not found.")

    with st.expander("➕ Add a New Member"):
        with st.form("add_member_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            password = st.text_input("Set Temporary Password", type="password")
            plan = st.selectbox("Membership Plan", options=list(st.session_state.plans.keys()))
            
            if st.form_submit_button("Add Member"):
                if email and name and password:
                    # Simple username generation (e.g., first name + first letter of last name)
                    username = name.lower().split(' ')[0] + name.lower().split(' ')[-1][0]
                    if any(m['Email'] == email for m in st.session_state.members):
                        st.error("An account with this email already exists.")
                    elif any(m['username'] == username for m in st.session_state.members):
                        st.error("Username already exists. Please try a different name.")
                    else:
                        new_id = max(m['ID'] for m in st.session_state.members) + 1 if st.session_state.members else 1
                        new_member = {
                            "ID": new_id, "Name": name, "username": username, "Password": password, "Email": email, "Phone": phone,
                            "DOB": date(1999, 1, 1), "Address": "Bengaluru, Karnataka", 
                            "Photo URL": f"https://api.dicebear.com/8.x/avataaars/svg?seed={name.split(' ')[0]}",
                            "Plan": plan, "Status": "Active", "Join Date": date.today(), 
                            "Expiry Date": date.today() + timedelta(days=st.session_state.plans[plan]['duration']), 'Trainer ID': None, 'Uploaded Photo': None
                        }
                        st.session_state.members.append(new_member)
                        st.session_state.member_workouts[new_id] = []
                        st.session_state.nutrition[new_id] = []
                        st.session_state.badges[new_id] = []
                        st.session_state.body_metrics[new_id] = []
                        st.session_state.progress_photos[new_id] = []
                        st.success(f"Registration successful! Your new Member ID is {new_id} and your username is '{username}'. Please log in.")
                        st.rerun()
                else:
                    st.warning("Please fill all fields and ensure passwords match.")

def class_schedule_management():
    st.title("🗓️ Class & Schedule Management")
    classes_df = pd.DataFrame(st.session_state.classes)
    classes_df.index = range(1, len(classes_df) + 1)
    st.dataframe(classes_df[['ID', 'Name', 'Trainer', 'Date', 'Time', 'Capacity']], use_container_width=True)

    with st.expander("➕ Add a New Class"):
        with st.form("add_class_form"):
            name = st.text_input("Class Name")
            trainer_name = st.selectbox("Assign Trainer", [t['Name'] for t in st.session_state.trainers])
            class_date = st.date_input("Date", min_value=date.today())
            class_time = st.time_input("Time")
            capacity = st.number_input("Capacity", min_value=1, max_value=50, step=1)

            if st.form_submit_button("Add Class"):
                new_id = max(c['ID'] for c in st.session_state.classes) + 1 if st.session_state.classes else 1001
                new_class = {
                    'ID': new_id, 'Name': name, 'Trainer': trainer_name, 'Date': class_date, 
                    'Time': class_time.strftime('%H:%M'), 'Capacity': capacity, 'Booked': []
                }
                st.session_state.classes.append(new_class)
                st.success(f"Successfully added class '{name}'.")
                st.rerun()

def trainer_management():
    st.title("💪 Trainer Management")
    trainers_df = pd.DataFrame(st.session_state.trainers)
    trainers_df.index = range(1, len(trainers_df) + 1)
    st.dataframe(trainers_df, use_container_width=True)

    with st.expander("➕ Add a New Trainer"):
        with st.form("add_trainer_form"):
            name = st.text_input("Trainer Name")
            specialization = st.text_input("Specialization")

            if st.form_submit_button("Add Trainer"):
                new_id = max(t['ID'] for t in st.session_state.trainers) + 1 if st.session_state.trainers else 101
                new_trainer = {'ID': new_id, 'Name': name, 'Specialization': specialization, 'username': name.lower().replace(' ', ''), 'password': 'pass'}
                st.session_state.trainers.append(new_trainer)
                st.success(f"Successfully added trainer {name}.")
                st.rerun()

def equipment_management():
    st.title("🔩 Equipment Management")
    equipment_df = pd.DataFrame(st.session_state.equipment)
    equipment_df.index = range(1, len(equipment_df) + 1)
    st.dataframe(equipment_df, use_container_width=True)
    
    with st.form("add_equipment_form"):
        st.subheader("Add or Update Equipment")
        name = st.text_input("Equipment Name")
        status = st.selectbox("Status", ['Working', 'Maintenance', 'Broken'])
        if st.form_submit_button("Add/Update Equipment"):
            # Mock update logic
            st.success(f"Successfully updated '{name}' status to '{status}'.")
            st.rerun()

def billing_payments():
    st.title("💳 Billing & Payments")
    id_to_name = {m['ID']: m['Name'] for m in st.session_state.members}
    payments_data = st.session_state.payments
    for p in payments_data:
        p['Member Name'] = id_to_name.get(p['Member ID'], 'Unknown')
    
    payments_df = pd.DataFrame(payments_data)
    payments_df.index = range(1, len(payments_df) + 1)
    st.dataframe(payments_df[['Member Name', 'Amount', 'Date', 'Plan']], use_container_width=True,
                  column_config={"Amount": st.column_config.NumberColumn(format="₹ %d")})

def reporting():
    st.title("📈 Reporting")
    report_type = st.selectbox("Select Report Type", ["Financial", "Member", "Usage"])
    if report_type == "Financial":
        st.subheader("Financial Report")
        payments_df = pd.DataFrame(st.session_state.payments)
        payments_df['Month'] = pd.to_datetime(payments_df['Date']).dt.to_period('M').astype(str)
        revenue_by_month = payments_df.groupby('Month')['Amount'].sum().reset_index()
        fig = px.bar(revenue_by_month, x='Month', y='Amount', title='Monthly Revenue')
        st.plotly_chart(fig, use_container_width=True)
    elif report_type == "Member":
        st.subheader("Member Report")
        members_df = pd.DataFrame(st.session_state.members)
        plan_counts = members_df['Plan'].value_counts().reset_index()
        plan_counts.columns = ['Plan', 'Count']
        fig_pie = px.pie(plan_counts, names='Plan', values='Count', title='Membership Plan Distribution')
        st.plotly_chart(fig_pie, use_container_width=True)
    elif report_type == "Usage":
        st.subheader("Usage Report (Class Popularity)")
        class_usage = [{'Name': c['Name'], 'Bookings': len(c['Booked'])} for c in st.session_state.classes]
        usage_df = pd.DataFrame(class_usage)
        fig_usage = px.bar(usage_df, x='Name', y='Bookings', title='Class Popularity by Bookings')
        st.plotly_chart(fig_usage, use_container_width=True)

def post_announcement():
    st.title("📢 Post/Edit Announcement")
    st.subheader("Post a New Announcement")
    with st.form("new_announcement_form"):
        announcement_text = st.text_area("Enter announcement text:")
        if st.form_submit_button("Post"):
            if announcement_text:
                st.session_state.announcements.insert(0, announcement_text)
                st.success("Announcement posted!")
                st.rerun()
            else:
                st.warning("Announcement text cannot be empty.")
    
    st.markdown("---")
    st.subheader("Edit an Existing Announcement")
    if st.session_state.announcements:
        announcement_to_edit = st.selectbox("Select announcement to edit", st.session_state.announcements, key="edit_announcement_select")
        with st.form("edit_announcement_form"):
            edited_text = st.text_area("Edit announcement text:", value=announcement_to_edit)
            if st.form_submit_button("Save Changes"):
                index = st.session_state.announcements.index(announcement_to_edit)
                st.session_state.announcements[index] = edited_text
                st.success("Announcement updated!")
                st.rerun()
    else:
        st.info("No announcements to edit.")

    st.subheader("Current Announcements")
    for ann in st.session_state.announcements:
        st.info(ann)

# --- TRAINER VIEW ---
def trainer_view():
    trainer = next((t for t in st.session_state.trainers if t['ID'] == st.session_state.current_trainer_id), None)
    if not trainer:
        st.error("Trainer profile not found.")
        return

    st.sidebar.title("Trainer Menu")
    st.sidebar.header(trainer['Name'])
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigate", ["My Dashboard", "My Profile", "My Members", "Pending Requests"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if page == "My Dashboard":
        st.title("👨‍💼 Trainer Dashboard")
        st.subheader(f"Welcome, {trainer['Name']}!")
        assigned_classes = [c for c in st.session_state.classes if c['Trainer'] == trainer['Name']]
        st.write("### Your Upcoming Classes")
        if assigned_classes:
            classes_df = pd.DataFrame(assigned_classes)
            st.dataframe(classes_df[['Name', 'Date', 'Time', 'Booked']], use_container_width=True)
        else:
            st.info("You have no classes scheduled.")
    
    elif page == "My Profile":
        st.title("Trainer Profile")
        st.subheader("Edit Your Profile")
        with st.form("trainer_profile_form"):
            new_name = st.text_input("Name", value=trainer['Name'])
            new_specialization = st.text_input("Specialization", value=trainer['Specialization'])
            if st.form_submit_button("Update Profile"):
                trainer['Name'] = new_name
                trainer['Specialization'] = new_specialization
                st.session_state.current_trainer_id = trainer['ID']
                st.success("Trainer profile updated successfully!")
                st.rerun()
    
    elif page == "My Members":
        st.title("My Members")
        my_members = [m for m in st.session_state.members if m.get('Trainer ID') == trainer['ID']]
        if my_members:
            members_df = pd.DataFrame(my_members)
            st.dataframe(members_df[['ID', 'Name', 'Email', 'Phone', 'Plan']], use_container_width=True)
        else:
            st.info("You are not currently assigned to any members.")
    
    elif page == "Pending Requests":
        st.title("📥 Pending Trainer Requests")
        requests = st.session_state.trainer_requests.get(trainer['ID'], [])
        if not requests:
            st.info("You have no new trainer requests.")
        else:
            st.subheader("Requests to Assign")
            for member_id in requests:
                member_requesting = next((m for m in st.session_state.members if m['ID'] == member_id), None)
                if member_requesting:
                    with st.container(border=True):
                        st.write(f"**Member:** {member_requesting['Name']} (ID: {member_requesting['ID']})")
                        col1, col2 = st.columns(2)
                        if col1.button("Accept", key=f"accept_req_{member_id}"):
                            # Assign the trainer to the member
                            for member_to_update in st.session_state.members:
                                if member_to_update['ID'] == member_id:
                                    member_to_update['Trainer ID'] = trainer['ID']
                                    break
                            # Remove the request
                            st.session_state.trainer_requests[trainer['ID']].remove(member_id)
                            st.success(f"Successfully assigned {member_requesting['Name']} as your member!")
                            st.rerun()
                        if col2.button("Reject", key=f"reject_req_{member_id}"):
                            # Remove the request without assigning
                            st.session_state.trainer_requests[trainer['ID']].remove(member_id)
                            st.info(f"Rejected request from {member_requesting['Name']}.")
                            st.rerun()


# --- MEMBER VIEW ---
def member_view():
    member = next((m for m in st.session_state.members if m['ID'] == st.session_state.current_user_id), None)
    if not member:
        st.error("Profile not found. Please log out.")
        return

    st.sidebar.title("Member Menu")
    if member.get('Uploaded Photo'):
        st.sidebar.image(member.get('Uploaded Photo'), width=100)
    else:
        st.sidebar.image(member.get('Photo URL', ''), width=100)
    st.sidebar.header(member['Name'])
    st.sidebar.markdown(f"**Member ID:** {member['ID']}")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigate", ["My Profile", "Class Booking", "Workout Tracking", "Nutrition Tracking", "Progress Photos", "Challenges", "Community", "Find a Trainer", "Announcements"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if page == "My Profile":
        st.title(f"👋 Welcome, {member['Name']}!")
        col1, col2 = st.columns([1, 2])
        with col1:
            if member.get('Uploaded Photo'):
                st.image(member.get('Uploaded Photo'), caption="Profile Photo", width=200)
            else:
                st.image(member.get('Photo URL', ''), caption="Profile Photo", width=200)
            
            uploaded_file = st.file_uploader("Upload your profile photo", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                st.session_state.members[st.session_state.current_user_id - 1]['Uploaded Photo'] = uploaded_file.getvalue()
                st.success("Photo uploaded successfully! Refresh the page to see the new profile picture.")
                st.rerun()

        with col2:
            st.subheader("Your Membership Details")
            st.info(f"**Plan:** {member.get('Plan', 'N/A')}")
            st.info(f"**Status:** {member.get('Status', 'N/A')}")
            expiry = member.get('Expiry Date')
            if expiry: st.info(f"**Expires On:** {expiry.strftime('%d %B %Y')}")
            trainer_name = next((t['Name'] for t in st.session_state.trainers if t['ID'] == member.get('Trainer ID')), 'Not Assigned')
            st.info(f"**Assigned Trainer:** {trainer_name}")

        with st.expander("✏️ Edit Your Contact Information"):
            with st.form("update_info"):
                new_name = st.text_input("Name", value=member.get('Name', ''))
                new_email = st.text_input("Email", value=member.get('Email', ''))
                new_phone = st.text_input("Phone Number", value=member.get('Phone', ''))
                new_address = st.text_area("Address", value=member.get('Address', ''))
                if st.form_submit_button("Update Info"):
                    member['Name'] = new_name
                    member['Email'] = new_email
                    member['Phone'] = new_phone
                    member['Address'] = new_address
                    st.success("Your information has been updated.")
                    st.rerun()

    elif page == "Class Booking":
        st.title("🤸 Class Booking")
        st.subheader("Available Classes")
        for c in st.session_state.classes:
            is_full = len(c.get('Booked', [])) >= c['Capacity']
            is_booked = member['ID'] in c.get('Booked', [])
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**{c['Name']}** with {c['Trainer']}")
                col1.write(f"📅 {c['Date'].strftime('%d-%b-%Y')} at {c['Time']}")
                col2.write(f"**Slots:** {len(c.get('Booked', []))} / {c['Capacity']}")
                
                if is_booked:
                    if col3.button("Cancel Booking", key=f"cancel_{c['ID']}", type="primary", use_container_width=True):
                        c['Booked'].remove(member['ID'])
                        st.toast("Booking cancelled!")
                        st.rerun()
                elif is_full:
                    col3.error("Class is Full", icon="⛔")
                else:
                    if st.button(f"Book Now", key=f"book_{c['ID']}", use_container_width=True):
                        c['Booked'].append(member['ID'])
                        st.toast("Booking successful!")
                        st.rerun()

    elif page == "Workout Tracking":
        st.title("🏋️‍♀️ Workout & Progress Tracking")
        tab1, tab2, tab3, tab4 = st.tabs(["Log New Workout", "My Workout History", "Workout Library", "My Plans"])

        with tab1:
            with st.form("log_workout"):
                workout_names = [w['Name'] for w in st.session_state.workout_library]
                exercise = st.selectbox("Exercise", workout_names)
                weight = st.number_input("Weight (kg)", min_value=0.0, step=2.5)
                sets = st.number_input("Sets", min_value=1, step=1)
                reps = st.number_input("Reps", min_value=1, step=1)
                if st.form_submit_button("Log Workout"):
                    log_entry = {'Date': date.today(), 'Exercise': exercise, 'Weight': weight, 'Sets': sets, 'Reps': reps}
                    if st.session_state.current_user_id not in st.session_state.member_workouts:
                         st.session_state.member_workouts[st.session_state.current_user_id] = []
                    st.session_state.member_workouts[st.session_state.current_user_id].append(log_entry)
                    st.success("Workout logged!")

        with tab2:
            st.subheader("Your Workout History")
            workouts = st.session_state.member_workouts.get(st.session_state.current_user_id, [])
            if workouts:
                df = pd.DataFrame(workouts)
                df.index = range(1, len(df) + 1)
                st.dataframe(df)

                st.subheader("Progress Visualization")
                exercise_to_chart = st.selectbox("Select exercise to visualize", df['Exercise'].unique())
                progress_df = df[df['Exercise'] == exercise_to_chart].sort_values(by='Date')
                if not progress_df.empty:
                    fig = px.line(progress_df, x='Date', y='Weight', title=f'Weight Progress for {exercise_to_chart}', markers=True)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("You have no logged workouts yet.")

        with tab3:
            st.subheader("Browse Workout Library")
            
            # Group workouts by muscle group
            workouts_by_group = {}
            for workout in st.session_state.workout_library:
                group = workout['Muscle Group']
                if group not in workouts_by_group:
                    workouts_by_group[group] = []
                workouts_by_group[group].append(workout)

            for group, workouts in workouts_by_group.items():
                st.markdown(f"### {group}")
                for workout in workouts:
                    with st.expander(f"{workout['Name']} ({workout['Difficulty']})"):
                        st.write(f"**Equipment:** {workout['Equipment']}")
                        st.video(workout['Video'])
            
            st.markdown("---")
            with st.expander("➕ Add a New Exercise to Library"):
                with st.form("add_exercise_form"):
                    name = st.text_input("Exercise Name")
                    muscle_group = st.text_input("Muscle Group (e.g., Legs, Chest, Back)")
                    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
                    equipment = st.text_input("Equipment")
                    video = st.text_input("Video URL (YouTube link)")
                    if st.form_submit_button("Add Exercise"):
                        if name and muscle_group and video:
                            new_workout = {'Name': name, 'Muscle Group': muscle_group, 'Difficulty': difficulty, 'Equipment': equipment, 'Video': video}
                            st.session_state.workout_library.append(new_workout)
                            st.success(f"Exercise '{name}' added to the library!")
                            st.rerun()
                        else:
                            st.error("Please fill out all required fields.")

        with tab4:
            st.subheader("Your Personalized Workout Plans")
            plans = st.session_state.member_plans.get(st.session_state.current_user_id, [])
            if plans:
                st.info("This is your current plan from your trainer.")
                plans_df = pd.DataFrame(plans)
                st.data_editor(plans_df, use_container_width=True, hide_index=True)
                st.markdown("---")
            else:
                st.info("You don't have a plan assigned by a trainer yet. Why not create your own?")
            
            with st.expander("➕ Create Your Own Workout Plan"):
                with st.form("create_plan_form"):
                    st.write("Add an exercise to your custom plan:")
                    exercise_name = st.text_input("Exercise Name")
                    sets = st.number_input("Sets", min_value=1, step=1)
                    reps = st.number_input("Reps", min_value=1, step=1)
                    notes = st.text_area("Notes (optional)")
                    if st.form_submit_button("Add Exercise to Plan"):
                        if exercise_name:
                            new_plan_entry = {'exercise': exercise_name, 'sets': sets, 'reps': reps, 'notes': notes}
                            if st.session_state.current_user_id not in st.session_state.member_plans:
                                st.session_state.member_plans[st.session_state.current_user_id] = []
                            st.session_state.member_plans[st.session_state.current_user_id].append(new_plan_entry)
                            st.success("Exercise added to your plan!")
                            st.rerun()
                        else:
                            st.error("Exercise name is required.")

    elif page == "Nutrition Tracking":
        st.title("🥗 Nutrition Tracking")
        with st.form("log_meal"):
            st.subheader("Log Your Meal")
            food = st.text_input("What did you eat?")
            calories = st.number_input("Calories", min_value=0, step=10)
            macronutrients = st.text_input("Macronutrients (e.g., 50g protein, 30g carbs)")
            if st.form_submit_button("Log Meal"):
                new_meal = {'Date': date.today(), 'Food': food, 'Calories': calories, 'Macronutrients': macronutrients}
                if st.session_state.current_user_id not in st.session_state.nutrition:
                    st.session_state.nutrition[st.session_state.current_user_id] = []
                st.session_state.nutrition[st.session_state.current_user_id].append(new_meal)
                st.success("Meal logged!")
        
        st.subheader("Your Nutrition History")
        nutrition_data = st.session_state.nutrition.get(st.session_state.current_user_id, [])
        if nutrition_data:
            df = pd.DataFrame(nutrition_data)
            df.index = range(1, len(df) + 1)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("You haven't logged any meals yet.")

    elif page == "Progress Photos":
        st.title("📸 Progress Tracking")
        tab1, tab2 = st.tabs(["Log Body Metrics", "Progress Photos"])

        with tab1:
            with st.form("log_metrics"):
                st.subheader("Log Your Body Metrics")
                weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
                body_fat = st.number_input("Body Fat (%)", min_value=0.0, step=0.1)
                if st.form_submit_button("Log Metrics"):
                    new_metric = {'date': date.today(), 'weight': weight, 'body_fat': body_fat}
                    if st.session_state.current_user_id not in st.session_state.body_metrics:
                        st.session_state.body_metrics[st.session_state.current_user_id] = []
                    st.session_state.body_metrics[st.session_state.current_user_id].append(new_metric)
                    st.success("Metrics logged!")
            
            st.subheader("Your Body Metric History")
            metrics_data = st.session_state.body_metrics.get(st.session_state.current_user_id, [])
            if metrics_data:
                df = pd.DataFrame(metrics_data)
                fig = px.line(df, x='date', y='weight', title='Weight Progress')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No body metrics logged yet.")
            
            st.subheader("Your Achievements")
            badges = st.session_state.badges.get(st.session_state.current_user_id, [])
            if badges:
                st.info(", ".join(badges))
            else:
                st.info("No badges earned yet. Keep it up!")

        with tab2:
            st.subheader("Your Progress Photos")
            uploaded_photo = st.file_uploader("Upload a progress photo", type=["png", "jpg", "jpeg"])
            if uploaded_photo is not None:
                new_photo = {'date': date.today(), 'photo': uploaded_photo.getvalue()}
                st.session_state.progress_photos[st.session_state.current_user_id].append(new_photo)
                st.success("Photo uploaded successfully!")
                st.rerun()

            progress_photos = st.session_state.progress_photos.get(st.session_state.current_user_id, [])
            if progress_photos:
                photo_dates = [p['date'].strftime('%Y-%m-%d') for p in progress_photos]
                selected_photo_date = st.selectbox("Select a photo to view", options=photo_dates)
                
                selected_photo = next((p for p in progress_photos if p['date'].strftime('%Y-%m-%d') == selected_photo_date), None)
                if selected_photo:
                    st.image(selected_photo['photo'], caption=f"Photo from {selected_photo['date'].strftime('%B %d, %Y')}")
            else:
                st.info("You haven't uploaded any progress photos yet.")


    elif page == "Challenges":
        st.title("🏆 Challenges & Leaderboards")
        st.subheader("Join a Challenge")
        st.info("This is where you'd see a list of challenges to join.")
        
        st.subheader("Active Leaderboards")
        for challenge, data in st.session_state.challenges.items():
            st.write(f"#### {challenge}")
            df = pd.DataFrame(data['participants']).sort_values(by=list(data['participants'][0].keys())[2], ascending=False)
            df.index = range(1, len(df) + 1)
            st.dataframe(df)

    elif page == "Community":
        st.title("💬 Community Feed")
        st.subheader("Share your progress and connect!")
        with st.form("new_post"):
            post_text = st.text_area("What's on your mind?")
            if st.form_submit_button("Post"):
                if post_text:
                    member_name = member['Name']
                    new_post = {'user': member_name, 'text': post_text, 'date': datetime.now()}
                    st.session_state.community_posts.insert(0, new_post)
                    st.success("Your post has been shared!")
                    st.rerun()
        
        st.subheader("Recent Posts")
        for post in st.session_state.community_posts:
            st.info(f"**{post['user']}** - *{post['date'].strftime('%d %B %Y, %H:%M')}*\n\n{post['text']}")
    
    elif page == "Find a Trainer":
        st.title("🤝 Find a Trainer")
        st.subheader("Connect with the right trainer for you!")
        
        trainers_df = pd.DataFrame(st.session_state.trainers)
        current_trainer_id = member.get('Trainer ID')
        
        for index, trainer in trainers_df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.subheader(trainer['Name'])
                    st.markdown(f"**Specialization:** {trainer['Specialization']}")
                with col2:
                    is_requested = member['ID'] in st.session_state.trainer_requests.get(trainer['ID'], [])
                    if trainer['ID'] == current_trainer_id:
                        st.success("You are already assigned to this trainer!")
                    elif is_requested:
                        st.info("Request pending...")
                    else:
                        if st.button(f"Request {trainer['Name']}", key=f"request_{trainer['ID']}", use_container_width=True):
                            st.session_state.trainer_requests[trainer['ID']].append(member['ID'])
                            st.success(f"You have requested to be assigned to {trainer['Name']}. An admin will review your request.")
                            st.rerun()

    
    elif page == "Announcements":
        st.title("📢 Gym Announcements")
        if st.session_state.announcements:
            for ann in st.session_state.announcements:
                st.info(ann)
        else:
            st.success("No new announcements at this time.")

# --- MAIN APP ROUTER ---
def main():
    initialize_data()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        role = st.selectbox("Login as:", ["Member", "Admin", "Trainer"], key="login_role")
        login_register_page(role)
    else:
        if st.session_state.role == "Admin":
            admin_view()
        elif st.session_state.role == "Member":
            member_view()
        elif st.session_state.role == "Trainer":
            trainer_view()

if __name__ == "__main__":
    main()

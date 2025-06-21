import streamlit as st
import requests
import json
from enum import Enum

# API URL - Replace with your backend URL when deployed
import os
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

# Task status enum to match backend
class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

# Page configuration
st.set_page_config(page_title="Task Manager", layout="wide")

# Initialize session state variables
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Authentication functions
def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.username = username
            return True
        return False
    except Exception as e:
        st.error(f"Error during login: {e}")
        return False

def signup(username, password):
    try:
        response = requests.post(
            f"{API_URL}/users/",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            st.success("Account created successfully! Please log in.")
            return True
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error during signup: {e}")
        return False

def logout():
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.tasks = []

# Task functions
def fetch_tasks():
    if not st.session_state.token:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/tasks/", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch tasks")
            return []
    except Exception as e:
        st.error(f"Error fetching tasks: {e}")
        return []

def create_task(title, description):
    if not st.session_state.token:
        return False
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        data = {"title": title, "description": description}
        response = requests.post(f"{API_URL}/tasks/", json=data, headers=headers)
        if response.status_code == 200:
            st.success("Task created successfully!")
            return True
        else:
            st.error(f"Error creating task: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error creating task: {e}")
        return False

def update_task_status(task_id, title, description, status):
    if not st.session_state.token:
        return False
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        data = {"title": title, "description": description, "status": status}
        response = requests.put(f"{API_URL}/tasks/{task_id}", json=data, headers=headers)
        if response.status_code == 200:
            st.success("Task updated successfully!")
            return True
        else:
            st.error(f"Error updating task: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error updating task: {e}")
        return False

def delete_task(task_id):
    if not st.session_state.token:
        return False
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.delete(f"{API_URL}/tasks/{task_id}", headers=headers)
        if response.status_code == 204:
            st.success("Task deleted successfully!")
            return True
        else:
            st.error(f"Error deleting task: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error deleting task: {e}")
        return False

# UI Components
def show_login_page():
    st.title("Task Manager - Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login(username, password):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    if signup(new_username, new_password):
                        st.rerun()

def show_task_dashboard():
    st.title(f"Welcome, {st.session_state.username}!")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.button("Logout", on_click=logout)
    
    # Fetch and display tasks
    st.session_state.tasks = fetch_tasks()
    
    # Create new task
    with st.expander("Create New Task", expanded=False):
        with st.form("create_task_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            submit = st.form_submit_button("Create Task")
            
            if submit:
                if title:
                    if create_task(title, description):
                        st.session_state.tasks = fetch_tasks()
                        st.rerun()
                else:
                    st.error("Title is required")
    
    # Filter tasks
    status_filter = st.selectbox(
        "Filter by status", 
        ["All", StatusEnum.pending.value, StatusEnum.in_progress.value, StatusEnum.done.value]
    )
    
    # Display tasks
    if st.session_state.tasks:
        filtered_tasks = st.session_state.tasks
        if status_filter != "All":
            filtered_tasks = [task for task in st.session_state.tasks if task["status"] == status_filter]
        
        for task in filtered_tasks:
            with st.expander(f"{task['title']} ({task['status']})"):
                task_title = st.text_input("Title", value=task["title"], key=f"title_{task['id']}")
                task_description = st.text_area("Description", value=task["description"], key=f"desc_{task['id']}")
                task_status = st.selectbox(
                    "Status", 
                    [StatusEnum.pending.value, StatusEnum.in_progress.value, StatusEnum.done.value],
                    index=[StatusEnum.pending.value, StatusEnum.in_progress.value, StatusEnum.done.value].index(task["status"]),
                    key=f"status_{task['id']}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update", key=f"update_{task['id']}"):
                        if update_task_status(task["id"], task_title, task_description, task_status):
                            st.session_state.tasks = fetch_tasks()
                            st.rerun()
                
                with col2:
                    if st.button("Delete", key=f"delete_{task['id']}"):
                        if delete_task(task["id"]):
                            st.session_state.tasks = fetch_tasks()
                            st.rerun()
    else:
        st.info("No tasks found. Create a new task to get started!")

# Main app logic
def main():
    if st.session_state.token:
        show_task_dashboard()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
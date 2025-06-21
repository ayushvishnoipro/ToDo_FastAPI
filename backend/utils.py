from fastapi import HTTPException, status

def check_admin_privileges(user):
    """Check if user has admin role"""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

def check_task_owner(task, user_id):
    """Verify if the user is the task owner or an admin"""
    if task.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
        
def format_task_response(task):
    """Format task response for consistent API output"""
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "owner_id": task.owner_id
    }
import requests
import uuid

ENDPOINT = "https://todo.pixegami.io"

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    
def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    
    data = create_task_response.json()
    
    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)
    
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    # Create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    task_id = create_task_response.json()["task"]["task_id"]
    
    # Update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my update content",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    # Create N tasks.
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    # List tasks, and check there are N items.
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    
    tasks = data["tasks"]
    assert len(tasks) == n

def test_can_delete_task():
    # Create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    
    # Delete a task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    
    # Get the task, and check that it's not found.
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
      
# Helper functions
def list_tasks(user_id):
    return requests.get(ENDPOINT + "/list-tasks/" + user_id)
    
    
def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + "/get-task/" + task_id)

def update_task(new_payload):
    return requests.put(ENDPOINT + "/update-task", json=new_payload)

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")
     
def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    
    print(f"Creating task for user {user_id} with content {content}")
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }

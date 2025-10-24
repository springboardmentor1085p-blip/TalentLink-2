import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def print_response(response, description):
    print(f"\n=== {description} ===")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("=" * 50)

def test_auth():
    # Register a client
    print("\n1. Registering a client...")
    client_data = {
        "username": "testclient",
        "email": "client@test.com",
        "password": "clientpass123",
        "role": "client"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=client_data)
    print_response(response, "Client Registration")
    
    # Register a freelancer
    print("\n2. Registering a freelancer...")
    freelancer_data = {
        "username": "testfreelancer",
        "email": "freelancer@test.com",
        "password": "freelancerpass123",
        "role": "freelancer"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=freelancer_data)
    print_response(response, "Freelancer Registration")
    
    # Login as client
    print("\n3. Logging in as client...")
    login_data = {
        "email": "client@test.com",
        "password": "clientpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    client_token = response.json().get('access_token')
    print_response(response, "Client Login")
    
    # Login as freelancer
    print("\n4. Logging in as freelancer...")
    login_data = {
        "email": "freelancer@test.com",
        "password": "freelancerpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    freelancer_token = response.json().get('access_token')
    print_response(response, "Freelancer Login")
    
    return client_token, freelancer_token

def test_projects(client_token, freelancer_token):
    headers = {
        "Authorization": f"Bearer {client_token}",
        "Content-Type": "application/json"
    }
    
    # Create a project
    print("\n5. Creating a project...")
    project_data = {
        "title": "Website Development",
        "description": "Need a professional website for my business",
        "budget": 1500,
        "duration": "2 months",
        "skills_required": "HTML, CSS, JavaScript, React"
    }
    response = requests.post(
        f"{BASE_URL}/projects",
        headers=headers,
        json=project_data
    )
    project_id = response.json().get('project', {}).get('id')
    print_response(response, "Create Project")
    
    # List projects
    print("\n6. Listing projects...")
    response = requests.get(
        f"{BASE_URL}/projects",
        headers=headers
    )
    print_response(response, "List Projects")
    
    return project_id

def test_proposals(project_id, freelancer_token):
    headers = {
        "Authorization": f"Bearer {freelancer_token}",
        "Content-Type": "application/json"
    }
    
    # Submit a proposal
    print("\n7. Submitting a proposal...")
    proposal_data = {
        "cover_letter": "I have 5 years of experience with React and would love to work on your project!",
        "proposed_rate": 1200
    }
    response = requests.post(
        f"{BASE_URL}/proposals/{project_id}",
        headers=headers,
        json=proposal_data
    )
    proposal_id = response.json().get('id')
    print_response(response, "Submit Proposal")
    
    return proposal_id

def test_proposal_management(project_id, proposal_id, client_token):
    headers = {
        "Authorization": f"Bearer {client_token}",
        "Content-Type": "application/json"
    }
    
    # List proposals for project
    print("\n8. Listing proposals for project...")
    response = requests.get(
        f"{BASE_URL}/proposals/project/{project_id}",
        headers=headers
    )
    print_response(response, "List Proposals")
    
    # Accept proposal
    print("\n9. Accepting proposal...")
    response = requests.put(
        f"{BASE_URL}/proposals/{proposal_id}/status",
        headers=headers,
        json={"status": "accepted"}
    )
    print_response(response, "Accept Proposal")

def main():
    print("=== Starting API Tests ===\n")
    
    try:
        # Test authentication
        client_token, freelancer_token = test_auth()
        
        if not client_token or not freelancer_token:
            print("Error: Failed to get authentication tokens")
            return
        
        # Test project creation
        project_id = test_projects(client_token, freelancer_token)
        
        if not project_id:
            print("Error: Failed to create project")
            return
        
        # Test proposal submission
        proposal_id = test_proposals(project_id, freelancer_token)
        
        if not proposal_id:
            print("Error: Failed to submit proposal")
            return
        
        # Test proposal management
        test_proposal_management(project_id, proposal_id, client_token)
        
        print("\n=== All tests completed successfully! ===")
        
    except Exception as e:
        print(f"\n=== Test failed: {str(e)} ===")

if __name__ == "__main__":
    main()

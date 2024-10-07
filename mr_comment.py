import os
import requests

GITLAB_API_URL = os.getenv("CI_API_V4_URL")
PROJECT_ID = os.getenv("CI_PROJECT_ID")
MR_IID = os.getenv("CI_MERGE_REQUEST_IID")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

def post_comment_on_mr(comment):
    url = f"{GITLAB_API_URL}/projects/{PROJECT_ID}/merge_requests/{MR_IID}/notes"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {"body": comment}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        print(f"Failed to post comment: {response.status_code}")
        print(response.json())

# Read heap profile results
with open("heap_profile.log", "r") as f:
    heap_profile_data = f.read()

# Post the heap profile data as a comment
post_comment_on_mr(f"Heap Profile Results:\n\n{heap_profile_data}")


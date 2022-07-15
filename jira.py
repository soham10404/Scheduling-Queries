import requests
import json

def jiraPost(title: str, query: str):
    url = "https://growwdevs.atlassian.net/rest/api/3/issue"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = json.dumps( 
        {
        "fields": {
            "project": {
                "key": "TEST"
            },
            "summary": str(title),
            "issuetype": {
                "name": "Task"
            },
            "assignee": {
                "id": "62a968a3188d08006fe1f549"
            },
            "reporter": {
                "id": "62b02b68cebad33432f5a11b"
            },
            "customfield_10020": 1039,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": str(query)
                            }
                        ]
                    }
                ]
            }
        }
    })
    response = requests.post(url, headers = headers, data = payload, auth = ("soham.chaudhuri@groww.in", "ZCqvi8HuFk8NkKbPXzK65B71"))
    data = response.json()
    return data


def jiraEdit(key: str, title: str, query: str):
    url = f"https://growwdevs.atlassian.net/rest/api/3/issue/{key}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = json.dumps( 
        {
        "fields": {
            "project": {
                "key": "TEST"
            },
            "summary": str(title),
            "issuetype": {
                "name": "Task"
            },
            "assignee": {
                "id": "62b02b68cebad33432f5a11b"
            },
            "reporter": {
                "id": "62b02b68cebad33432f5a11b"
            },
            "customfield_10020": 1039,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": str(query)
                            }
                        ]
                    }
                ]
            }
        }
    })
    response = requests.put(url, headers = headers, data = payload, auth = ("soham.chaudhuri@groww.in", "ZCqvi8HuFk8NkKbPXzK65B71"))
    return response.text


def jiraDelete(key: str):
    url = f"https://growwdevs.atlassian.net/rest/api/2/issue/{key}" 
    response = requests.delete(url, auth = ("soham.chaudhuri@groww.in", "ZCqvi8HuFk8NkKbPXzK65B71"))
    return response.text


def jiraGet(key: str):
    url = f"https://growwdevs.atlassian.net/rest/api/3/issue/{key}"
    response = requests.get(url, auth = ("soham.chaudhuri@groww.in", "ZCqvi8HuFk8NkKbPXzK65B71"))
    return response.json()
    
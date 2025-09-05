#!/usr/bin/env python3
"""
Test script for Document E-Signature Platform API
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print("✅ Health check passed")
    return data

def test_list_documents():
    """Test document listing"""
    print("\nTesting document listing...")
    response = requests.get(f"{BASE_URL}/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["data"]) == 3  # We have 3 documents
    print(f"✅ Found {len(data['data'])} documents")
    return data

def test_get_document():
    """Test getting a specific document"""
    print("\nTesting document retrieval...")
    response = requests.get(f"{BASE_URL}/api/documents/company_policy")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "content" in data["data"]
    assert "html" in data["data"]
    print(f"✅ Retrieved document: {data['data']['title']}")
    return data

def test_send_document():
    """Test sending a document for signature"""
    print("\nTesting send document...")
    payload = {
        "sender_email": "test.sender@company.com",
        "sender_name": "Test Sender",
        "purpose": "API Testing Purpose",
        "receiver_email": "test.recipient@example.com",
        "document_id": "nda_policy"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/send-document",
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "tracking_id" in data["data"]
    print(f"✅ Document sent with tracking ID: {data['data']['tracking_id']}")
    return data["data"]["tracking_id"]

def test_signature_flow(tracking_id):
    """Test the complete signature flow"""
    print(f"\nTesting signature flow for tracking ID: {tracking_id}")
    
    # Get signature status
    print("  1. Getting signature status...")
    response = requests.get(f"{BASE_URL}/api/signature/{tracking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["signature"]["status"] == "sent"
    print("  ✅ Signature status retrieved")
    
    # Submit signature
    print("  2. Submitting signature...")
    signature_data = {
        "acknowledged": True,
        "name": "Test Recipient",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "location": "New York, USA"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/submit-signature/{tracking_id}",
        json=signature_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "quiz_id" in data["data"]
    quiz_id = data["data"]["quiz_id"]
    print(f"  ✅ Signature submitted, quiz ID: {quiz_id}")
    
    # Get quiz
    print("  3. Getting quiz questions...")
    response = requests.get(f"{BASE_URL}/api/quiz/{quiz_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["questions"]) == 3
    questions = data["data"]["questions"]
    print(f"  ✅ Retrieved {len(questions)} quiz questions")
    
    # Submit quiz (with first option for each question - may fail)
    print("  4. Submitting quiz answers...")
    answers = {}
    for question in questions:
        answers[question["id"]] = question["options"][0]  # Select first option
    
    response = requests.post(
        f"{BASE_URL}/api/submit-quiz/{quiz_id}",
        json={"answers": answers}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"  ✅ Quiz submitted - Passed: {data['data']['passed']}, Score: {data['data']['score']}")
    
    return quiz_id

def test_dashboard():
    """Test dashboard endpoint"""
    print("\nTesting dashboard...")
    response = requests.get(f"{BASE_URL}/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    print(f"✅ Dashboard retrieved with {data['data']['total']} signatures")
    
    # Print some stats
    if data["data"]["signatures"]:
        statuses = {}
        for sig in data["data"]["signatures"]:
            status = sig["status"]
            statuses[status] = statuses.get(status, 0) + 1
        print("  Status breakdown:")
        for status, count in statuses.items():
            print(f"    - {status}: {count}")
    
    return data

def main():
    """Run all tests"""
    print("=" * 60)
    print("Document E-Signature Platform API Test Suite")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        health = test_health()
        documents = test_list_documents()
        document = test_get_document()
        
        # Test signature flow
        tracking_id = test_send_document()
        quiz_id = test_signature_flow(tracking_id)
        
        # Test dashboard
        dashboard = test_dashboard()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        
        print("\nTest Summary:")
        print(f"  - Health: OK")
        print(f"  - Documents Available: {len(documents['data'])}")
        print(f"  - Total Signatures: {dashboard['data']['total']}")
        print(f"  - OpenAI Configured: {health['data']['openai_configured']}")
        print(f"  - Webhook Configured: {health['data']['webhook_configured']}")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
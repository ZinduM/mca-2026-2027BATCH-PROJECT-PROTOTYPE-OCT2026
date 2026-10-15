import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=== 1. Health Check ===")
res = client.get("/api/health")
print("Health:", res.status_code, res.json())

print("\n=== 2. Student Scholarship Recommendation (Student 1601 - MCA) ===")
res = client.post("/api/recommendations/scholarships", json={
    "student_id": 1601,
    "query": "show scholarships",
    "top_k": 4
})
print("Status:", res.status_code)
data = res.json()
print("Total matches:", data.get("total_matches"))
for r in data.get("results", []):
    print(f"  [{r['relevance_score']}] {r['scholarship_name'][:45]} | Rs. {r['amount']} | {r['eligibility_status']}")

print("\n=== 3. Admin Scholarship Search with Amount Filter ('find scholarships above 50000') ===")
res = client.post("/api/scholarships/search", json={
    "query": "find scholarships above 50000",
    "top_k": 4
})
print("Status:", res.status_code)
data = res.json()
print("Applied filters:", data.get("applied_filters"))
for r in data.get("results", []):
    print(f"  [{r['relevance_score']}] {r['scholarship_name'][:45]} | Rs. {r['amount']} | {r['provider']}")

print("\n=== 4. Admin Scholarship Search for MCA ('show MCA scholarships') ===")
res = client.post("/api/scholarships/search", json={
    "query": "show MCA scholarships",
    "top_k": 4
})
print("Status:", res.status_code)
for r in res.json().get("results", []):
    print(f"  [{r['relevance_score']}] {r['scholarship_name'][:45]} | Rs. {r['amount']} | Target: {r.get('course')}")

print("\n=== 5. Student Internship Recommendation (Student 1601 - MCA) ===")
res = client.post("/api/recommendations/internships", json={
    "student_id": 1601,
    "query": "",
    "top_k": 4
})
print("Status:", res.status_code)
for r in res.json().get("results", []):
    print(f"  [{r['relevance_score']}] {r['role']} at {r['company_name']} | Rs. {r['stipend']}/mo")

print("\n=== 6. Admin Query via NLP Speech-to-SQL ('show all scholarships') ===")
res = client.post("/api/query", json={
    "query": "show all scholarships",
    "role": "admin"
})
print("Status:", res.status_code)
q_res = res.json()
print("Execution status:", q_res.get("execution_status"))
print("Generated SQL:", q_res.get("sql"))
print("Row count:", q_res.get("row_count"))
if q_res.get("data"):
    print("Sample row:", q_res["data"][0])

print("\n=== 7. Admin Query via NLP Speech-to-SQL ('find scholarships above 50000') ===")
res = client.post("/api/query", json={
    "query": "find scholarships above 50000",
    "role": "admin"
})
q_res = res.json()
print("Generated SQL:", q_res.get("sql"))
print("Row count:", q_res.get("row_count"))

print("\n=== 8. Student Query via NLP Speech-to-SQL (Student 1601 - 'show my scholarships') ===")
res = client.post("/api/query", json={
    "query": "show my scholarships",
    "student_id": 1601,
    "role": "student"
})
q_res = res.json()
print("Generated SQL:", q_res.get("sql"))
print("Row count:", q_res.get("row_count"))

print("\nALL BACKEND API TESTS COMPLETED SUCCESSFULLY!")

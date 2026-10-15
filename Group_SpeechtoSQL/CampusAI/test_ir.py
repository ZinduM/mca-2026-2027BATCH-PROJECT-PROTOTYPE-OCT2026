import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from backend.recommendation.ir_engine import ir_engine

print("=== 1. Testing Scholarship Recommendation for MCA Student 1601 ===")
res1 = ir_engine.search_scholarships(query="show scholarships", student_id=1601, top_k=5)
print("Profile used:", res1["student_profile_used"]["name"], "|", res1["student_profile_used"]["course"], "| CGPA:", res1["student_profile_used"]["cgpa"])
print(f"Total indexed docs: {res1['ir_metadata']['indexed_documents']}")
print(f"Query tokens: {res1['ir_metadata']['query_tokens']}")
print(f"Context tokens: {res1['ir_metadata']['context_tokens']}")
for r in res1["results"]:
    print(f"  [{r['relevance_score']}] {r['scholarship_name'][:50]} | Rs. {r['amount']} | {r['provider']} | {r['eligibility_status']}")
    print(f"    Snippet: {r['snippet']}")
    print(f"    Matched Terms: {r['matched_terms']}")

print("\n=== 2. Testing Admin Search for 'find scholarships above 50000' ===")
res2 = ir_engine.search_scholarships(query="find scholarships above 50000", is_admin=True, top_k=5)
print("Applied filters:", res2["applied_filters"])
for r in res2["results"]:
    print(f"  [{r['relevance_score']}] {r['scholarship_name'][:50]} | Rs. {r['amount']} | {r['provider']}")

print("\n=== 3. Testing Admin Search for 'show MCA scholarships' ===")
res2_mca = ir_engine.search_scholarships(query="show MCA scholarships", is_admin=True, top_k=5)
for r in res2_mca["results"]:
    print(f"  [{r['relevance_score']}] {r['scholarship_name'][:50]} | Rs. {r['amount']} | Course: {r.get('course')}")

print("\n=== 4. Testing Internship Recommendation for MCA Student 1601 ===")
res3 = ir_engine.search_internships(query="show internships", student_id=1601, top_k=5)
print("Skills used:", res3["student_profile_used"]["skills"])
for r in res3["results"]:
    print(f"  [{r['relevance_score']}] {r['role']} at {r['company_name']} | Rs. {r['stipend']}/mo | {r['location']}")
    print(f"    Skills Required: {r['skills_required']}")

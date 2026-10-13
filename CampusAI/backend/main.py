"""
CampusAI - FastAPI Backend Application
Main API server with all endpoints for the College ERP Assistant.
"""

import os
import sys
import traceback

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db, execute_raw_sql, get_db_session
from backend.nlp_engine import nlp_engine
from models import Student, Department, AcademicRecord, Attendance, Fee, Scholarship, Internship, Document, Faculty

search_engine = None
web_crawler_instance = None


def get_search_engine():
    global search_engine
    if search_engine is None:
        try:
            from retrieval.document_search import search_engine as se
            search_engine = se
        except Exception:
            pass
    return search_engine


def get_web_crawler():
    global web_crawler_instance
    if web_crawler_instance is None:
        try:
            from crawler.web_crawler import web_crawler as wc
            web_crawler_instance = wc
        except Exception:
            pass
    return web_crawler_instance


# ── FastAPI App ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="CampusAI API",
    description="Intelligent Voice-Based College ERP Assistant API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ── Pydantic Models ───────────────────────────────────────────────────────────


class LoginRequest(BaseModel):
    email: str
    password: str
    role: str  # 'admin' or 'student'


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[int] = None


class QueryRequest(BaseModel):
    query: str
    student_id: Optional[int] = None
    role: Optional[str] = "admin"


class DocumentSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class WebSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    top_k: Optional[int] = 10


class RecommendRequest(BaseModel):
    student_id: Optional[int] = None
    query: Optional[str] = ""
    top_k: Optional[int] = 5


# ── Authentication Endpoints ──────────────────────────────────────────────────

@app.post("/api/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """Authenticate user (admin/faculty or student)."""
    clean_email = request.email.strip().lower()
    clean_password = request.password.strip()
    req_role = request.role.strip().lower()

    print(f"\n[LOGIN] Attempt: role='{req_role}', email='{clean_email}'")

    db = get_db_session()
    try:
        if req_role == "admin":
            # Primary ORM check
            faculty = db.query(Faculty).filter(
                func.lower(Faculty.email) == clean_email,
                Faculty.password == clean_password
            ).first()

            if faculty:
                dept = db.query(Department).filter(
                    Department.department_id == faculty.department_id
                ).first()
                print(f"[LOGIN SUCCESS] Faculty: {faculty.name}")
                return LoginResponse(
                    success=True,
                    message="Login successful",
                    user_id=faculty.faculty_id,
                    name=faculty.name,
                    email=faculty.email,
                    role="admin",
                    department=dept.department_name if dept else "N/A"
                )

            # Direct SQL fallback check
            sql_check = execute_raw_sql(f"""
                SELECT f.faculty_id, f.name, f.email, d.department_name
                FROM faculty f
                LEFT JOIN departments d ON f.department_id = d.department_id
                WHERE LOWER(TRIM(f.email)) = '{clean_email}' AND TRIM(f.password) = '{clean_password}'
                LIMIT 1
            """)
            if sql_check.get("success") and sql_check.get("data"):
                user = sql_check["data"][0]
                print(f"[LOGIN SUCCESS via SQL] Faculty: {user['name']}")
                return LoginResponse(
                    success=True,
                    message="Login successful",
                    user_id=user["faculty_id"],
                    name=user["name"],
                    email=user["email"],
                    role="admin",
                    department=user.get("department_name") or "N/A"
                )

            print(f"[LOGIN FAILED] Invalid faculty credentials for '{clean_email}'")
            raise HTTPException(status_code=401, detail="Invalid credentials. Please verify your email and password.")

        elif req_role == "student":
            # Primary ORM check
            student = db.query(Student).filter(
                func.lower(Student.email) == clean_email,
                Student.password == clean_password
            ).first()

            if student:
                dept = db.query(Department).filter(
                    Department.department_id == student.department_id
                ).first()
                print(f"[LOGIN SUCCESS] Student: {student.name} (ID: {student.student_id})")
                return LoginResponse(
                    success=True,
                    message="Login successful",
                    user_id=student.student_id,
                    student_id=student.student_id,
                    name=student.name,
                    email=student.email,
                    role="student",
                    department=dept.department_name if dept else "N/A"
                )

            # Direct SQL fallback check
            sql_check = execute_raw_sql(f"""
                SELECT s.student_id, s.name, s.email, d.department_name
                FROM students s
                LEFT JOIN departments d ON s.department_id = d.department_id
                WHERE LOWER(TRIM(s.email)) = '{clean_email}' AND TRIM(s.password) = '{clean_password}'
                LIMIT 1
            """)
            if sql_check.get("success") and sql_check.get("data"):
                user = sql_check["data"][0]
                print(f"[LOGIN SUCCESS via SQL] Student: {user['name']} (ID: {user['student_id']})")
                return LoginResponse(
                    success=True,
                    message="Login successful",
                    user_id=user["student_id"],
                    student_id=user["student_id"],
                    name=user["name"],
                    email=user["email"],
                    role="student",
                    department=user.get("department_name") or "N/A"
                )

            print(f"[LOGIN FAILED] Invalid student credentials for '{clean_email}'")
            raise HTTPException(status_code=401, detail="Invalid credentials. Please verify your email and password.")

        raise HTTPException(status_code=400, detail="Invalid role specified")
    finally:
        db.close()


# ── Dashboard Statistics ──────────────────────────────────────────────────────

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """Get dashboard statistics (admin view)."""
    db = get_db_session()
    try:
        total_students = db.query(func.count(Student.student_id)).scalar() or 0
        avg_cgpa = db.query(func.avg(AcademicRecord.cgpa)).scalar() or 0
        avg_attendance = db.query(func.avg(Attendance.attendance_percent)).scalar() or 0
        scholarship_count = db.query(func.count(Scholarship.scholarship_id)).filter(
            Scholarship.application_status == "Approved"
        ).scalar() or 0
        total_departments = db.query(func.count(Department.department_id)).scalar() or 0
        total_faculty = db.query(func.count(Faculty.faculty_id)).scalar() or 0
        pending_fees = db.query(func.count(Fee.fee_id)).filter(
            Fee.payment_status.in_(["Pending", "Partial"])
        ).scalar() or 0
        total_internships = db.query(func.count(Internship.internship_id)).scalar() or 0

        return {
            "total_students": total_students,
            "avg_cgpa": round(float(avg_cgpa), 2),
            "avg_attendance": round(float(avg_attendance), 2),
            "scholarship_count": scholarship_count,
            "total_departments": total_departments,
            "total_faculty": total_faculty,
            "pending_fees": pending_fees,
            "total_internships": total_internships
        }
    finally:
        db.close()


@app.get("/api/dashboard/department-stats")
def get_department_stats():
    """Get department-wise statistics."""
    result = execute_raw_sql("""
        SELECT d.department_name,
               COUNT(DISTINCT s.student_id) as student_count,
               ROUND(AVG(ar.cgpa), 2) as avg_cgpa,
               ROUND(AVG(a.attendance_percent), 2) as avg_attendance
        FROM departments d
        LEFT JOIN students s ON d.department_id = s.department_id
        LEFT JOIN academic_record ar ON s.student_id = ar.student_id
        LEFT JOIN attendance a ON s.student_id = a.student_id
        GROUP BY d.department_name
        ORDER BY d.department_name
    """)
    return result


# ── NLP Query Endpoint ────────────────────────────────────────────────────────

@app.post("/api/query")
async def process_nlp_query(request: Request):
    """
    Process a natural language query with verified RBAC security.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    query_str = body.get("query", "")
    req_student_id = body.get("student_id")
    req_role = body.get("role", "admin")

    db = get_db_session()
    try:
        verified_student_id = None
        if req_student_id is not None:
            student = db.query(Student).filter(Student.student_id == req_student_id).first()
            if student:
                verified_student_id = student.student_id
                req_role = "student"
    finally:
        db.close()

    try:
        result = nlp_engine.process_query(
            query=query_str,
            student_id=verified_student_id,
            role=req_role
        )
        return result
    except Exception as e:
        traceback.print_exc()
        return {
            "original_query": query_str,
            "intent": "error",
            "sql": "",
            "execution_status": "Error",
            "error": str(e),
            "columns": [],
            "data": [],
            "row_count": 0,
            "recommendations": [
                "Show my attendance",
                "Show my CGPA",
                "Show my semester results",
                "Show my fees"
            ] if req_role == "student" else [
                "Show all students",
                "Department-wise students",
                "City-wise students",
                "Gender distribution"
            ]
        }


# ── Recommendation Endpoints ──────────────────────────────────────────────────

@app.post("/api/recommendations/internships")
def recommend_internships(request: RecommendRequest):
    """Recommend internships based on student skills/profile using TF-IDF + Cosine Similarity."""
    db = get_db_session()
    try:
        profile_text = request.query or ""
        if request.student_id:
            student = db.query(Student).filter(Student.student_id == request.student_id).first()
            if student:
                student_dept = db.query(Department).filter(Department.department_id == student.department_id).first()
                dept_name = student_dept.department_name if student_dept else ""
                profile_text += f" {student.course or ''} {dept_name}"

        internships_res = execute_raw_sql("SELECT internship_id, title, company_name, description, stipend, location FROM internships")
        internships = internships_res if isinstance(internships_res, list) else (internships_res.get("data", []) if isinstance(internships_res, dict) else [])

        scored_internships = nlp_engine.recommender.match_opportunities(
            student_profile=profile_text.strip(),
            items=internships,
            field="title"
        )
        return {"results": scored_internships[:request.top_k]}
    finally:
        db.close()


@app.post("/api/recommendations/queries")
def recommend_queries(request: RecommendRequest):
    """Get query suggestions using TF-IDF and Cosine Similarity."""
    suggestions = nlp_engine.recommender.get_query_recommendations(
        query=request.query or "",
        top_k=request.top_k or 5
    )
    return {"recommendations": suggestions}


# ── Student-Specific Endpoints ────────────────────────────────────────────────

@app.get("/api/student/{student_id}/profile")
def get_student_profile(student_id: int):
    """Get complete student profile."""
    db = get_db_session()
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        dept = db.query(Department).filter(
            Department.department_id == student.department_id
        ).first()

        return {
            "student": student.to_dict() if hasattr(student, "to_dict") else {
                "student_id": student.student_id,
                "name": student.name,
                "roll_number": student.roll_number,
                "email": student.email,
                "course": student.course,
                "year": student.year,
                "semester": student.semester
            },
            "department": dept.to_dict() if dept and hasattr(dept, "to_dict") else (dept.department_name if dept else None)
        }
    finally:
        db.close()


@app.get("/api/student/{student_id}/academics")
def get_student_academics(student_id: int):
    """Get student's academic records."""
    result = execute_raw_sql(f"""
        SELECT ar.subject_name, ar.internal_marks, ar.external_marks,
               ar.total_marks, ar.grade, ar.cgpa, ar.semester, ar.academic_year
        FROM academic_record ar
        WHERE ar.student_id = {student_id}
        ORDER BY ar.semester, ar.subject_name
    """)
    return result


@app.get("/api/student/{student_id}/attendance")
def get_student_attendance(student_id: int):
    """Get student's attendance records."""
    result = execute_raw_sql(f"""
        SELECT a.subject_name, a.total_classes, a.attended_classes,
               a.attendance_percent, a.semester
        FROM attendance a
        WHERE a.student_id = {student_id}
        ORDER BY a.semester, a.subject_name
    """)
    return result


@app.get("/api/student/{student_id}/fees")
def get_student_fees(student_id: int):
    """Get student's fee details."""
    result = execute_raw_sql(f"""
        SELECT f.total_fee, f.paid_amount, f.pending_amount,
               f.payment_status, f.scholarship_applied, f.academic_year
        FROM fees f
        WHERE f.student_id = {student_id}
    """)
    return result


@app.get("/api/student/{student_id}/scholarships")
def get_student_scholarships(student_id: int):
    """Get student's scholarship information."""
    result = execute_raw_sql(f"""
        SELECT sc.scholarship_name, sc.provider, sc.amount,
               sc.eligibility_status, sc.application_status
        FROM scholarships sc
        WHERE sc.student_id = {student_id}
    """)
    return result


@app.get("/api/student/{student_id}/suggestions")
def get_student_suggestions(student_id: int):
    """Get AI-powered suggestions for a student."""
    db = get_db_session()
    try:
        suggestions = []

        low_attendance = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.attendance_percent < 75
        ).all()

        if low_attendance:
            subjects = [a.subject_name for a in low_attendance]
            suggestions.append({
                "type": "warning",
                "title": "Low Attendance Alert",
                "message": f"Your attendance is below 75% in: {', '.join(subjects)}. Attend more classes to maintain eligibility.",
                "priority": "high"
            })

        weak_subjects = db.query(AcademicRecord).filter(
            AcademicRecord.student_id == student_id,
            AcademicRecord.total_marks < 50
        ).all()

        if weak_subjects:
            subjects = [f"{s.subject_name} ({s.total_marks})" for s in weak_subjects]
            suggestions.append({
                "type": "improvement",
                "title": "Subject Improvement Needed",
                "message": f"Focus on improving these subjects: {', '.join(subjects)}",
                "priority": "high"
            })

        pending_fee = db.query(Fee).filter(
            Fee.student_id == student_id,
            Fee.payment_status.in_(["Pending", "Partial"])
        ).first()

        if pending_fee:
            suggestions.append({
                "type": "finance",
                "title": "Fee Payment Reminder",
                "message": f"You have Rs. {pending_fee.pending_amount:,.0f} pending fee. Clear your dues to avoid late charges.",
                "priority": "medium"
            })

        academic = db.query(AcademicRecord).filter(
            AcademicRecord.student_id == student_id
        ).all()

        if academic:
            avg_cgpa = sum(a.cgpa for a in academic) / len(academic)
            if avg_cgpa >= 8.0:
                suggestions.append({
                    "type": "opportunity",
                    "title": "Scholarship Opportunity",
                    "message": f"Your CGPA ({avg_cgpa:.2f}) makes you eligible for merit-based scholarships. Apply now!",
                    "priority": "medium"
                })

        if not suggestions:
            suggestions.append({
                "type": "info",
                "title": "Keep Up the Good Work!",
                "message": "Your academic performance and attendance are satisfactory. Continue maintaining consistency.",
                "priority": "low"
            })

        suggestions.append({
            "type": "tip",
            "title": "Career Tip",
            "message": "Check out the latest internship opportunities. Industry experience is valuable for placements.",
            "priority": "low"
        })

        return {"suggestions": suggestions}
    finally:
        db.close()


# ── Document Search Endpoints ─────────────────────────────────────────────────

@app.post("/api/documents/search")
def search_documents(request: DocumentSearchRequest):
    """Search uploaded documents using TF-IDF, BM25, and semantic search."""
    engine = get_search_engine()
    if engine:
        try:
            results = engine.search(request.query, request.top_k)
            return results
        except Exception as e:
            return {"query": request.query, "results": [], "error": str(e)}
    return {"query": request.query, "results": [], "error": "Search engine not available"}


@app.get("/api/documents")
def list_documents():
    """List all uploaded documents."""
    result = execute_raw_sql("""
        SELECT document_id, title, category, file_path, uploaded_date
        FROM documents
        ORDER BY uploaded_date DESC
    """)
    return result


# ── Web Crawling / External Information ────────────────────────────────────────

@app.post("/api/external/search")
def search_external(request: WebSearchRequest):
    """Search external information (scholarships, internships, announcements)."""
    crawler = get_web_crawler()
    if crawler:
        try:
            results = crawler.search(request.query, request.category, request.top_k)
            return {"query": request.query, "results": results}
        except Exception as e:
            return {"query": request.query, "results": [], "error": str(e)}
    return {"query": request.query, "results": [], "error": "Web crawler not available"}


@app.get("/api/external/scholarships")
def get_external_scholarships():
    """Get scholarship information from crawled sources."""
    crawler = get_web_crawler()
    if crawler:
        return {"results": crawler.get_scholarships()}
    return {"results": []}


@app.get("/api/external/internships")
def get_external_internships():
    """Get internship information from crawled sources."""
    crawler = get_web_crawler()
    if crawler:
        return {"results": crawler.get_internships()}
    return {"results": []}


@app.get("/api/external/announcements")
def get_external_announcements():
    """Get announcements from crawled sources."""
    crawler = get_web_crawler()
    if crawler:
        return {"results": crawler.get_announcements()}
    return {"results": []}


# ── Utility Endpoints ─────────────────────────────────────────────────────────

@app.get("/api/departments")
def list_departments():
    """List all departments."""
    result = execute_raw_sql("SELECT * FROM departments ORDER BY department_name")
    return result


@app.get("/api/internships")
def list_internships():
    """List all internship opportunities."""
    result = execute_raw_sql("SELECT * FROM internships ORDER BY stipend DESC")
    return result


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "CampusAI API", "version": "1.0.0"}


@app.get("/api/sample-queries")
def get_sample_queries():
    """Get sample queries for the admin dashboard."""
    return {
        "queries": [
            {"text": "Show top 10 students based on CGPA", "category": "Academic"},
            {"text": "Show students with attendance below 75%", "category": "Attendance"},
            {"text": "Which department has highest average marks?", "category": "Department"},
            {"text": "Show scholarship eligible students", "category": "Scholarship"},
            {"text": "Show students with pending fees", "category": "Finance"},
            {"text": "Department-wise attendance comparison", "category": "Comparison"},
            {"text": "How many students in each department?", "category": "Count"},
            {"text": "Show available internships", "category": "Internship"},
            {"text": "Show gender distribution", "category": "Demographics"},
            {"text": "Average CGPA of all students", "category": "Academic"},
            {"text": "Show students who failed in any subject", "category": "Academic"},
            {"text": "Show top 5 highest paying internships", "category": "Internship"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
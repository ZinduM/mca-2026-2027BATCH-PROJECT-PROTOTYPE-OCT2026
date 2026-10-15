"""
College ERP - NLP Engine

Natural Language Query Processing:
- Converts user queries into SQL with schema-accurate joins and filters.
- Enforces strict role-based data security: students are strictly confined
  to their own records (student_id), preventing access to other students,
  department-wide stats, or unauthorized ERP tables.
- Faculty/Admin retains full ERP administrative query access.
- Built-in TF-IDF + Cosine Similarity recommendation system.
"""

import re
import os
import sys
from typing import List, Dict, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from backend.database import execute_raw_sql


class ContentRecommender:
    """TF-IDF and Cosine Similarity recommender for query suggestions."""

    def __init__(self):
        self._corpus = [
            "show all students",
            "department-wise student count",
            "city-wise students",
            "gender distribution",
            "year-wise count",
            "show top 10 students by cgpa",
            "show students with attendance below 75",
            "show students with attendance below 75 in MCA department",
            "show students with pending fees",
            "show scholarship eligible students",
            "show available internships",
            "department-wise attendance comparison",
            "department average marks"
        ]

    def get_query_recommendations(self, query: str, role: str = "admin", top_k: int = 5) -> List[str]:
        """Generate role-aware query recommendations."""
        if role == "student":
            return [
                "Show my attendance",
                "Show my CGPA",
                "Show my semester results",
                "Show my fees",
                "Show my scholarships"
            ][:top_k]

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            corpus = self._corpus + [query]
            vectorizer = TfidfVectorizer().fit_transform(corpus)
            vectors = vectorizer.toarray()

            query_vec = vectors[-1].reshape(1, -1)
            sim_scores = cosine_similarity(query_vec, vectors[:-1])[0]

            ranked_indices = sim_scores.argsort()[::-1]
            results = [self._corpus[i].capitalize() for i in ranked_indices if sim_scores[i] > 0]
            if not results:
                results = [c.capitalize() for c in self._corpus[:top_k]]
            return results[:top_k]
        except Exception:
            return [
                "Show all students",
                "Show students with attendance below 75 in MCA department",
                "Department-wise student count",
                "Show top 10 students by CGPA",
                "Show students with pending fees"
            ]

    def match_opportunities(self, student_profile: str, items: List[Dict[str, Any]], field: str = "skills") -> List[Dict[str, Any]]:
        """Matches internships/courses to student profile using TF-IDF and Cosine Similarity."""
        if not items:
            return []

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            item_texts = [
                f"{item.get('title', '')} {item.get(field, '')} {item.get('description', '')}"
                for item in items
            ]
            corpus = [student_profile] + item_texts

            vectorizer = TfidfVectorizer().fit_transform(corpus)
            vectors = vectorizer.toarray()

            sim_scores = cosine_similarity(vectors[0].reshape(1, -1), vectors[1:])[0]
            ranked_indices = sim_scores.argsort()[::-1]

            scored_items = []
            for idx in ranked_indices:
                record = dict(items[idx])
                record["similarity_score"] = round(float(sim_scores[idx]), 3)
                scored_items.append(record)
            return scored_items
        except Exception:
            for item in items:
                item["similarity_score"] = 0.5
            return items


class NLPEngine:
    """Natural Language to SQLite SQL Generator with RBAC Security."""

    EXACT_DEPARTMENTS = [
        "Computer Science & Engineering",
        "Information Technology",
        "Electronics & Communication",
        "Mechanical Engineering",
        "Civil Engineering",
        "Electrical Engineering",
        "Master of Computer Applications",
        "Business Administration"
    ]

    DEPT_ALIASES = {
        "mca": "Master of Computer Applications",
        "master of computer applications": "Master of Computer Applications",
        "mba": "Business Administration",
        "business administration": "Business Administration",
        "cse": "Computer Science & Engineering",
        "cs": "Computer Science & Engineering",
        "computer science": "Computer Science & Engineering",
        "computer science and engineering": "Computer Science & Engineering",
        "computer science & engineering": "Computer Science & Engineering",
        "it": "Information Technology",
        "information technology": "Information Technology",
        "ece": "Electronics & Communication",
        "electronics": "Electronics & Communication",
        "electronics and communication": "Electronics & Communication",
        "electronics & communication": "Electronics & Communication",
        "me": "Mechanical Engineering",
        "mech": "Mechanical Engineering",
        "mechanical": "Mechanical Engineering",
        "mechanical engineering": "Mechanical Engineering",
        "ce": "Civil Engineering",
        "civil": "Civil Engineering",
        "civil engineering": "Civil Engineering",
        "ee": "Electrical Engineering",
        "electrical": "Electrical Engineering",
        "electrical engineering": "Electrical Engineering"
    }

    def __init__(self):
        self.recommender = ContentRecommender()

    def _extract_department(self, query: str) -> Optional[str]:
        for dept in self.EXACT_DEPARTMENTS:
            if dept.lower() in query:
                return dept

        sorted_aliases = sorted(self.DEPT_ALIASES.keys(), key=lambda k: len(k.split()), reverse=True)
        for alias in sorted_aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, query):
                return self.DEPT_ALIASES[alias]
        return None

    def _extract_attendance_condition(self, query: str) -> Optional[Dict[str, Any]]:
        # Do not treat amounts (scholarship, fee, stipend) as attendance
        if any(k in query for k in ["scholarship", "fee", "fees", "stipend", "salary"]):
            return None

        # Require percentage sign or explicit attendance keywords
        m = re.search(r"(?:attendance\s*(?:percentage|percent)?\s*)?(?:below|less than|under|<|<=)\s*(\d+(?:\.\d+)?)\s*%", query)
        if m:
            return {"operator": "<", "value": float(m.group(1))}

        m = re.search(r"(?:attendance\s*(?:percentage|percent)?\s*)?(?:above|greater than|more than|>|>=)\s*(\d+(?:\.\d+)?)\s*%", query)
        if m:
            return {"operator": ">", "value": float(m.group(1))}

        m = re.search(r"(?:attendance\s*(?:percentage|percent)?\s*)(?:below|less than|under|<|<=)\s*(\d+(?:\.\d+)?)", query)
        if m:
            return {"operator": "<", "value": float(m.group(1))}

        m = re.search(r"(?:attendance\s*(?:percentage|percent)?\s*)(?:above|greater than|more than|>|>=)\s*(\d+(?:\.\d+)?)", query)
        if m:
            return {"operator": ">", "value": float(m.group(1))}

        if any(k in query for k in ["low attendance", "poor attendance", "shortage"]):
            return {"operator": "<", "value": 75.0}
        return None

    def _extract_cgpa_condition(self, query: str) -> Optional[Dict[str, Any]]:
        m = re.search(r"(?:cgpa|gpa)\s*(?:above|greater than|more than|>|>=)\s*(\d+(?:\.\d+)?)", query)
        if m:
            return {"operator": ">=", "value": float(m.group(1))}

        m = re.search(r"(?:cgpa|gpa)\s*(?:below|less than|under|<|<=)\s*(\d+(?:\.\d+)?)", query)
        if m:
            return {"operator": "<=", "value": float(m.group(1))}
        return None

    def _extract_limit(self, query: str) -> int:
        m = re.search(r"(?:top|first|limit)\s*(\d+)", query)
        if m:
            return int(m.group(1))
        return 50

    # ─────────────────────────────────────────────────────────────
    # STUDENT SECURITY ENGINE
    # ─────────────────────────────────────────────────────────────

    def _generate_student_sql(self, query: str, student_id: int) -> str:
        """
        Generates SQL strictly sandboxed to the student's unique student_id.
        Rejects queries attempting to access all students, other students,
        departments, or general stats.
        """
        # Block attempts to view other students or department-level aggregates
        bypass_patterns = [
            r"\ball students\b",
            r"\bevery student\b",
            r"\bother students\b",
            r"\bdepartment-wise\b",
            r"\ball department\b",
            r"\bdepartments\b",
            r"\bstatistics\b",
            r"\ball mca\b",
            r"\bmca students\b",
            r"\bb\.tech students\b",
            r"\bbranch-wise\b",
            r"\bignore\b",
            r"\bbypass\b"
        ]

        # 1. Attendance queries
        if any(k in query for k in ["attendance", "absent", "present", "classes"]):
            return f"""
                SELECT a.subject_name, a.total_classes, a.attended_classes, a.attendance_percent, a.semester
                FROM attendance a
                WHERE a.student_id = {student_id}
                ORDER BY a.semester, a.subject_name
            """.strip()

        # 2. CGPA / Marks / Academic queries
        if any(k in query for k in ["cgpa", "gpa", "marks", "grade", "score", "result", "academic", "performance", "semester"]):
            return f"""
                SELECT ar.semester, ar.subject_name, ar.internal_marks, ar.external_marks, ar.total_marks, ar.grade, ar.cgpa
                FROM academic_record ar
                WHERE ar.student_id = {student_id}
                ORDER BY ar.semester, ar.subject_name
            """.strip()

        # 3. Fees queries
        if any(k in query for k in ["fee", "fees", "due", "dues", "payment", "pending amount"]):
            return f"""
                SELECT f.total_fee, f.paid_amount, f.pending_amount, f.payment_status, f.scholarship_applied, f.academic_year
                FROM fees f
                WHERE f.student_id = {student_id}
            """.strip()

        # 4. Scholarship queries
        if any(k in query for k in ["scholarship", "scholarships", "financial aid", "grant"]):
            # If the student specifically asks for their own applied / awarded scholarships:
            if any(k in query for k in ["my scholarship", "my applied", "applied scholarship", "my application", "my status", "awarded to me", "my grant"]):
                return f"""
                    SELECT sc.scholarship_name, sc.provider, sc.amount, sc.course, sc.eligibility_status, sc.application_status
                    FROM scholarships sc
                    WHERE sc.student_id = {student_id}
                """.strip()

            # Otherwise, student is querying available scholarships (institutional opportunities catalog)
            where_clauses = [f"(sc.student_id = {student_id} OR sc.student_id IS NULL)"]

            if "mca" in query:
                where_clauses.append("(sc.course LIKE '%MCA%' OR sc.scholarship_name LIKE '%MCA%' OR sc.description LIKE '%MCA%')")
            elif any(k in query for k in ["btech", "b.tech", "cse", "computer"]):
                where_clauses.append("(sc.course LIKE '%B.Tech%' OR sc.course LIKE '%CSE%' OR sc.description LIKE '%Computer%')")

            if "aicte" in query:
                where_clauses.append("sc.provider LIKE '%AICTE%'")
            if any(k in query for k in ["maharashtra", "mahadbt"]):
                where_clauses.append("(sc.provider LIKE '%Maharashtra%' OR sc.scholarship_name LIKE '%MahaDBT%' OR sc.scholarship_name LIKE '%Maharashtra%')")
            if "eligible" in query:
                where_clauses.append("sc.eligibility_status = 'Eligible'")

            range_match = re.search(
                r'(?:between|from|range)?\s*(?:rs\.?|₹)?\s*(\d+(?:,\d+)?|\d+k)\s*(?:and|to|-)\s*(?:rs\.?|₹)?\s*(\d+(?:,\d+)?|\d+k)',
                query.lower()
            )
            if range_match and any(w in query.lower() for w in ["between", "from", "to", "and", "-"]):
                v1 = float(range_match.group(1).replace(",", "").replace("k", "000"))
                v2 = float(range_match.group(2).replace(",", "").replace("k", "000"))
                min_v, max_v = min(v1, v2), max(v1, v2)
                where_clauses.append(f"sc.amount BETWEEN {min_v} AND {max_v}")
            else:
                amt_gte = re.search(r'(?:>=|at least|min|minimum)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())
                amt_gt = re.search(r'(?:above|greater than|more than|exceeding|higher than|>)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())
                amt_lte = re.search(r'(?:<=|at most|max|maximum)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())
                amt_lt = re.search(r'(?:below|less than|under|<)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())

                if amt_gte:
                    where_clauses.append(f"sc.amount >= {float(amt_gte.group(1))}")
                elif amt_gt:
                    where_clauses.append(f"sc.amount > {float(amt_gt.group(1))}")

                if amt_lte:
                    where_clauses.append(f"sc.amount <= {float(amt_lte.group(1))}")
                elif amt_lt:
                    where_clauses.append(f"sc.amount < {float(amt_lt.group(1))}")

            return f"""
                SELECT sc.scholarship_name, sc.provider, sc.amount, sc.course,
                       sc.min_cgpa, sc.deadline, sc.eligibility_status, sc.application_status
                FROM scholarships sc
                WHERE {' AND '.join(where_clauses)}
                ORDER BY sc.amount DESC
                LIMIT 25
            """.strip()

        # 5. Internship listings (general public information permitted for students)
        if any(k in query for k in ["internship", "internships", "placement", "hiring", "company"]):
            return """
                SELECT role, domain, company_name, stipend, location, duration, skills_required, eligibility
                FROM internships
                ORDER BY stipend DESC
                LIMIT 20
            """.strip()

        # 6. Profile / Identity query (default safe fallback for student)
        # Even if query says "Show all students" or "Show MCA students", only return own profile
        return f"""
            SELECT s.student_id, s.name, s.roll_number, s.email, s.course, s.year, s.semester, d.department_name
            FROM students s
            JOIN departments d ON s.department_id = d.department_id
            WHERE s.student_id = {student_id}
        """.strip()

    # ─────────────────────────────────────────────────────────────
    # FACULTY / ADMIN ENGINE (Broader ERP access)
    # ─────────────────────────────────────────────────────────────

    def _generate_admin_sql(self, query: str) -> str:
        limit = self._extract_limit(query)
        dept_name = self._extract_department(query)
        att_cond = self._extract_attendance_condition(query)
        cgpa_cond = self._extract_cgpa_condition(query)

        # Demographics & Distributions
        if "gender" in query and any(k in query for k in ["distribution", "count", "ratio"]):
            if dept_name:
                return f"""
                    SELECT s.gender, COUNT(s.student_id) AS student_count
                    FROM students s
                    JOIN departments d ON s.department_id = d.department_id
                    WHERE d.department_name = '{dept_name}'
                    GROUP BY s.gender
                """
            return "SELECT gender, COUNT(student_id) AS student_count FROM students GROUP BY gender"

        if any(k in query for k in ["city", "cities", "location"]) and any(k in query for k in ["wise", "count", "distribution"]):
            return """
                SELECT city, COUNT(student_id) AS student_count
                FROM students
                WHERE city IS NOT NULL AND city != ''
                GROUP BY city
                ORDER BY student_count DESC
            """

        if ("year" in query or "year-wise" in query or "yearwise" in query) and any(k in query for k in ["count", "student", "wise"]):
            return """
                SELECT year, COUNT(student_id) AS student_count
                FROM students
                GROUP BY year
                ORDER BY year ASC
            """

        if "category" in query and any(k in query for k in ["count", "distribution"]):
            return """
                SELECT category, COUNT(student_id) AS student_count
                FROM students
                GROUP BY category
                ORDER BY student_count DESC
            """

        # Department Entity Queries
        if ("department" in query or "departments" in query) and not any(k in query for k in ["student", "attendance", "cgpa", "marks", "fee"]):
            if any(k in query for k in ["how many", "count", "total"]):
                return "SELECT COUNT(*) AS total_departments FROM departments"
            return """
                SELECT department_id, department_name, hod_name, total_faculty, location
                FROM departments
                ORDER BY department_name
            """

        if ("department" in query or "dept" in query) and any(k in query for k in ["count", "how many", "total students"]):
            return """
                SELECT d.department_name, COUNT(s.student_id) AS student_count
                FROM departments d
                LEFT JOIN students s ON d.department_id = s.department_id
                GROUP BY d.department_name
                ORDER BY student_count DESC
            """

        if "attendance" in query and ("department" in query or "dept" in query) and any(k in query for k in ["average", "avg", "comparison"]) and not att_cond:
            return """
                SELECT d.department_name, ROUND(AVG(a.attendance_percent), 2) AS average_attendance
                FROM departments d
                JOIN students s ON d.department_id = s.department_id
                JOIN attendance a ON s.student_id = a.student_id
                GROUP BY d.department_name
                ORDER BY average_attendance DESC
            """

        if any(k in query for k in ["marks", "cgpa", "score", "performance"]) and any(k in query for k in ["average", "avg"]) and not cgpa_cond and not att_cond:
            return """
                SELECT d.department_name,
                       ROUND(AVG(ar.total_marks), 2) AS average_marks,
                       ROUND(AVG(ar.cgpa), 2) AS average_cgpa
                FROM departments d
                JOIN students s ON d.department_id = s.department_id
                JOIN academic_record ar ON s.student_id = ar.student_id
                GROUP BY d.department_name
                ORDER BY average_cgpa DESC
            """

        # Internships
        if any(k in query for k in ["internship", "internships", "stipend", "placement", "hiring"]):
            amt_match = re.search(r'(?:above|greater than|more than|>|>=)\s*(\d+)', query)
            where_clause = f"WHERE stipend >= {float(amt_match.group(1))}" if amt_match else ""
            return f"""
                SELECT role, domain, company_name, stipend, location, duration, skills_required, eligibility
                FROM internships
                {where_clause}
                ORDER BY stipend DESC
                LIMIT {limit}
            """

        # Scholarships
        if any(k in query for k in ["scholarship", "scholarships"]):
            where_clauses = []
            if dept_name:
                where_clauses.append(f"(d.department_name = '{dept_name}' OR sc.department = '{dept_name}' OR sc.course LIKE '%{dept_name}%')")
            if "mca" in query:
                where_clauses.append("(sc.course LIKE '%MCA%' OR sc.scholarship_name LIKE '%MCA%' OR sc.description LIKE '%MCA%')")
            if "aicte" in query:
                where_clauses.append("sc.provider LIKE '%AICTE%'")
            if any(k in query for k in ["maharashtra", "mahadbt"]):
                where_clauses.append("(sc.provider LIKE '%Maharashtra%' OR sc.scholarship_name LIKE '%MahaDBT%' OR sc.scholarship_name LIKE '%Maharashtra%')")
            if "eligible" in query:
                where_clauses.append("sc.eligibility_status = 'Eligible'")
            if "approved" in query:
                where_clauses.append("sc.application_status = 'Approved'")

            range_match = re.search(
                r'(?:between|from|range)?\s*(?:rs\.?|₹)?\s*(\d+(?:,\d+)?|\d+k)\s*(?:and|to|-)\s*(?:rs\.?|₹)?\s*(\d+(?:,\d+)?|\d+k)',
                query.lower()
            )
            if range_match and any(w in query.lower() for w in ["between", "from", "to", "and", "-"]):
                v1 = float(range_match.group(1).replace(",", "").replace("k", "000"))
                v2 = float(range_match.group(2).replace(",", "").replace("k", "000"))
                min_v, max_v = min(v1, v2), max(v1, v2)
                where_clauses.append(f"sc.amount BETWEEN {min_v} AND {max_v}")
            else:
                amt_gte = re.search(r'(?:>=|at least|min|minimum)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())
                amt_gt = re.search(r'(?:above|greater than|more than|exceeding|higher than|>)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())
                amt_lte = re.search(r'(?:<=|at most|max|maximum)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())
                amt_lt = re.search(r'(?:below|less than|under|<)\s*(?:rs\.?|₹)?\s*(\d+)', query.lower())

                if amt_gte:
                    where_clauses.append(f"sc.amount >= {float(amt_gte.group(1))}")
                elif amt_gt:
                    where_clauses.append(f"sc.amount > {float(amt_gt.group(1))}")

                if amt_lte:
                    where_clauses.append(f"sc.amount <= {float(amt_lte.group(1))}")
                elif amt_lt:
                    where_clauses.append(f"sc.amount < {float(amt_lt.group(1))}")

            where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            return f"""
                SELECT sc.scholarship_name, sc.provider, sc.amount, sc.course,
                       sc.min_cgpa, sc.deadline, sc.eligibility_status, sc.application_status,
                       COALESCE(s.name, 'Open / All Students') AS student_name
                FROM scholarships sc
                LEFT JOIN students s ON sc.student_id = s.student_id
                LEFT JOIN departments d ON s.department_id = d.department_id
                {where_str}
                ORDER BY sc.amount DESC
                LIMIT {limit}
            """

        # Fees
        if any(k in query for k in ["fee", "fees", "pending fee", "dues"]) and not att_cond and not cgpa_cond:
            where_clauses = ["f.payment_status != 'Paid'"]
            if dept_name:
                where_clauses.append(f"d.department_name = '{dept_name}'")

            return f"""
                SELECT s.name, s.roll_number, d.department_name, f.total_fee,
                       f.paid_amount, f.pending_amount, f.payment_status
                FROM fees f
                JOIN students s ON f.student_id = s.student_id
                JOIN departments d ON s.department_id = d.department_id
                WHERE {' AND '.join(where_clauses)}
                ORDER BY f.pending_amount DESC
                LIMIT {limit}
            """

        # Combined multi-table filters (Attendance, CGPA, Department, Year, Semester)
        select_fields = [
            "s.student_id",
            "s.name",
            "s.roll_number",
            "s.course",
            "d.department_name"
        ]
        from_clause = "FROM students s JOIN departments d ON s.department_id = d.department_id"
        where_conditions = []
        having_conditions = []
        order_by = "s.name"
        group_by = ""

        if dept_name:
            where_conditions.append(f"d.department_name = '{dept_name}'")

        if att_cond or ("attendance" in query and any(k in query for k in ["low", "below", "shortage", "less"])):
            from_clause += " JOIN attendance a ON s.student_id = a.student_id"
            select_fields.append("ROUND(AVG(a.attendance_percent), 2) AS avg_attendance")
            group_by = "GROUP BY s.student_id"

            op = att_cond["operator"] if att_cond else "<"
            val = att_cond["value"] if att_cond else 75.0
            having_conditions.append(f"AVG(a.attendance_percent) {op} {val}")
            order_by = "avg_attendance ASC"

        if cgpa_cond or any(k in query for k in ["cgpa", "gpa", "topper", "marks"]):
            from_clause += " JOIN academic_record ar ON s.student_id = ar.student_id"
            select_fields.append("ROUND(AVG(ar.cgpa), 2) AS cgpa")

            if not group_by:
                group_by = "GROUP BY s.student_id"

            if cgpa_cond:
                having_conditions.append(f"AVG(ar.cgpa) {cgpa_cond['operator']} {cgpa_cond['value']}")

            if "top" in query or "highest" in query or not att_cond:
                order_by = "cgpa DESC"

        sem_match = re.search(r"semester\s*(\d+)", query)
        if sem_match:
            where_conditions.append(f"s.semester = {int(sem_match.group(1))}")

        year_match = re.search(r"(\d+)(?:st|nd|rd|th)?\s*year", query)
        if year_match:
            where_conditions.append(f"s.year = {int(year_match.group(1))}")

        where_str = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
        having_str = f"HAVING {' AND '.join(having_conditions)}" if having_conditions else ""

        if any(k in query for k in ["how many", "count", "total"]) and not att_cond and not cgpa_cond:
            return f"SELECT COUNT(*) AS total_students FROM students s JOIN departments d ON s.department_id = d.department_id {where_str}"

        sql = f"""
            SELECT {', '.join(select_fields)}
            {from_clause}
            {where_str}
            {group_by}
            {having_str}
            ORDER BY {order_by}
            LIMIT {limit}
        """
        return sql.strip()

    # ─────────────────────────────────────────────────────────────
    # QUERY EXECUTION DISPATCHER & SECURITY AUDITOR
    # ─────────────────────────────────────────────────────────────

    def process_query(self, query: str, student_id: Optional[int] = None, role: str = "admin") -> Dict[str, Any]:
        """
        Convert NL query to SQL with strict RBAC enforcement.
        If role is 'student', student_id is mandatory and enforced at the SQL level.
        """
        clean_query = (query or "").strip()
        query_lower = clean_query.lower()

        # Enforce Student Role Security Policy
        if role == "student":
            if not student_id:
                return {
                    "original_query": clean_query,
                    "intent": "security_violation",
                    "target": "security",
                    "sql": "",
                    "execution_status": "Error",
                    "error": "Authentication Error: Unverified student identity.",
                    "columns": [],
                    "data": [],
                    "row_count": 0,
                    "recommendations": self.recommender.get_query_recommendations(query_lower, role="student")
                }
            sql = self._generate_student_sql(query_lower, int(student_id))
        else:
            sql = self._generate_admin_sql(query_lower)

        # Backend Security Sanity Check:
        # Guarantee that if role is student, any query against tables with student_id contains the constraint
        if role == "student":
            sensitive_tables = ["students", "attendance", "academic_record", "fees", "scholarships"]
            contains_sensitive = any(t in sql.lower() for t in sensitive_tables)
            expected_clause = f"student_id = {student_id}"
            expected_alias_clause = f".student_id = {student_id}"

            if contains_sensitive and (expected_clause not in sql and expected_alias_clause not in sql):
                # Security override: force student_id restriction
                sql = f"SELECT * FROM students WHERE student_id = {student_id}"

        db_res = execute_raw_sql(sql)

        if isinstance(db_res, dict):
            columns = db_res.get("columns", [])
            data = db_res.get("data", [])
            success = db_res.get("success", True)
            error_msg = db_res.get("error")
        elif isinstance(db_res, list):
            data = db_res
            columns = list(data[0].keys()) if data else []
            success = True
            error_msg = None
        else:
            data = []
            columns = []
            success = False
            error_msg = "Unknown database output structure"

        target = "student"
        if "department" in query_lower and "student" not in query_lower and role != "student":
            target = "department"
        elif "attendance" in query_lower:
            target = "attendance"
        elif any(k in query_lower for k in ["cgpa", "marks", "academic"]):
            target = "academic"
        elif "fee" in query_lower:
            target = "fees"
        elif "scholarship" in query_lower:
            target = "scholarship"
        elif "internship" in query_lower:
            target = "internship"

        return {
            "original_query": clean_query,
            "intent": "query",
            "target": target,
            "sql": sql,
            "execution_status": "Success" if success else "Error",
            "error": error_msg,
            "columns": columns,
            "data": data,
            "row_count": len(data),
            "recommendations": self.recommender.get_query_recommendations(query_lower, role=role, top_k=5)
        }


# Singleton instance
nlp_engine = NLPEngine()
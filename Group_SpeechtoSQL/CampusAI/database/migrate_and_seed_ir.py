"""
CampusAI - Database Migration and IR Seed Script
Safely adds text-rich columns to 'scholarships' and 'internships' tables
and inserts 75+ realistic scholarships for MCA and Technical students.
"""

import os
import sys
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "campus_ai.db")

print(f"Connecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ── 1. Safely add columns to scholarships ───────────────────────────────────
cursor.execute("PRAGMA table_info(scholarships)")
existing_sch_cols = {col[1] for col in cursor.fetchall()}
print(f"Existing scholarships columns: {existing_sch_cols}")

sch_cols_to_add = [
    ("description", "TEXT"),
    ("eligibility_criteria", "TEXT"),
    ("course", "VARCHAR(100)"),
    ("department", "VARCHAR(100)"),
    ("min_cgpa", "FLOAT DEFAULT 0.0"),
    ("deadline", "VARCHAR(30)")
]

for col_name, col_type in sch_cols_to_add:
    if col_name not in existing_sch_cols:
        print(f"Adding column '{col_name}' to scholarships...")
        cursor.execute(f"ALTER TABLE scholarships ADD COLUMN {col_name} {col_type}")

# ── 2. Safely add columns to internships ────────────────────────────────────
cursor.execute("PRAGMA table_info(internships)")
existing_int_cols = {col[1] for col in cursor.fetchall()}
print(f"Existing internships columns: {existing_int_cols}")

int_cols_to_add = [
    ("skills_required", "VARCHAR(200)"),
    ("description", "TEXT")
]

for col_name, col_type in int_cols_to_add:
    if col_name not in existing_int_cols:
        print(f"Adding column '{col_name}' to internships...")
        cursor.execute(f"ALTER TABLE internships ADD COLUMN {col_name} {col_type}")

conn.commit()

# ── 3. Backfill existing scholarships if they have NULL descriptions ────────
cursor.execute("""
    UPDATE scholarships
    SET description = CASE
        WHEN scholarship_name LIKE '%Pragati%' THEN 'AICTE initiative providing financial support to meritorious girl students pursuing technical degree or diploma courses to empower women in STEM fields.'
        WHEN scholarship_name LIKE '%INSPIRE%' THEN 'Innovation in Science Pursuit for Inspired Research grant offered by DST for students demonstrating outstanding aptitude in science and computational disciplines.'
        WHEN scholarship_name LIKE '%Post-Matric%' THEN 'Government social justice scholarship providing complete tuition and maintenance support for reserved category students in higher technical education.'
        WHEN scholarship_name LIKE '%Central Sector%' THEN 'Central government scholarship scheme for meritorious students above 80th percentile in board examinations pursuing professional graduation and post-graduation.'
        WHEN scholarship_name LIKE '%State Government%' THEN 'State Directorate of Technical Education merit-cum-means scholarship for residents of Maharashtra pursuing professional degrees.'
        WHEN scholarship_name LIKE '%Minority%' THEN 'Ministry of Minority Affairs financial assistance for meritorious minority students enrolled in recognized professional and technical institutions.'
        WHEN scholarship_name LIKE '%Need-Based%' THEN 'Institutional financial aid scheme designed to support economically weaker students facing financial constraints.'
        ELSE 'Merit and technical education scholarship supporting deserving students in higher education with financial awards and tuition grants.'
    END,
    eligibility_criteria = CASE
        WHEN scholarship_name LIKE '%Pragati%' THEN 'Girl students only; Family income below 8 LPA; Admitted to AICTE approved technical degree program; Minimum 6.0 CGPA.'
        WHEN scholarship_name LIKE '%INSPIRE%' THEN 'Top 1% in Class 12 board examination; Pursuing technical or science degree; Minimum 7.5 CGPA.'
        WHEN scholarship_name LIKE '%Post-Matric%' THEN 'SC/ST/OBC category; Family income below 2.5 LPA; Regular full-time student.'
        WHEN scholarship_name LIKE '%Central Sector%' THEN 'Above 80th percentile in board exam; Family income below 4.5 LPA; Minimum 7.0 CGPA.'
        ELSE 'Minimum 60% marks in previous qualification; Family income under 8 LPA; Valid enrollment in approved course.'
    END,
    course = CASE
        WHEN scholarship_name LIKE '%Pragati%' THEN 'MCA, B.Tech CSE, B.Tech IT'
        WHEN scholarship_name LIKE '%INSPIRE%' THEN 'B.Tech CSE, MCA, M.Tech'
        WHEN scholarship_name LIKE '%Post-Matric%' THEN 'MCA, B.Tech, MBA'
        ELSE 'MCA, B.Tech, MBA'
    END,
    department = CASE
        WHEN scholarship_name LIKE '%Pragati%' THEN 'Master of Computer Applications'
        WHEN scholarship_name LIKE '%INSPIRE%' THEN 'Computer Science & Engineering'
        ELSE 'All Departments'
    END,
    min_cgpa = CASE
        WHEN scholarship_name LIKE '%Excellence%' THEN 8.0
        WHEN scholarship_name LIKE '%INSPIRE%' THEN 7.5
        WHEN scholarship_name LIKE '%Pragati%' THEN 6.5
        ELSE 6.0
    END,
    deadline = '2026-11-30'
    WHERE description IS NULL OR description = ''
""")
conn.commit()

# ── 4. Comprehensive Realistic Scholarship Records ──────────────────────────
# Around 75 realistic records spanning AICTE, MahaDBT, Technical, and MCA scholarships
NEW_SCHOLARSHIPS = [
    # AICTE SCHOLARSHIPS
    {
        "name": "AICTE Pragati Scholarship for Girls (MCA & Tech Degree)",
        "provider": "AICTE",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "AICTE flagship scholarship granting financial assistance to girl students admitted to first year or direct second year of technical degree programs like MCA and B.Tech. Aims to empower women in technical higher education with ₹50,000 per annum for tuition, equipment, and books.",
        "eligibility_criteria": "Female students admitted to AICTE approved MCA or B.Tech program; Maximum 2 girl children per family; Annual family income below 8 Lakhs; Minimum 6.5 CGPA in previous degree.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-10-31"
    },
    {
        "name": "AICTE Saksham Scholarship for Differently-Abled Technical Students",
        "provider": "AICTE",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "AICTE scheme dedicated to supporting specially-abled students pursuing professional technical education. Covers purchase of assistive hardware, software development tools, laptops, and college tuition.",
        "eligibility_criteria": "Disability of not less than 40%; Admitted to AICTE approved MCA or Engineering degree course; Family income limit ₹8 Lakhs per annum; Minimum 6.0 CGPA.",
        "course": "MCA, B.Tech, M.Tech",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-10-31"
    },
    {
        "name": "AICTE Swanath Scholarship Scheme for Technical Education",
        "provider": "AICTE",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial aid provided by AICTE to orphans, wards of armed forces and central paramilitary personnel martyred in action, or students whose both parents died due to COVID-19 pursuing degree programs in computer applications or engineering.",
        "eligibility_criteria": "Orphan students or wards of martyred armed personnel; Enrolled in full-time MCA or B.Tech; Family income under 8 LPA; No minimum CGPA bar.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.5,
        "deadline": "2026-11-15"
    },
    {
        "name": "AICTE PG Scholarship for Technical Postgraduates (GATE/National Level)",
        "provider": "AICTE",
        "amount": 148800.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Postgraduate monthly stipend of ₹12,400 per month (total ₹1,48,800/yr) awarded by AICTE to postgraduate students enrolled in computer applications, IT, and software technology with valid national qualifying scores.",
        "eligibility_criteria": "Admitted to full-time MCA or M.Tech program; Valid national level entrance or GATE score; Minimum 7.0 CGPA in undergraduate degree; Regular attendance above 75%.",
        "course": "MCA, M.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "AICTE Lilavati Award Technical Scholar Grant",
        "provider": "AICTE",
        "amount": 75000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Prestigious grant celebrating outstanding academic innovation and software projects designed by female students in computing, artificial intelligence, and mobile application development.",
        "eligibility_criteria": "Female students in MCA or B.Tech Computer Science; Minimum CGPA 7.5; Documented participation in software hackathons or innovative tech projects.",
        "course": "MCA, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-12-15"
    },
    {
        "name": "AICTE-INAE Student Technical Travel & Innovation Grant",
        "provider": "AICTE",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Special scheme by AICTE and Indian National Academy of Engineering supporting students presenting peer-reviewed research papers in international computer science and database conferences.",
        "eligibility_criteria": "MCA or Engineering student with accepted research paper in IEEE, ACM, or Springer conference; Recommendation of Head of Department; CGPA > 7.0.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-12-31"
    },
    {
        "name": "AICTE Tech Saksham Digital Upskilling Grant",
        "provider": "AICTE",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Collaborative digital enablement grant with Microsoft and SAP India providing laptops and reimbursement for certifications in Cloud Computing, AI/ML, and Cybersecurity for MCA and engineering students.",
        "eligibility_criteria": "Full-time student in MCA, CSE, or IT; Demonstrated proficiency in Python or Java; Family income under 6 LPA; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-20"
    },

    # MAHARASHTRA GOVERNMENT / MAHADBT SCHOLARSHIPS
    {
        "name": "Rajarshi Chhatrapati Shahu Maharaj Shikshan Shulkh Shishyavrutti Yojna (EBC)",
        "provider": "Government of Maharashtra (DTE)",
        "amount": 42500.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "Major Maharashtra state government scheme granting 50% tuition fee and exam fee waiver to students belonging to Economically Backward Class (EBC) enrolled in professional postgraduate technical programs like MCA.",
        "eligibility_criteria": "Maharashtra State Domicile; Admitted through CAP (Centralized Admission Process); Annual family income below 8 Lakhs; Minimum 50% marks in graduation.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-10-31"
    },
    {
        "name": "Dr. Panjabrao Deshmukh Vasatigruh Nirvah Bhatta Yojna (Hostel Allowance)",
        "provider": "Government of Maharashtra (DTE)",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Pending",
        "description": "Maharashtra DTE maintenance allowance providing financial relief of ₹30,000 for hostel, mess, and living expenses to children of registered marginal farmers and EBC students admitted to professional MCA and engineering programs.",
        "eligibility_criteria": "Maharashtra Domicile; Hosteller or paying guest in urban areas; Child of marginal farmer or family income up to ₹8 Lakhs; Enrolled in technical degree.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.5,
        "deadline": "2026-11-15"
    },
    {
        "name": "MahaDBT Post Matric Scholarship for SC Category (100% Tuition Waiver)",
        "provider": "Social Justice & Special Assistance Dept, Maharashtra",
        "amount": 85000.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "Complete 100% tuition, development, and examination fee reimbursement along with monthly maintenance allowance for Scheduled Caste (SC) students studying in technical MCA and engineering degree colleges.",
        "eligibility_criteria": "Maharashtra Domicile; SC category caste certificate and caste validity; Family income less than ₹2.5 Lakhs per year; Full-time enrolled student.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.0,
        "deadline": "2026-12-15"
    },
    {
        "name": "MahaDBT Post Matric Scholarship for ST Category",
        "provider": "Tribal Development Department, Maharashtra",
        "amount": 85000.0,
        "eligibility_status": "Eligible",
        "application_status": "Submitted",
        "description": "Full financial sponsorship covering total institutional tuition fees, library charges, computer lab dues, and study tour expenses for Scheduled Tribe (ST) students in postgraduate computer applications.",
        "eligibility_criteria": "ST category with valid tribe certificate and validity certificate issued by Maharashtra authorities; Family income below ₹2.5 Lakhs.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.0,
        "deadline": "2026-12-15"
    },
    {
        "name": "MahaDBT Post Matric Scholarship for OBC/VJNT/SBC Categories",
        "provider": "OBC, VJNT & SBC Welfare Dept, Maharashtra",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Under Review",
        "description": "State welfare scholarship granting 50% to 100% tuition fee reimbursement for Other Backward Classes, Vimukta Jati, Nomadic Tribes, and Special Backward Classes in professional MCA colleges across Maharashtra.",
        "eligibility_criteria": "OBC/VJNT/SBC category certificate with valid non-creamy layer certificate; Family annual income under ₹1.5 Lakhs for scholarship or ₹8 Lakhs for freeship.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Pandit Deendayal Upadhyay Swayam Yojna (Tribal Living Grant)",
        "provider": "Tribal Development Department, Maharashtra",
        "amount": 51000.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "Direct bank transfer of ₹51,000 for food, lodging, and academic materials for tribal students who did not get hostel admissions in Pune, Mumbai, or Nagpur divisional technical colleges.",
        "eligibility_criteria": "Scheduled Tribe student admitted to professional technical college; Unable to get government hostel seat; Maharashtra Domicile.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.0,
        "deadline": "2026-11-20"
    },
    {
        "name": "State Minority Scholarship for Professional Technical Courses (Maharashtra)",
        "provider": "Minority Development Department, Maharashtra",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Maharashtra government scholarship for students from religious minority communities (Muslim, Christian, Buddhist, Sikh, Parsi, Jain) enrolled in AICTE approved MCA and engineering degrees.",
        "eligibility_criteria": "Resident of Maharashtra; Belongs to notified minority community; Annual family income below ₹8 Lakhs; Minimum 50% marks in previous examination.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Dr. Babasaheb Ambedkar Swadhar Yojna",
        "provider": "Social Justice & Special Assistance Dept, Maharashtra",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial grant for SC and Nav-Buddhist students admitted to professional courses in tier-1 Maharashtra cities who could not obtain government hostel accommodation.",
        "eligibility_criteria": "SC category; Resident of Maharashtra; Family income under ₹2.5 Lakhs; Admitted to recognized degree in Pune/Mumbai division.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.0,
        "deadline": "2026-12-05"
    },
    {
        "name": "Directorate of Higher Education (DHE) Eklavya Scholarship Maharashtra",
        "provider": "Higher & Technical Education Dept, Maharashtra",
        "amount": 15000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Merit award for postgraduate students who achieved high aggregate percentages in their undergraduate degree and are currently pursuing Master of Computer Applications (MCA) or M.Sc.",
        "eligibility_criteria": "Graduation from a Maharashtra recognized university with at least 60% marks in science or computer stream; Family income below ₹75,000 per annum.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-10"
    },

    # MCA & COMPUTING SPECIFIC SCHOLARSHIPS
    {
        "name": "Post Graduate Merit Scholarship for Computer Applications (MCA)",
        "provider": "University Grants Commission (UGC)",
        "amount": 36200.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "National UGC scholarship awarded to university first and second rank holders in BCA, B.Sc Computer Science, or B.Sc IT who enroll into Master of Computer Applications (MCA) programs.",
        "eligibility_criteria": "Rank holder (1st or 2nd) at undergraduate level in affiliated university; Enrolled in full-time MCA program; No family income ceiling; Minimum 7.5 CGPA.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-10-31"
    },
    {
        "name": "Google Generation Scholarship for Women in Computing",
        "provider": "Google APAC",
        "amount": 120000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Global flagship scholarship by Google supporting women studying computer science and software applications. Selected scholars receive USD $1,000 to $2,500 equivalent in INR, retreat invitations, and Google technical mentorship.",
        "eligibility_criteria": "Female student currently enrolled in MCA or Computer Science degree; Strong coding background in Python/Java/C++; Demonstrated leadership in tech community; Minimum 7.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-12-15"
    },
    {
        "name": "Adobe India Women-in-Technology Postgraduate Scholarship",
        "provider": "Adobe Systems India",
        "amount": 150000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Highly prestigious tech award by Adobe India covering full tuition fees, travel funding for Grace Hopper Celebration, and fast-track internship interview opportunities for female MCA and CS scholars.",
        "eligibility_criteria": "Female student in 1st or 2nd year of MCA or B.Tech/M.Tech CSE; Excellent academic track record with CGPA >= 8.0; Strong algorithmic problem-solving and software development skills.",
        "course": "MCA, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 8.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "Cognizant Foundation Post-Graduate Tech Scholarship",
        "provider": "Cognizant Foundation",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Corporate CSR fellowship for meritorious students from socio-economically disadvantaged backgrounds pursuing MCA, software engineering, and data science specializations.",
        "eligibility_criteria": "Enrolled in MCA or B.Tech IT/CSE; Family income under ₹3.5 Lakhs; Minimum 70% marks throughout 10th, 12th, and graduation; CGPA > 7.0.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-25"
    },
    {
        "name": "Persistent Foundation Girls in IT Scholarship (MCA & CSE)",
        "provider": "Persistent Foundation",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Annual scholarship by Persistent Systems for female students studying MCA and Computer Science in Maharashtra colleges. Includes technical mentorship by Persistent engineers and placement readiness support.",
        "eligibility_criteria": "Girl students in MCA or B.Tech CSE/IT; Admitted in Pune/Nagpur/Mumbai colleges; Family income < ₹5 Lakhs; Minimum 65% aggregate or 7.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Infosys Foundation STEM Stars Scholarship for MCA Scholars",
        "provider": "Infosys Foundation",
        "amount": 100000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial scholarship by Infosys Foundation covering tuition fees, living costs, and study materials for female and economically weak students pursuing MCA, IT, and software development.",
        "eligibility_criteria": "Female students enrolled in 1st year MCA or B.Tech; Family annual income not exceeding ₹8 Lakhs; Minimum 7.0 CGPA in current semester or graduation.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-12-20"
    },
    {
        "name": "Microsoft Tech Diversity & Inclusion Empowerment Grant",
        "provider": "Microsoft India",
        "amount": 95000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Scholarship and technical mentorship program by Microsoft India aimed at elevating underrepresented students in software engineering, cloud computing, and intelligent systems.",
        "eligibility_criteria": "Enrolled in MCA, CSE, or IT degree; Demonstrated passion for coding, open source, or cloud development; Minimum 7.2 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.2,
        "deadline": "2026-12-10"
    },
    {
        "name": "Amazon Future Engineer Postgraduate Computing Grant",
        "provider": "Amazon India",
        "amount": 80000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Comprehensive scholarship covering educational expenses and Amazon Web Services (AWS) training credits for MCA students from economically challenged backgrounds.",
        "eligibility_criteria": "Admitted to full-time MCA program; Family income under ₹4 Lakhs; Passion for cloud architecture, distributed systems, and software engineering; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-20"
    },
    {
        "name": "Oracle Women in Computing Postgraduate Fellowship",
        "provider": "Oracle India",
        "amount": 85000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Fellowship supporting female students with a focus on Database Management Systems, Cloud Infrastructure, and Enterprise Software Development.",
        "eligibility_criteria": "Female student in MCA or B.Tech Computer Science; Grade A or above in DBMS/SQL and Data Structures; Minimum 7.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Mindtree Technical Excellence Award for MCA Students",
        "provider": "LTIMindtree Foundation",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial scholarship and industry training program for students excelling in full-stack web development, microservices, and mobile application engineering.",
        "eligibility_criteria": "Enrolled in 2nd or 3rd year MCA; Completed practical web projects in React, Node, or Java; Minimum 6.8 CGPA.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.8,
        "deadline": "2026-10-31"
    },
    {
        "name": "Nasscom Foundation FutureSkills Tech Fellowship",
        "provider": "Nasscom Foundation",
        "amount": 45000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Tech scholarship awarded to students certified in AI, Big Data, Cloud Computing, or Cybersecurity through government recognized digital portals.",
        "eligibility_criteria": "MCA or Engineering student; Valid certificate from NPTEL/Swayam or FutureSkills Prime; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-12-05"
    },
    {
        "name": "Tata Consultancy Services (TCS) Innovation Lab Grant",
        "provider": "Tata Consultancy Services",
        "amount": 70000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Research fellowship for postgraduate MCA students working on enterprise software, NLP, and intelligent speech-to-SQL or ERP interfaces.",
        "eligibility_criteria": "MCA final year or pre-final year; Approved research project in Natural Language Processing or Software Engineering; CGPA >= 7.5.",
        "course": "MCA, M.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-11-25"
    },
    {
        "name": "Wipro Cares Technical Scholarship for MCA",
        "provider": "Wipro Cares",
        "amount": 48000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Need-based financial aid program for students from economically weaker households pursuing computer applications with strong academic consistency.",
        "eligibility_criteria": "Full-time MCA student; Total family income less than ₹3.5 LPA; Minimum 60% in graduation; Minimum 6.5 CGPA in current semester.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-15"
    },
    {
        "name": "SAP Community Young Enterprise Innovator Grant",
        "provider": "SAP Labs India",
        "amount": 65000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Grant for MCA and tech students who develop ERP extensions, database integration modules, or business automation workflows.",
        "eligibility_criteria": "MCA or B.Tech student; Submission of an ERP or database automation mini-project; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-12-20"
    },

    # CORPORATE & TECHNICAL EDUCATION SCHOLARSHIPS
    {
        "name": "Tata Trusts Technical Education Excellence Grant",
        "provider": "Tata Trusts",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Need-cum-merit educational award by Tata Trusts supporting deserving undergraduate and postgraduate students in technical, engineering, and computer application degrees.",
        "eligibility_criteria": "Annual family income not exceeding ₹4.5 Lakhs; Minimum 70% marks or 7.0 CGPA; Enrolled in recognized technical college.",
        "course": "MCA, B.Tech CSE, B.Tech IT, B.Tech ECE",
        "department": "Computer Science & Engineering",
        "min_cgpa": 7.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Cummins Scholarship for Technical Students (Maharashtra)",
        "provider": "Cummins India Foundation",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Cummins Foundation scholarship for students from economically disadvantaged families studying in Pune, Jamshedpur, or Phaltan colleges.",
        "eligibility_criteria": "Family annual income below ₹3 Lakhs; Minimum 60% in previous exams; Enrolled in MCA or B.Tech program.",
        "course": "MCA, B.Tech CSE, B.Tech ME, B.Tech EE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-10-31"
    },
    {
        "name": "Reliance Foundation Postgraduate Technical Scholarship",
        "provider": "Reliance Foundation",
        "amount": 100000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Competitive nationwide scholarship for first-year postgraduate students in Computer Science, Artificial Intelligence, and MCA. Selection based on national aptitude test and interview.",
        "eligibility_criteria": "First year MCA or M.Tech student; Minimum 7.5 CGPA; Open to all income categories with preference given to income below ₹15 Lakhs.",
        "course": "MCA, M.Tech CSE, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Cybage Asha Educational Scholarship for Tech Scholars",
        "provider": "Cybage Software CSR",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Cybage Asha trust initiative providing tuition fee support to promising students in Maharashtra who have passion for software engineering and software testing.",
        "eligibility_criteria": "Enrolled in MCA, Computer Engineering, or IT in Pune region; Family income below ₹3 Lakhs; Minimum 60% in graduation.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-10"
    },
    {
        "name": "L&T Build India Fellowship for Technical Students",
        "provider": "Larsen & Toubro",
        "amount": 90000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Full sponsorship program by L&T for technical postgraduates with employment orientation and monthly living allowances.",
        "eligibility_criteria": "B.Tech or MCA student; Consistent first-class academic performance; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech CE, B.Tech EE, B.Tech ME",
        "department": "All Departments",
        "min_cgpa": 7.0,
        "deadline": "2026-12-10"
    },
    {
        "name": "KPIT Sparkle Innovation & Software Fellowship",
        "provider": "KPIT Technologies",
        "amount": 75000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Award honoring students with ground-breaking software designs in autonomous systems, green mobility, and embedded systems.",
        "eligibility_criteria": "Team or individual student entry; Prototype demonstration; Enrolled in MCA or B.Tech engineering; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech ECE",
        "department": "Computer Science & Engineering",
        "min_cgpa": 6.5,
        "deadline": "2026-12-25"
    },
    {
        "name": "HDFC Bank Parivartan Educational Crisis Scholarship",
        "provider": "HDFC Bank",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Crisis support scholarship helping students who are at risk of dropping out due to personal or financial distress in their families.",
        "eligibility_criteria": "Enrolled in college degree course; Facing critical financial crisis; Minimum 55% marks in previous year; Family income below ₹6 LPA.",
        "course": "MCA, B.Tech, MBA",
        "department": "All Departments",
        "min_cgpa": 5.5,
        "deadline": "2026-11-20"
    },
    {
        "name": "Siemens Technical Education Scholarship Program",
        "provider": "Siemens India",
        "amount": 55000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Sponsorship of tuition fees, book allowances, and comprehensive soft skills and tech training for students pursuing technical degrees.",
        "eligibility_criteria": "First year MCA or B.Tech; Government or government-aided college; Family income under ₹2 Lakhs; Minimum 60% in 10th and 12th.",
        "course": "MCA, B.Tech EE, B.Tech ECE, B.Tech ME",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-05"
    },
    {
        "name": "Aditya Birla Capital Scholarship for Meritorious Technical Scholars",
        "provider": "Aditya Birla Capital Foundation",
        "amount": 65000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Educational grant providing financial cover for college fees to high-performing technical students from lower income strata.",
        "eligibility_criteria": "Students in professional technical courses; Annual family income under ₹6 Lakhs; Minimum 7.5 CGPA in current semester.",
        "course": "MCA, B.Tech CSE, B.Tech IT, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-11-30"
    },

    # CENTRAL & NATIONAL SCHOLARSHIPS
    {
        "name": "Central Sector Scheme of Scholarship for College and University Students",
        "provider": "Department of Higher Education (MHRD)",
        "amount": 20000.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "National scholarship scheme for meritorious students who scored above 80th percentile in board exams, providing ₹20,000 annually for postgraduate studies like MCA.",
        "eligibility_criteria": "Above 80th percentile in 12th examination; Annual family income under ₹4.5 Lakhs; Minimum 50% marks in previous semester.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-10-31"
    },
    {
        "name": "Merit-cum-Means Scholarship for Professional and Technical Courses CS",
        "provider": "Ministry of Minority Affairs",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Central government grant for minority students admitted to professional graduate and postgraduate technical programs on merit basis.",
        "eligibility_criteria": "Notified minority community; Family income below ₹2.5 Lakhs; Minimum 50% marks in previous degree.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Prime Minister's Scholarship Scheme (PMSS) for CAPF & AR Wards",
        "provider": "Ministry of Home Affairs, Govt. of India",
        "amount": 36000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Scholarship of ₹3,000 per month for girls (₹36,000/yr) and ₹2,500 for boys pursuing professional degrees like MCA and engineering.",
        "eligibility_criteria": "Wards of deceased/retired Central Armed Police Forces or Assam Rifles personnel; Minimum 60% in minimum entry qualification.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "National Fellowship for OBC Students (NFOBC)",
        "provider": "Ministry of Social Justice & Empowerment",
        "amount": 42000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "UGC administered fellowship for OBC postgraduate students pursuing higher degree programs and advanced research in computer science.",
        "eligibility_criteria": "OBC category certificate; Enrolled in full-time postgraduate course; Minimum 55% marks in graduation.",
        "course": "MCA, M.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-12-15"
    },
    {
        "name": "INSPIRE Fellowship for Advanced Computing and Natural Sciences",
        "provider": "Department of Science and Technology (DST)",
        "amount": 80000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Research grant for top rankers and scholars entering research, machine learning, and data analytics disciplines.",
        "eligibility_criteria": "First rank in university graduation or top 1% in board examination; Minimum 8.0 CGPA; Full-time postgraduate enrollment.",
        "course": "MCA, M.Tech CSE",
        "department": "Computer Science & Engineering",
        "min_cgpa": 8.0,
        "deadline": "2026-11-20"
    },

    # INSTITUTIONAL & ALUMNI SCHOLARSHIPS
    {
        "name": "CampusAI Alumni MCA Academic Excellence Endowment",
        "provider": "CampusAI Alumni Association",
        "amount": 25000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Funded directly by proud alumni of the MCA department to encourage top semester performers in Data Structures, Database Systems, and Cloud Computing.",
        "eligibility_criteria": "Full-time student in Master of Computer Applications; CGPA >= 8.0 in preceding semester; Active participation in campus tech events.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 8.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Dean's Merit List Scholarship for Computer Applications",
        "provider": "Campus Academic Council",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "Direct institutional tuition waiver awarded to students on the Dean's Honor Roll maintaining an exemplary CGPA of 8.5 or higher.",
        "eligibility_criteria": "Current student of MCA; SGPA >= 8.5 in previous semester; Clean disciplinary record; Attendance above 80%.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 8.5,
        "deadline": "2026-10-31"
    },
    {
        "name": "Campus Industry Advisory Cloud & DevOps Innovation Grant",
        "provider": "Industry Advisory Board",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Award presented to MCA and CS students who showcase outstanding semester capstone projects in DevOps CI/CD pipelines, Docker, and Kubernetes.",
        "eligibility_criteria": "Verified deployment of a cloud-native software architecture; Recommended by departmental project guide; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-12-01"
    },
    {
        "name": "Dr. APJ Abdul Kalam Memorial Technical Grant",
        "provider": "University Trust",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Institutional endowment for students developing software solutions aimed at rural empowerment, agricultural intelligence, or smart campus automation.",
        "eligibility_criteria": "Open to all MCA and Engineering students; Working software prototype addressing societal challenge; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Women in Cybersecurity & Network Defense Fellowship",
        "provider": "Campus InfoSec Research Lab",
        "amount": 45000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Specialized scholarship promoting women engineers and MCA scholars who develop vulnerability scanners, cryptography tools, and secure web services.",
        "eligibility_criteria": "Female student in MCA or Computer Science; Coursework or certification in Network Security or Cryptography; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-25"
    },
    {
        "name": "Sir Ratan Tata Trust Higher Technical Education Grant",
        "provider": "Sir Ratan Tata Trust",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Educational grant providing financial cover for college fees to high-performing technical students from lower income strata.",
        "eligibility_criteria": "Students in professional technical courses; Annual family income under ₹4 Lakhs; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-15"
    },
    {
        "name": "J.N. Tata Endowment Merit Award for Technical Postgraduate Studies",
        "provider": "J.N. Tata Endowment",
        "amount": 75000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Prestigious scholarship recognizing intellectual caliber, scientific curiosity, and technical depth in postgraduate computer applications.",
        "eligibility_criteria": "Postgraduate student in MCA or M.Tech; Excellent academic record with minimum 7.5 CGPA; Formal interview evaluation.",
        "course": "MCA, M.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-12-15"
    },
    {
        "name": "Postgraduate Open Source Contributor Fellowship",
        "provider": "Campus Open Source Hub",
        "amount": 25000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial stipend awarded to students who have active GitHub repositories with open source contributions in Python, JavaScript, or database tooling.",
        "eligibility_criteria": "Active GitHub profile with minimum 5 public commits to popular open source projects; Minimum 6.5 CGPA; Enrolled in MCA/CSE.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-12-05"
    },
    {
        "name": "National Scholarship Portal (NSP) Post-Graduate Financial Aid",
        "provider": "Ministry of Electronics and Information Technology (MeitY)",
        "amount": 55000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Central government digital fellowship awarded through National Scholarship Portal for students pursuing postgraduate master's degrees in IT and computer software.",
        "eligibility_criteria": "Enrolled in MCA or M.Sc IT; Family income below ₹6 LPA; Aadhaar linked bank account; Minimum 60% in graduation.",
        "course": "MCA, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.2,
        "deadline": "2026-11-30"
    },
    {
        "name": "Directorate of Technical Education (DTE) Merit Scholarship for MCA Toppers",
        "provider": "DTE Maharashtra",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "State merit scholarship recognizing top rankers in MAH-MCA-CET examination admitted into accredited MCA institutions in Maharashtra.",
        "eligibility_criteria": "Top 100 rank in MAH-MCA-CET entrance; Maharashtra State Domicile; Enrolled in MCA; Minimum 7.0 CGPA.",
        "course": "MCA",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-10-31"
    },
    {
        "name": "Fair and Lovely Career Foundation Postgraduate Tech Award",
        "provider": "Glow & Lovely Foundation",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Educational grant supporting female students from modest backgrounds to fund tuition fees and competitive exam preparation in technology.",
        "eligibility_criteria": "Female students pursuing MCA or B.Tech; Family annual income not exceeding ₹4 LPA; Minimum 60% in graduation.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Sahu Jain Trust Educational Need-Cum-Merit Scholarship",
        "provider": "Sahu Jain Trust",
        "amount": 25000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial scholarship for deserving students pursuing technical degrees in computer applications, software engineering, and business administration.",
        "eligibility_criteria": "Family income under ₹3 LPA; Minimum 60% in previous exams; Enrolled in recognized university.",
        "course": "MCA, B.Tech, MBA",
        "department": "All Departments",
        "min_cgpa": 6.0,
        "deadline": "2026-11-20"
    },
    {
        "name": "Maharashtra State Technical Board Merit Scholarship",
        "provider": "MSBTE / DTE",
        "amount": 25000.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "State technical merit grant for students who transitioned from diploma or BCA to professional engineering or MCA degrees with distinction.",
        "eligibility_criteria": "Maharashtra domicile; Distinction (>75%) in qualifying diploma or degree; Minimum 6.8 CGPA in MCA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.8,
        "deadline": "2026-10-31"
    },
    {
        "name": "Kishore Vaigyanik Protsahan Yojana (KVPY) Extended Fellowship",
        "provider": "Department of Science and Technology (DST)",
        "amount": 84000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "National research fellowship promoting computational innovation and algorithmic computer science projects among university scholars.",
        "eligibility_criteria": "High aptitude in mathematics and computer algorithms; Minimum 7.5 CGPA; Full-time enrolled candidate.",
        "course": "MCA, B.Tech CSE, M.Tech",
        "department": "Computer Science & Engineering",
        "min_cgpa": 7.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Accenture Digital Skills Tech Scholarship",
        "provider": "Accenture India",
        "amount": 55000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "CSR scholarship for students demonstrating expertise in Cloud Modernization, Data Engineering, and Full Stack Enterprise Applications.",
        "eligibility_criteria": "MCA or B.Tech CS/IT; CGPA >= 7.0; Family income under ₹5 Lakhs; Active software development portfolio.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-12-10"
    },
    {
        "name": "Capgemini STEM Empowerment Grant for Female Techies",
        "provider": "Capgemini India",
        "amount": 48000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Grant encouraging young women in technology to pursue advanced degrees in computer applications, artificial intelligence, and cloud platforms.",
        "eligibility_criteria": "Female student in MCA or Computer Engineering; Minimum 6.5 CGPA; Family income under ₹4.5 LPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-25"
    },
    {
        "name": "Infosys InStep Academic Merit Bursary",
        "provider": "Infosys Limited",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Bursary awarded to outstanding postgraduate computer students demonstrating high performance in distributed systems and software engineering.",
        "eligibility_criteria": "Enrolled in MCA or B.Tech; CGPA >= 7.5; Completed projects in Java or Python systems.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "State Tribal Development Department Education Freeship",
        "provider": "Tribal Development Department, Maharashtra",
        "amount": 80000.0,
        "eligibility_status": "Eligible",
        "application_status": "Approved",
        "description": "Direct tuition freeship for ST students studying professional computer applications in recognized colleges across Maharashtra.",
        "eligibility_criteria": "ST category with valid tribe validity certificate; Maharashtra domicile; No income cap for freeship scheme.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 5.0,
        "deadline": "2026-12-15"
    },
    {
        "name": "Vidyasaarathi Corporate CSR Education Scholarship",
        "provider": "NSDL e-Governance / Vidyasaarathi",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Online CSR scholarship portal grant matching corporate donors with deserving MCA and engineering students from economically disadvantaged families.",
        "eligibility_criteria": "Family income under ₹3.5 LPA; Minimum 60% in 10th, 12th, and graduation; Enrolled in full-time MCA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Kotak Kanya Scholarship for Female Technical Scholars",
        "provider": "Kotak Education Foundation",
        "amount": 100000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Annual scholarship of ₹1 Lakh per year for meritorious girl students from underprivileged families pursuing professional degrees in technology and computer applications.",
        "eligibility_criteria": "Female student only; Family income under ₹3.2 LPA; Minimum 75% in 12th / graduation; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-12-15"
    },
    {
        "name": "L'Oréal India For Young Women in Science & Tech Scholarship",
        "provider": "L'Oréal India",
        "amount": 85000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Promotes scientific and technical careers among promising young women pursuing higher education in computational science, software engineering, and MCA.",
        "eligibility_criteria": "Female student in science/tech degree; Family income under ₹4 LPA; Minimum 70% in graduation; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-20"
    },
    {
        "name": "ONGC Foundation Scholarship for Meritorious SC/ST Students",
        "provider": "ONGC Foundation",
        "amount": 48000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "CSR scholarship by Oil and Natural Gas Corporation providing annual financial aid to SC/ST students enrolled in professional engineering, geology, and computer applications.",
        "eligibility_criteria": "SC/ST student; Family income under ₹4.5 LPA; Minimum 60% in graduation; Regular full-time student.",
        "course": "MCA, B.Tech CSE, B.Tech ME, B.Tech EE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "Federal Bank Hormis Memorial Foundation Technical Scholarship",
        "provider": "Federal Bank Officers Association",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Sponsorship of tuition fees for students belonging to low income families admitted under government quota in professional engineering and computer application programs.",
        "eligibility_criteria": "Admitted through state entrance merit list; Family income under ₹3 LPA; Minimum 6.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-10"
    },
    {
        "name": "DLP India Postgraduate Technology Scholarship",
        "provider": "DLP India EdTech Foundation",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Scholarship awarded to students pursuing distance or regular postgraduate IT degrees with emphasis on artificial intelligence and cloud certifications.",
        "eligibility_criteria": "Enrolled in MCA or M.Sc IT; Minimum 6.0 CGPA; Completed at least one industry tech certification.",
        "course": "MCA, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-12-05"
    },
    {
        "name": "G. P. Birla Educational Foundation Scholarship",
        "provider": "G. P. Birla Trust",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Scholarship for exceptionally bright students from financially constrained backgrounds studying in recognized science and computer colleges.",
        "eligibility_criteria": "Minimum 80% in 12th / 70% in graduation; Family income below ₹3 LPA; Minimum 7.0 CGPA in current course.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-25"
    },
    {
        "name": "Sitaram Jindal Foundation Technical Scholarship",
        "provider": "Sitaram Jindal Foundation",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Philanthropic financial grant for students of technical degree courses like MCA and engineering who belong to economically weaker sections.",
        "eligibility_criteria": "Family income not exceeding ₹2.5 LPA; Minimum 60% for boys and 55% for girls in previous exam; Regular student.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Sant Nirankari Mandal Higher Technical Education Scholarship",
        "provider": "Sant Nirankari Charitable Foundation",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial assistance covering college tuition fees for meritorious students pursuing professional courses in approved institutions.",
        "eligibility_criteria": "Regular student admitted through merit; Family income less than ₹3.5 LPA; Minimum 60% in previous qualification.",
        "course": "MCA, B.Tech, MBA",
        "department": "All Departments",
        "min_cgpa": 6.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "Post-Matric Scholarship for Differently Abled Students (National)",
        "provider": "Department of Empowerment of Persons with Disabilities",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Government of India financial aid including book grant, disability allowance, and tuition fee reimbursement for students with disabilities in technical programs.",
        "eligibility_criteria": "Minimum 40% disability with valid certificate; Family income under ₹2.5 LPA; Admitted to recognized MCA/B.Tech.",
        "course": "MCA, B.Tech, MBA",
        "department": "All Departments",
        "min_cgpa": 5.5,
        "deadline": "2026-12-15"
    },
    {
        "name": "National Fellowship for Persons with Disabilities (NFPwD)",
        "provider": "UGC & Department of Empowerment of PwD",
        "amount": 75000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "UGC fellowship program empowering students with disabilities to pursue master's and research programs in computer science, software engineering, and data systems.",
        "eligibility_criteria": "PwD certificate with >= 40% disability; Admitted to full-time MCA or M.Tech; Minimum 55% in graduation.",
        "course": "MCA, M.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-12-10"
    },
    {
        "name": "Government of Maharashtra Merit-cum-Means Post Graduate Technical Award",
        "provider": "Directorate of Higher & Technical Education",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "State government academic grant awarded to top students enrolled in post-graduate professional programs including Master of Computer Applications.",
        "eligibility_criteria": "Maharashtra domicile; Family income below ₹6 LPA; Minimum 65% aggregate in graduation; Minimum 7.0 CGPA.",
        "course": "MCA, M.Tech",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-10-31"
    },
    {
        "name": "Indian Oil Educational Scholarship Scheme for Technical Students",
        "provider": "Indian Oil Corporation Limited (IOCL)",
        "amount": 36000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "IOCL CSR initiative awarding ₹3,000 per month to meritorious students pursuing full-time technical and computer application degrees.",
        "eligibility_criteria": "Enrolled in 1st year MCA or B.Tech; Family income under ₹1 LPA (relaxable up to ₹3 LPA); Minimum 65% in qualifying exam.",
        "course": "MCA, B.Tech CSE, B.Tech ME, B.Tech EE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-20"
    },
    {
        "name": "NTPC Scholarship Scheme for Scheduled Caste & Tribe Students",
        "provider": "National Thermal Power Corporation (NTPC)",
        "amount": 36000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial scholarship by NTPC for SC, ST, and physically challenged students pursuing higher technical education in recognized colleges.",
        "eligibility_criteria": "SC/ST/PwD student; Full-time enrolled in MCA or Engineering; Minimum 60% in 1st year exams; Good academic record.",
        "course": "MCA, B.Tech CSE, B.Tech EE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "BHEL Educational Sponsorship for Engineering and Tech Scholars",
        "provider": "Bharat Heavy Electricals Limited (BHEL)",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Public sector technical scholarship for students enrolled in professional engineering and computer software courses from low income families.",
        "eligibility_criteria": "Family annual income below ₹2 LPA; Minimum 65% in 12th/graduation; Minimum 6.5 CGPA in current semester.",
        "course": "MCA, B.Tech ME, B.Tech EE, B.Tech CSE",
        "department": "All Departments",
        "min_cgpa": 6.5,
        "deadline": "2026-11-15"
    },
    {
        "name": "Mahindra All India Talent Scholarship (MAITS)",
        "provider": "K. C. Mahindra Education Trust",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Encourages students from underprivileged backgrounds who have transitioned into technical and computer application studies.",
        "eligibility_criteria": "First year student in technical degree/diploma; Family income under ₹1.5 LPA; Minimum 60% marks in previous examination.",
        "course": "MCA, B.Tech",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-10-31"
    },
    {
        "name": "Marubeni India Meritorious Technical Scholarship",
        "provider": "Marubeni India Pvt. Ltd.",
        "amount": 45000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Corporate CSR grant awarded to talented students in computing and engineering disciplines with high academic standing.",
        "eligibility_criteria": "Minimum 75% marks in previous degree; Family income not exceeding ₹4 LPA; Minimum 7.2 CGPA in MCA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.2,
        "deadline": "2026-11-25"
    },
    {
        "name": "Legrand Empowering Scholarship for Women in Technology",
        "provider": "Legrand India",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Promotes gender diversity in higher technical education by sponsoring tuition fees of girl students pursuing MCA and engineering.",
        "eligibility_criteria": "Female students only; Family income under ₹5 LPA; Minimum 70% in 10th, 12th, and graduation; Minimum 6.8 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech EE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.8,
        "deadline": "2026-11-15"
    },
    {
        "name": "Rolls-Royce Unnati Scholarship for Women in Engineering and Tech",
        "provider": "Rolls-Royce India",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Supports female students enrolled in technology and computing degrees with financial aid, technical workshops, and industry mentoring.",
        "eligibility_criteria": "Female student in MCA, CSE, or IT; Minimum 65% marks in graduation; Annual family income below ₹4 LPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-20"
    },
    {
        "name": "Schaeffler India Hope Engineering and Tech Scholarship",
        "provider": "Schaeffler India",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Educational empowerment program for students studying in technical and professional institutions in Maharashtra and Gujarat.",
        "eligibility_criteria": "Enrolled in MCA or B.Tech; Family income below ₹5 LPA; Minimum 60% in previous exams; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech ME, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Tata Housing Scholarships for Meritorious Girl Students",
        "provider": "Tata Housing CSR",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Annual financial scholarship helping meritorious girl students complete professional degrees in computer applications and civil engineering.",
        "eligibility_criteria": "Girl students admitted to second year of degree course; Family income under ₹3 LPA; Minimum 6.5 CGPA.",
        "course": "MCA, B.Tech CE, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-12-10"
    },
    {
        "name": "North South Foundation (NSF) College Scholarship",
        "provider": "North South Foundation India",
        "amount": 30000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Merit-cum-means scholarship for top-tier rankers entering professional college courses who have high financial need.",
        "eligibility_criteria": "Rank in top 10% in entrance exam; Family income less than ₹1 LPA; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech, MBA",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Foundation for Excellence (FFE) Engineering and Tech Scholarship",
        "provider": "Foundation for Excellence India",
        "amount": 50000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Pre-eminent scholarship for academically gifted students in computer science, MCA, and engineering facing severe financial barriers.",
        "eligibility_criteria": "Admitted to degree through state/national entrance exam; Family income under ₹3 LPA; Minimum 7.0 CGPA.",
        "course": "MCA, B.Tech CSE, B.Tech IT",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.0,
        "deadline": "2026-11-30"
    },
    {
        "name": "Keep India Smiling Foundational Scholarship for Young Techies",
        "provider": "Colgate-Palmolive India",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "CSR scholarship providing financial grants to students pursuing vocational, undergraduate, and post-graduate computer degrees.",
        "eligibility_criteria": "Minimum 60% in previous degree; Family income below ₹5 LPA; Enrolled in full-time course.",
        "course": "MCA, B.Tech",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.0,
        "deadline": "2026-11-10"
    },
    {
        "name": "Federal-Mogul Anand Scholarship for Technical Scholars",
        "provider": "Anand Group India",
        "amount": 35000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Financial assistance program for students studying technical programs in Pune, Nashik, and Mumbai industrial belts.",
        "eligibility_criteria": "Family income below ₹3 LPA; Minimum 60% in previous qualification; Regular attendance.",
        "course": "MCA, B.Tech ME, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.2,
        "deadline": "2026-11-25"
    },
    {
        "name": "SBI Foundation Youth for India Technical Fellowship",
        "provider": "State Bank of India Foundation",
        "amount": 60000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Prestigious fellowship supporting students working on rural digital empowerment, fintech interfaces, and software automation for cooperatives.",
        "eligibility_criteria": "MCA, MBA, or B.Tech student; Passion for technology-driven social change; Minimum 6.5 CGPA.",
        "course": "MCA, MBA, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 6.5,
        "deadline": "2026-12-15"
    },
    {
        "name": "Canara Bank Vidya Jyothi Educational Concession Scheme",
        "provider": "Canara Bank CSR",
        "amount": 25000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Direct financial aid for college students from low income families to pay tuition and purchase educational computer hardware.",
        "eligibility_criteria": "Family income under ₹2.5 LPA; Minimum 60% in graduation; Valid enrollment in approved degree.",
        "course": "MCA, B.Tech, MBA",
        "department": "All Departments",
        "min_cgpa": 6.0,
        "deadline": "2026-11-15"
    },
    {
        "name": "Bank of Baroda Achievers Award for Higher Technical Education",
        "provider": "Bank of Baroda",
        "amount": 40000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Merit award for top academic scorers in computer applications, banking software technologies, and quantitative methods.",
        "eligibility_criteria": "Top 5% rank in previous university semester; Minimum 7.5 CGPA; Full-time postgraduate enrollment.",
        "course": "MCA, MBA, B.Tech CSE",
        "department": "Master of Computer Applications",
        "min_cgpa": 7.5,
        "deadline": "2026-11-30"
    },
    {
        "name": "Indian Institute of Science Computational Excellence Grant",
        "provider": "IISc Bangalore Extended Outreach",
        "amount": 90000.0,
        "eligibility_status": "Eligible",
        "application_status": "Open",
        "description": "Outreach grant supporting promising postgraduate computer students working on algorithms, quantum logic, or deep learning architectures.",
        "eligibility_criteria": "Enrolled in MCA or M.Tech; CGPA >= 8.0; Submission of research paper draft or open-source AI project.",
        "course": "MCA, M.Tech CSE",
        "department": "Computer Science & Engineering",
        "min_cgpa": 8.0,
        "deadline": "2026-12-20"
    }
]

print(f"\nChecking existing scholarship names to avoid duplicate records...")
cursor.execute("SELECT LOWER(TRIM(scholarship_name)) FROM scholarships")
existing_names = {row[0] for row in cursor.fetchall()}

inserted_count = 0
for s in NEW_SCHOLARSHIPS:
    if s["name"].lower().strip() not in existing_names:
        cursor.execute("""
            INSERT INTO scholarships (
                student_id, scholarship_name, provider, amount,
                eligibility_status, application_status,
                description, eligibility_criteria, course, department, min_cgpa, deadline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            None,  # Available to all students in catalog
            s["name"],
            s["provider"],
            s["amount"],
            s["eligibility_status"],
            s["application_status"],
            s["description"],
            s["eligibility_criteria"],
            s["course"],
            s["department"],
            s["min_cgpa"],
            s["deadline"]
        ))
        existing_names.add(s["name"].lower().strip())
        inserted_count += 1

conn.commit()
print(f"Successfully inserted {inserted_count} new realistic scholarship records!")

# ── 5. Enhance Internships with skills_required and description ─────────────
cursor.execute("SELECT internship_id, role, domain, company_name, eligibility FROM internships")
internships = cursor.fetchall()

domain_skills_map = {
    "Software Development": ("Python, Java, Data Structures, Algorithms, Git, REST APIs", "Develop robust software solutions, write clean unit-tested code, collaborate with engineering teams on backend architectures and software lifecycle."),
    "Cloud Computing": ("AWS, Azure, Docker, Kubernetes, Linux, Terraform, CI/CD", "Design cloud infrastructure, manage containerized microservices, automate deployments, and monitor cloud resources."),
    "Data Analytics": ("Python, SQL, Tableau, PowerBI, Pandas, Statistics, Excel", "Analyze large business datasets, generate insightful visual dashboards, write complex analytical SQL queries, and present actionable metrics."),
    "Cybersecurity": ("Network Security, Cryptography, Ethical Hacking, Linux, SIEM, Firewalls", "Perform vulnerability assessments, audit system logs, test web application security against OWASP vulnerabilities, and implement network security policies."),
    "AI/ML": ("Python, PyTorch, TensorFlow, Scikit-Learn, NLP, Deep Learning, OpenCV", "Build and train predictive machine learning models, preprocess high-dimensional datasets, deploy NLP algorithms, and optimize neural networks."),
    "Web Development": ("React, JavaScript, HTML5, CSS3, Node.js, Express, MongoDB, SQL", "Design responsive user interfaces, integrate RESTful APIs, manage frontend state, and deliver accessible web applications."),
    "Consulting": ("Business Analysis, Communication, Agile, Excel, Problem Solving", "Consult with enterprise clients, gather business requirements, document specifications, and assist in digital transformation projects."),
    "DevOps": ("CI/CD, Jenkins, Docker, Linux, Shell Scripting, Git, Kubernetes, Ansible", "Automate build and deployment pipelines, manage container orchestration, implement infrastructure as code, and optimize server reliability."),
    "ERP Systems": ("ERP Systems, SQL, Database Management, Business Workflows, SAP/Oracle", "Assist in Enterprise Resource Planning (ERP) customization, database integrity checks, SQL reporting, and campus ERP module deployments."),
    "Mobile Development": ("Flutter, Dart, React Native, Android, REST APIs, SQLite", "Develop cross-platform mobile applications, optimize mobile UI/UX, integrate local storage with SQLite, and connect mobile apps to backend services."),
    "Healthcare IT": ("Python, SQL, HL7, Database Management, Data Security, HIPAA", "Build secure healthcare data processing systems, ensure regulatory compliance, and develop reliable clinical database pipelines."),
    "Product Development": ("Product Management, User Stories, UI/UX, Agile, SQL, Analytics", "Collaborate on product roadmaps, conduct user feedback interviews, define MVP feature sets, and coordinate with engineering squads."),
    "E-Commerce": ("Java, Distributed Systems, Microservices, Redis, Spring Boot, MySQL", "Work on high-throughput e-commerce platforms, payment gateway integrations, distributed caching, and order management systems."),
    "Cloud Services": ("AWS, CloudFormation, Linux, Python, Networking, Cloud Security", "Assist enterprise customers in deploying cloud solutions, debugging network configurations, and monitoring high-availability architectures."),
    "Software Engineering": ("C++, Java, Object Oriented Programming, System Design, Multithreading", "Build mission-critical operating systems software, developer tooling, and distributed backend infrastructure with low latency."),
    "AI Research": ("Deep Learning, Transformer Models, PyTorch, Linear Algebra, Python", "Conduct cutting-edge research in generative models, natural language processing, transformer architectures, and publish research papers."),
    "Database": ("Oracle Database, SQL, PL/SQL, Performance Tuning, Database Administration", "Design normalized relational database schemas, optimize slow queries, manage indexes, write stored procedures, and maintain backup integrity."),
    "Enterprise Software": ("Java, Spring Boot, Microservices, Kafka, PostgreSQL, Docker", "Develop enterprise-grade software applications, integrate message queues, design secure REST endpoints, and implement business domain logic."),
    "AI & Automation": ("Python, Robotic Process Automation, Machine Learning, APIs, OCR", "Build automated bots for enterprise repetitive tasks, integrate machine learning classification, and streamline business processes."),
    "Analytics": ("Python, R, Statistical Modeling, Machine Learning, PowerBI, SQL", "Deliver predictive analytics solutions, build regression and clustering models, and visualize key performance indicators."),
    "Risk Advisory": ("IT Audit, Risk Management, Cybersecurity, Compliance, Information Security", "Evaluate enterprise IT risk controls, assess compliance frameworks, perform internal security audits, and prepare risk reports."),
    "Digital Transformation": ("Cloud, Agile, Enterprise Architecture, Analytics, Change Management", "Support enterprise clients in migrating legacy monoliths to modern cloud-first and API-driven architectures."),
    "Technology Consulting": ("Full Stack, Cloud, Database Architecture, Business Consulting", "Advise industry clients on modern tech stacks, evaluate architecture feasibility, and implement scalable digital solutions."),
    "Telecom": ("5G Networks, TCP/IP, Linux, Python, Network Protocols, Telecom Systems", "Work on modern telecommunications infrastructure, core routing protocols, network function virtualization, and connectivity optimization."),
    "Space Technology": ("Embedded C, Real-time Systems, Signal Processing, Python, MATLAB", "Participate in satellite data telemetry processing, embedded flight software algorithms, and space mission software engineering."),
    "Defence Research": ("C++, Python, Image Processing, Embedded Linux, Cryptography, DSP", "Develop defense simulation models, real-time image processing algorithms, and secure embedded communication systems."),
    "Digital Payments": ("Java, Spring Boot, Microservices, Kafka, Redis, Security, SQL", "Build ultra-secure payment processing microservices, handle concurrent transactions, implement encryption, and ensure financial compliance."),
    "Fintech": ("Python, Django, PostgreSQL, Blockchain, Financial APIs, Cryptography", "Develop financial technology services, build fraud detection mechanisms, and integrate banking APIs for instantaneous settlements."),
    "Food Tech": ("Python, Node.js, Geolocation, Logistics Algorithms, MongoDB, Redis", "Optimize delivery route planning algorithms, build real-time order tracking services, and maintain responsive customer-facing interfaces."),
    "Mobility": ("Go, Python, Microservices, Distributed Systems, Kafka, GPS Tracking", "Engineer real-time ride matching engines, dynamic pricing algorithms, and resilient driver dispatch systems."),
    "EdTech": ("React, Node.js, Video Streaming, MongoDB, WebSockets, Python", "Build interactive learning management systems, live video classroom services, and AI-driven quiz evaluation engines."),
    "SaaS": ("Ruby on Rails / Python, React, PostgreSQL, Docker, Multi-tenant Architecture", "Develop multi-tenant SaaS features, automated billing workflows, customer CRM tools, and scalable RESTful APIs."),
    "Cloud Data Protection": ("Go, C++, Linux Kernel, Distributed Storage, AWS, Data Backup", "Implement enterprise data protection solutions, distributed deduplication, snapshot management, and disaster recovery engines.")
}

updated_internships = 0
for row in internships:
    iid, role, domain, company, eligibility = row
    skills, desc = domain_skills_map.get(domain, ("Python, SQL, Software Engineering, Problem Solving", f"Internship opportunity at {company} in {domain} focusing on {role}."))
    cursor.execute("""
        UPDATE internships
        SET skills_required = ?, description = ?
        WHERE internship_id = ?
    """, (skills, desc, iid))
    updated_internships += 1

conn.commit()
print(f"Updated {updated_internships} internships with skills_required and description.")

# Verify counts and schema
cursor.execute("SELECT COUNT(*) FROM scholarships")
total_sch = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM internships")
total_int = cursor.fetchone()[0]

print(f"\nFinal Statistics:")
print(f"  Total Scholarships in database: {total_sch}")
print(f"  Total Internships in database:   {total_int}")

conn.close()
print("Migration and IR seeding complete successfully!")

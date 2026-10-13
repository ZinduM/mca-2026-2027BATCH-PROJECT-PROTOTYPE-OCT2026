"""
CampusAI - Database Setup & Seed Script
Creates the SQLite database, all tables, and populates with realistic records.
Features realistic CGPA distributions across all academic records.

Usage:
    python database/database_setup.py

This will create/recreate the database at database/campus_ai.db
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Base, Department, Student, AcademicRecord, Attendance,
    Fee, Scholarship, Internship, Document, Faculty
)

# ── Configuration ──────────────────────────────────────────────────────────────

DB_DIR = os.path.join(PROJECT_ROOT, "database")
DB_PATH = os.path.join(DB_DIR, "campus_ai.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

random.seed(42)  # For reproducible data generation

# ── Realistic Data Lists ──────────────────────────────────────────────────────

MALE_FIRST_NAMES = [
    "Aarav", "Arjun", "Rahul", "Amit", "Prashant", "Vikram", "Sanjay", "Deepak",
    "Manish", "Suresh", "Rajesh", "Aakash", "Nikhil", "Rohan", "Karan", "Vivek",
    "Gaurav", "Ankit", "Sahil", "Mohit", "Aditya", "Varun", "Harsh", "Pranav",
    "Kunal", "Tushar", "Yash", "Dhruv", "Ishaan", "Aryan", "Rishabh", "Akshay",
    "Mayank", "Kartik", "Siddharth", "Dev", "Tanmay", "Omkar", "Shubham", "Sachin",
    "Abhinav", "Ayush", "Nakul", "Parth", "Aman", "Ravi", "Vikas", "Ashish",
    "Neeraj", "Tarun", "Hemant", "Piyush", "Ritesh", "Sameer", "Arun", "Bhavesh",
    "Chirag", "Darshan", "Eshan", "Farhan", "Govind", "Hitesh", "Jayesh", "Krishna"
]

FEMALE_FIRST_NAMES = [
    "Priya", "Ananya", "Sneha", "Pooja", "Divya", "Ishita", "Riya", "Kavita",
    "Meera", "Nisha", "Shreya", "Aisha", "Sakshi", "Neha", "Tanvi", "Simran",
    "Aditi", "Kritika", "Bhavna", "Pallavi", "Swati", "Anjali", "Rashmi", "Komal",
    "Sonal", "Jyoti", "Asha", "Deepika", "Madhuri", "Lata", "Aaradhya", "Bhumi",
    "Charvi", "Diya", "Esha", "Falguni", "Gauri", "Hina", "Isha", "Juhi",
    "Kiara", "Lavanya", "Mansi", "Nandini", "Ojasvi", "Payal", "Radha", "Saanvi",
    "Tanya", "Uma", "Vani", "Yamini", "Zara", "Rhea", "Mahi", "Trisha"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Joshi", "Mishra",
    "Agarwal", "Reddy", "Nair", "Iyer", "Pillai", "Rao", "Desai", "Shah",
    "Mehta", "Chauhan", "Thakur", "Pandey", "Yadav", "Tiwari", "Saxena", "Jain",
    "Kapoor", "Malhotra", "Bhatia", "Khanna", "Sinha", "Bose", "Das", "Roy",
    "Sen", "Chatterjee", "Banerjee", "Mukherjee", "Chopra", "Goswami", "Dutta",
    "Menon", "Hegde", "Kulkarni", "Patil", "Naik", "Rathore", "Rajput", "Dubey",
    "Trivedi", "Bhatt", "Shukla"
]

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune",
    "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal",
    "Patna", "Vadodara", "Surat", "Coimbatore", "Kochi", "Chandigarh",
    "Dehradun", "Noida", "Gurgaon", "Mysore", "Visakhapatnam", "Ranchi",
    "Bhubaneswar", "Thiruvananthapuram", "Guwahati", "Raipur"
]

CATEGORIES = ["General", "OBC", "SC", "ST", "EWS"]
CATEGORY_WEIGHTS = [0.35, 0.30, 0.15, 0.10, 0.10]

# ── Department & Subject Configuration ─────────────────────────────────────────

DEPARTMENTS = [
    {"name": "Computer Science & Engineering", "hod": "Dr. Ramesh Sharma", "faculty_count": 15, "location": "Block A"},
    {"name": "Information Technology", "hod": "Dr. Sunil Verma", "faculty_count": 12, "location": "Block A"},
    {"name": "Electronics & Communication", "hod": "Dr. Anita Desai", "faculty_count": 12, "location": "Block B"},
    {"name": "Mechanical Engineering", "hod": "Dr. Vikram Thakur", "faculty_count": 14, "location": "Block C"},
    {"name": "Civil Engineering", "hod": "Dr. Pradeep Kulkarni", "faculty_count": 10, "location": "Block D"},
    {"name": "Electrical Engineering", "hod": "Dr. Sunita Rao", "faculty_count": 10, "location": "Block B"},
    {"name": "Master of Computer Applications", "hod": "Dr. Kavita Joshi", "faculty_count": 10, "location": "Block A"},
    {"name": "Business Administration", "hod": "Dr. Rajiv Mehta", "faculty_count": 8, "location": "Block E"},
]

DEPT_COURSES = {
    "Computer Science & Engineering": "B.Tech CSE",
    "Information Technology": "B.Tech IT",
    "Electronics & Communication": "B.Tech ECE",
    "Mechanical Engineering": "B.Tech ME",
    "Civil Engineering": "B.Tech CE",
    "Electrical Engineering": "B.Tech EE",
    "Master of Computer Applications": "MCA",
    "Business Administration": "MBA",
}

DEPT_MAX_YEAR = {
    "Computer Science & Engineering": 4,
    "Information Technology": 4,
    "Electronics & Communication": 4,
    "Mechanical Engineering": 4,
    "Civil Engineering": 4,
    "Electrical Engineering": 4,
    "Master of Computer Applications": 3,
    "Business Administration": 2,
}

STUDENT_DISTRIBUTION = {
    "Computer Science & Engineering": 400,
    "Information Technology": 350,
    "Electronics & Communication": 250,
    "Mechanical Engineering": 250,
    "Civil Engineering": 200,
    "Electrical Engineering": 150,
    "Master of Computer Applications": 250,
    "Business Administration": 150,
}

# Slight academic variation by department
DEPT_OFFSETS = {
    "Computer Science & Engineering": 0.25,
    "Information Technology": 0.18,
    "Master of Computer Applications": 0.10,
    "Business Administration": 0.05,
    "Electronics & Communication": -0.05,
    "Electrical Engineering": -0.10,
    "Mechanical Engineering": -0.18,
    "Civil Engineering": -0.22,
}

SUBJECTS_BY_DEPT = {
    "Computer Science & Engineering": {
        1: ["Mathematics I", "Physics", "Programming in C", "Digital Logic Design", "English Communication", "Engineering Drawing"],
        2: ["Mathematics II", "Chemistry", "Data Structures", "Computer Architecture", "Environmental Science", "Communication Skills"],
        3: ["Discrete Mathematics", "Object Oriented Programming", "Database Management Systems", "Operating Systems", "Computer Networks", "Data Communication"],
        4: ["Design & Analysis of Algorithms", "Software Engineering", "Web Technologies", "Theory of Computation", "Probability & Statistics", "Microprocessors"],
        5: ["Artificial Intelligence", "Compiler Design", "Computer Graphics", "Information Security", "Cloud Computing", "Machine Learning"],
        6: ["Deep Learning", "Big Data Analytics", "Internet of Things", "Blockchain Technology", "Natural Language Processing", "Mobile Computing"],
        7: ["Distributed Systems", "Cyber Security", "Project Phase I", "Software Testing", "DevOps Engineering", "Data Science"],
        8: ["Project Phase II", "Seminar", "Advanced Algorithms", "Quantum Computing", "Edge Computing", "Research Methodology"],
    },
    "Information Technology": {
        1: ["Mathematics I", "Physics", "Programming Fundamentals", "Digital Electronics", "English Communication", "Engineering Drawing"],
        2: ["Mathematics II", "Chemistry", "Data Structures & Algorithms", "Computer Organization", "Environmental Science", "Technical Writing"],
        3: ["Discrete Mathematics", "Java Programming", "Database Systems", "Operating Systems", "Computer Networks", "Web Development"],
        4: ["Algorithm Design", "Software Engineering", "Full Stack Development", "Information Theory", "Statistics", "System Administration"],
        5: ["Cloud Computing", "Information Security", "Data Mining", "Artificial Intelligence", "Mobile App Development", "DevOps"],
        6: ["Big Data Technologies", "IoT & Embedded Systems", "Machine Learning", "Cyber Security", "Network Security", "Agile Methodologies"],
        7: ["Distributed Computing", "Blockchain", "Project Phase I", "IT Governance", "Data Analytics", "Research Methods"],
        8: ["Project Phase II", "Seminar", "Advanced Networking", "IT Strategy", "Emerging Technologies", "Technical Communication"],
    },
    "Electronics & Communication": {
        1: ["Mathematics I", "Physics", "Basic Electronics", "Circuit Theory", "English Communication", "Engineering Drawing"],
        2: ["Mathematics II", "Chemistry", "Digital Electronics", "Network Analysis", "Environmental Science", "Communication Skills"],
        3: ["Signals & Systems", "Analog Electronics", "Electromagnetic Theory", "Digital Signal Processing", "Microprocessors", "Control Systems"],
        4: ["Communication Systems", "VLSI Design", "Antenna & Wave Propagation", "Embedded Systems", "Linear Algebra", "Instrumentation"],
        5: ["Wireless Communication", "Optical Communication", "Radar Engineering", "Robotics", "Image Processing", "Sensor Technology"],
        6: ["Satellite Communication", "Biomedical Electronics", "Advanced DSP", "IoT Systems", "Nano Electronics", "Power Electronics"],
        7: ["5G Technologies", "MEMS", "Project Phase I", "Research Methodology", "Advanced Communication", "System Design"],
        8: ["Project Phase II", "Seminar", "Quantum Electronics", "Advanced VLSI", "RF Engineering", "Technical Writing"],
    },
    "Mechanical Engineering": {
        1: ["Mathematics I", "Physics", "Engineering Mechanics", "Engineering Drawing", "English Communication", "Workshop Practice"],
        2: ["Mathematics II", "Chemistry", "Thermodynamics", "Material Science", "Environmental Science", "Manufacturing Processes"],
        3: ["Fluid Mechanics", "Strength of Materials", "Kinematics of Machines", "Machine Drawing", "Numerical Methods", "Engineering Metallurgy"],
        4: ["Heat Transfer", "Dynamics of Machines", "Machine Design I", "Manufacturing Technology", "Industrial Engineering", "CAD/CAM"],
        5: ["IC Engines", "Refrigeration & AC", "Machine Design II", "Finite Element Analysis", "Mechatronics", "Quality Engineering"],
        6: ["Automobile Engineering", "Robotics", "Power Plant Engineering", "Turbomachinery", "Production Planning", "Industrial Automation"],
        7: ["Advanced Manufacturing", "Renewable Energy", "Project Phase I", "Operations Research", "Vibration Analysis", "Computational Fluid Dynamics"],
        8: ["Project Phase II", "Seminar", "Advanced Thermodynamics", "Composite Materials", "Additive Manufacturing", "Research Methodology"],
    },
    "Civil Engineering": {
        1: ["Mathematics I", "Physics", "Engineering Mechanics", "Engineering Drawing", "English Communication", "Surveying I"],
        2: ["Mathematics II", "Chemistry", "Building Materials", "Surveying II", "Environmental Science", "Geology"],
        3: ["Structural Analysis I", "Fluid Mechanics", "Geotechnical Engineering I", "Building Construction", "Concrete Technology", "Numerical Methods"],
        4: ["Structural Analysis II", "Geotechnical Engineering II", "Transportation Engineering I", "Environmental Engineering I", "Hydrology", "Estimation & Costing"],
        5: ["RCC Design", "Steel Structures", "Transportation Engineering II", "Environmental Engineering II", "Water Resources", "Construction Management"],
        6: ["Prestressed Concrete", "Foundation Engineering", "Advanced Structural Design", "Traffic Engineering", "Remote Sensing & GIS", "Earthquake Engineering"],
        7: ["Bridge Engineering", "Advanced Geotechnical", "Project Phase I", "Green Building", "Urban Planning", "Research Methodology"],
        8: ["Project Phase II", "Seminar", "Smart Infrastructure", "Sustainable Construction", "Disaster Management", "Technical Communication"],
    },
    "Electrical Engineering": {
        1: ["Mathematics I", "Physics", "Basic Electrical Engineering", "Circuit Theory", "English Communication", "Engineering Drawing"],
        2: ["Mathematics II", "Chemistry", "Electromagnetic Fields", "Network Analysis", "Environmental Science", "Communication Skills"],
        3: ["Electrical Machines I", "Power Systems I", "Analog Electronics", "Control Systems", "Signals & Systems", "Electrical Measurements"],
        4: ["Electrical Machines II", "Power Systems II", "Digital Electronics", "Power Electronics", "Instrumentation", "Numerical Methods"],
        5: ["Power System Protection", "Electric Drives", "Renewable Energy Systems", "High Voltage Engineering", "Switchgear", "PLC & SCADA"],
        6: ["Smart Grid Technology", "Power Quality", "Advanced Control Systems", "Electrical Machine Design", "Energy Management", "Industrial Automation"],
        7: ["HVDC Transmission", "Power System Stability", "Project Phase I", "Electric Vehicle Technology", "AI in Power Systems", "Research Methodology"],
        8: ["Project Phase II", "Seminar", "Advanced Power Electronics", "Distributed Generation", "Energy Storage", "Technical Writing"],
    },
    "Master of Computer Applications": {
        1: ["Mathematical Foundations", "Programming with Python", "Computer Organization", "Database Management Systems", "Web Technologies", "Communication Skills"],
        2: ["Data Structures & Algorithms", "Java Programming", "Operating Systems", "Software Engineering", "Computer Networks", "Statistics & Probability"],
        3: ["Artificial Intelligence", "Cloud Computing", "Full Stack Development", "Mobile Application Development", "Cyber Security", "Machine Learning"],
        4: ["Deep Learning", "Big Data Analytics", "DevOps & CI/CD", "Natural Language Processing", "Blockchain Technology", "Research Methodology"],
        5: ["Project Phase I", "Advanced AI/ML", "Internet of Things", "Data Science", "Quantum Computing", "Seminar"],
        6: ["Project Phase II", "Dissertation", "Industry Internship", "Advanced Topics in CS", "Emerging Technologies", "Presentation Skills"],
    },
    "Business Administration": {
        1: ["Principles of Management", "Financial Accounting", "Business Economics", "Organizational Behavior", "Business Communication", "Quantitative Methods"],
        2: ["Marketing Management", "Financial Management", "Human Resource Management", "Operations Management", "Business Analytics", "Legal Environment"],
        3: ["Strategic Management", "International Business", "Supply Chain Management", "Digital Marketing", "Entrepreneurship", "Business Research Methods"],
        4: ["Project & Dissertation", "Corporate Governance", "Leadership & Ethics", "Innovation Management", "Capstone Simulation", "Seminar"],
    },
}

SCHOLARSHIP_NAMES = [
    "Merit-Based Excellence Award", "National Scholarship Portal (NSP)",
    "Post-Matric Scholarship for SC/ST", "Central Sector Scholarship",
    "INSPIRE Scholarship", "Pragati Scholarship for Girls",
    "State Government Merit Scholarship", "Minority Community Scholarship",
    "Sports Achievement Scholarship", "Research Fellowship Grant",
    "Industry Sponsored Scholarship", "Alumni Association Award",
    "Need-Based Financial Aid", "Innovation & Startup Grant",
    "International Exchange Scholarship"
]

SCHOLARSHIP_PROVIDERS = [
    "Ministry of Education", "UGC", "AICTE", "State Government",
    "University Trust", "Industry Partner", "Alumni Association",
    "Private Foundation", "CSIR", "DST"
]

INTERNSHIP_DATA = [
    {"company": "Tata Consultancy Services", "domain": "Software Development", "role": "Software Developer Intern", "location": "Mumbai", "duration": "6 months", "stipend": 25000, "eligibility": "B.Tech/MCA 3rd year+, CGPA > 7.0"},
    {"company": "Infosys", "domain": "Cloud Computing", "role": "Cloud Engineer Intern", "location": "Bangalore", "duration": "6 months", "stipend": 22000, "eligibility": "B.Tech CSE/IT, CGPA > 6.5"},
    {"company": "Wipro", "domain": "Data Analytics", "role": "Data Analyst Intern", "location": "Hyderabad", "duration": "4 months", "stipend": 20000, "eligibility": "B.Tech/MCA, CGPA > 6.0"},
    {"company": "HCL Technologies", "domain": "Cybersecurity", "role": "Security Analyst Intern", "location": "Noida", "duration": "6 months", "stipend": 28000, "eligibility": "B.Tech CSE/IT/ECE, CGPA > 7.0"},
    {"company": "Tech Mahindra", "domain": "AI/ML", "role": "ML Engineer Intern", "location": "Pune", "duration": "5 months", "stipend": 30000, "eligibility": "B.Tech/MCA, CGPA > 7.5"},
    {"company": "Cognizant", "domain": "Web Development", "role": "Full Stack Developer Intern", "location": "Chennai", "duration": "4 months", "stipend": 18000, "eligibility": "B.Tech CSE/IT/MCA, CGPA > 6.0"},
    {"company": "Accenture", "domain": "Consulting", "role": "Technology Consultant Intern", "location": "Mumbai", "duration": "6 months", "stipend": 35000, "eligibility": "B.Tech/MBA, CGPA > 7.0"},
    {"company": "Capgemini", "domain": "DevOps", "role": "DevOps Engineer Intern", "location": "Bangalore", "duration": "5 months", "stipend": 24000, "eligibility": "B.Tech CSE/IT, CGPA > 6.5"},
    {"company": "L&T Infotech", "domain": "ERP Systems", "role": "ERP Consultant Intern", "location": "Mumbai", "duration": "6 months", "stipend": 22000, "eligibility": "B.Tech/MCA/MBA, CGPA > 6.0"},
    {"company": "Mindtree", "domain": "Mobile Development", "role": "Mobile App Developer Intern", "location": "Bangalore", "duration": "4 months", "stipend": 20000, "eligibility": "B.Tech CSE/IT/MCA, CGPA > 6.5"},
    {"company": "Persistent Systems", "domain": "Healthcare IT", "role": "Software Developer Intern", "location": "Pune", "duration": "6 months", "stipend": 22000, "eligibility": "B.Tech/MCA, CGPA > 6.5"},
    {"company": "Zoho Corporation", "domain": "Product Development", "role": "Product Engineer Intern", "location": "Chennai", "duration": "6 months", "stipend": 26000, "eligibility": "B.Tech CSE/IT, CGPA > 7.0"},
    {"company": "Flipkart", "domain": "E-Commerce", "role": "SDE Intern", "location": "Bangalore", "duration": "3 months", "stipend": 60000, "eligibility": "B.Tech CSE/IT, CGPA > 8.0"},
    {"company": "Amazon India", "domain": "Cloud Services", "role": "Cloud Support Intern", "location": "Hyderabad", "duration": "6 months", "stipend": 55000, "eligibility": "B.Tech/MCA, CGPA > 7.5"},
    {"company": "Microsoft India", "domain": "Software Engineering", "role": "SWE Intern", "location": "Hyderabad", "duration": "3 months", "stipend": 80000, "eligibility": "B.Tech CSE, CGPA > 8.5"},
    {"company": "Google India", "domain": "AI Research", "role": "Research Intern", "location": "Bangalore", "duration": "3 months", "stipend": 85000, "eligibility": "B.Tech/M.Tech CSE, CGPA > 9.0"},
    {"company": "Oracle India", "domain": "Database", "role": "Database Developer Intern", "location": "Bangalore", "duration": "6 months", "stipend": 40000, "eligibility": "B.Tech CSE/IT, CGPA > 7.0"},
    {"company": "SAP Labs India", "domain": "Enterprise Software", "role": "Associate Developer Intern", "location": "Bangalore", "duration": "6 months", "stipend": 45000, "eligibility": "B.Tech/MCA, CGPA > 7.5"},
    {"company": "IBM India", "domain": "AI & Automation", "role": "AI Developer Intern", "location": "Pune", "duration": "6 months", "stipend": 35000, "eligibility": "B.Tech CSE/IT/MCA, CGPA > 7.0"},
    {"company": "Deloitte", "domain": "Analytics", "role": "Business Analyst Intern", "location": "Gurgaon", "duration": "4 months", "stipend": 40000, "eligibility": "B.Tech/MBA, CGPA > 7.0"},
    {"company": "KPMG", "domain": "Risk Advisory", "role": "Technology Risk Intern", "location": "Mumbai", "duration": "4 months", "stipend": 35000, "eligibility": "B.Tech/MCA, CGPA > 7.0"},
    {"company": "PwC India", "domain": "Digital Transformation", "role": "Digital Consultant Intern", "location": "Kolkata", "duration": "5 months", "stipend": 38000, "eligibility": "B.Tech/MBA, CGPA > 7.0"},
    {"company": "EY India", "domain": "Technology Consulting", "role": "Tech Consultant Intern", "location": "Chandigarh", "duration": "4 months", "stipend": 32000, "eligibility": "B.Tech/MCA/MBA, CGPA > 6.5"},
    {"company": "Reliance Jio", "domain": "Telecom", "role": "Network Engineer Intern", "location": "Mumbai", "duration": "6 months", "stipend": 30000, "eligibility": "B.Tech ECE/EE, CGPA > 6.5"},
    {"company": "Bharti Airtel", "domain": "Telecom", "role": "Telecom Engineer Intern", "location": "Gurgaon", "duration": "5 months", "stipend": 25000, "eligibility": "B.Tech ECE/EE, CGPA > 6.0"},
    {"company": "ISRO", "domain": "Space Technology", "role": "Research Trainee", "location": "Bangalore", "duration": "6 months", "stipend": 20000, "eligibility": "B.Tech/M.Tech ECE/EE/ME, CGPA > 8.0"},
    {"company": "DRDO", "domain": "Defence Research", "role": "Junior Research Fellow", "location": "Delhi", "duration": "12 months", "stipend": 31000, "eligibility": "B.Tech/M.Tech, CGPA > 7.5"},
    {"company": "Larsen & Toubro", "domain": "Construction", "role": "Graduate Engineer Trainee", "location": "Chennai", "duration": "12 months", "stipend": 28000, "eligibility": "B.Tech CE/ME/EE, CGPA > 6.5"},
    {"company": "Tata Motors", "domain": "Automotive", "role": "Design Engineer Intern", "location": "Pune", "duration": "6 months", "stipend": 25000, "eligibility": "B.Tech ME, CGPA > 7.0"},
    {"company": "Mahindra & Mahindra", "domain": "Automotive", "role": "R&D Intern", "location": "Mumbai", "duration": "6 months", "stipend": 27000, "eligibility": "B.Tech ME/EE, CGPA > 7.0"},
    {"company": "Bajaj Auto", "domain": "Manufacturing", "role": "Manufacturing Intern", "location": "Pune", "duration": "4 months", "stipend": 20000, "eligibility": "B.Tech ME, CGPA > 6.5"},
    {"company": "Godrej Industries", "domain": "Product Design", "role": "Product Design Intern", "location": "Mumbai", "duration": "5 months", "stipend": 22000, "eligibility": "B.Tech ME/CE, CGPA > 6.5"},
    {"company": "HDFC Bank", "domain": "Banking Technology", "role": "Tech Associate Intern", "location": "Mumbai", "duration": "4 months", "stipend": 30000, "eligibility": "B.Tech CSE/IT/MCA, CGPA > 7.0"},
    {"company": "ICICI Bank", "domain": "Fintech", "role": "Fintech Developer Intern", "location": "Hyderabad", "duration": "6 months", "stipend": 28000, "eligibility": "B.Tech CSE/IT, CGPA > 6.5"},
    {"company": "Paytm", "domain": "Digital Payments", "role": "Backend Developer Intern", "location": "Noida", "duration": "3 months", "stipend": 40000, "eligibility": "B.Tech CSE/IT/MCA, CGPA > 7.5"},
    {"company": "Razorpay", "domain": "Fintech", "role": "SDE Intern", "location": "Bangalore", "duration": "3 months", "stipend": 50000, "eligibility": "B.Tech CSE, CGPA > 8.0"},
    {"company": "PhonePe", "domain": "Digital Payments", "role": "Software Engineer Intern", "location": "Bangalore", "duration": "4 months", "stipend": 45000, "eligibility": "B.Tech CSE/IT, CGPA > 7.5"},
    {"company": "Swiggy", "domain": "Food Tech", "role": "Data Science Intern", "location": "Bangalore", "duration": "3 months", "stipend": 50000, "eligibility": "B.Tech/MCA, CGPA > 7.5"},
    {"company": "Zomato", "domain": "Food Tech", "role": "Frontend Developer Intern", "location": "Gurgaon", "duration": "4 months", "stipend": 40000, "eligibility": "B.Tech CSE/IT, CGPA > 7.0"},
    {"company": "Ola Cabs", "domain": "Mobility", "role": "Platform Engineer Intern", "location": "Bangalore", "duration": "4 months", "stipend": 45000, "eligibility": "B.Tech CSE/IT, CGPA > 7.5"},
    {"company": "Byju's", "domain": "EdTech", "role": "Content Developer Intern", "location": "Bangalore", "duration": "3 months", "stipend": 20000, "eligibility": "B.Tech/MCA/MBA, CGPA > 6.0"},
    {"company": "Unacademy", "domain": "EdTech", "role": "Product Intern", "location": "Bangalore", "duration": "4 months", "stipend": 25000, "eligibility": "B.Tech/MCA, CGPA > 6.5"},
    {"company": "Freshworks", "domain": "SaaS", "role": "SDE Intern", "location": "Chennai", "duration": "6 months", "stipend": 40000, "eligibility": "B.Tech CSE/IT, CGPA > 7.5"},
    {"company": "Druva", "domain": "Cloud Data Protection", "role": "Cloud Engineer Intern", "location": "Pune", "duration": "6 months", "stipend": 45000, "eligibility": "B.Tech CSE/IT, CGPA > 7.5"},
    {"company": "Tata Steel", "domain": "Steel Manufacturing", "role": "Process Engineer Intern", "location": "Jamshedpur", "duration": "6 months", "stipend": 22000, "eligibility": "B.Tech ME/CE, CGPA > 6.5"},
    {"company": "NTPC", "domain": "Power Generation", "role": "Engineering Trainee", "location": "Delhi", "duration": "6 months", "stipend": 25000, "eligibility": "B.Tech EE/ME, CGPA > 7.0"},
    {"company": "BHEL", "domain": "Heavy Engineering", "role": "Engineering Intern", "location": "Bhopal", "duration": "6 months", "stipend": 20000, "eligibility": "B.Tech ME/EE, CGPA > 6.5"},
    {"company": "Hindustan Unilever", "domain": "FMCG", "role": "Management Intern", "location": "Mumbai", "duration": "3 months", "stipend": 50000, "eligibility": "MBA, CGPA > 7.5"},
    {"company": "ITC Limited", "domain": "FMCG", "role": "Operations Intern", "location": "Kolkata", "duration": "4 months", "stipend": 35000, "eligibility": "MBA/B.Tech, CGPA > 7.0"},
    {"company": "Procter & Gamble", "domain": "Consumer Goods", "role": "Supply Chain Intern", "location": "Mumbai", "duration": "3 months", "stipend": 55000, "eligibility": "MBA/B.Tech ME, CGPA > 7.5"},
]

DOCUMENT_DATA = [
    {"title": "B.Tech Computer Science Syllabus 2024-25", "category": "Syllabus", "content": "This document outlines the complete curriculum for B.Tech Computer Science & Engineering program. The curriculum covers core subjects including Data Structures, Algorithms, Database Management, Operating Systems, Computer Networks, Software Engineering, Artificial Intelligence, Machine Learning, Cloud Computing, and Cybersecurity. Each semester includes theoretical courses, laboratory sessions, and project work. Students must complete a minimum of 160 credits for graduation. Elective courses are available from 5th semester onwards. Industrial training is mandatory in the 7th semester. The final year project spans two semesters with continuous evaluation."},
    {"title": "MCA Program Curriculum 2024-25", "category": "Syllabus", "content": "Master of Computer Applications (MCA) is a 3-year postgraduate program designed to develop professional skills in computer applications. The curriculum includes Programming with Python and Java, Data Structures, Database Management, Web Technologies, Software Engineering, Operating Systems, Computer Networks, AI/ML, Cloud Computing, Mobile Development, and Cybersecurity. Students undergo industry internship in the final semester. Research methodology and dissertation are integral parts of the program."},
    {"title": "MBA Program Structure 2024-25", "category": "Syllabus", "content": "The MBA program is a 2-year full-time postgraduate program. First year covers core management subjects including Financial Accounting, Marketing Management, Human Resource Management, Operations Management, Business Analytics, and Organizational Behavior. Second year offers specializations in Finance, Marketing, HR, Operations, and IT Management. Summer internship after first year is mandatory. Final semester includes a capstone project and industry collaboration."},
    {"title": "Examination Rules & Regulations", "category": "Exam Rules", "content": "University examinations are conducted at the end of each semester. Internal assessment carries 40% weightage and external examination carries 60% weightage. Minimum passing marks: 40% in each subject (internal + external combined). Students must maintain minimum 75% attendance to be eligible for examinations. Re-examination facility available for failed subjects. Maximum of 3 attempts per subject. Grace marks policy: up to 5 marks in aggregate. Malpractice during examination leads to cancellation of the subject and potential debarment. Hall ticket must be carried for all examinations. Mobile phones are strictly prohibited in examination halls. Late arrival beyond 30 minutes is not permitted."},
    {"title": "Scholarship Eligibility Criteria", "category": "Scholarship", "content": "Merit-based scholarships require minimum CGPA of 8.0. Need-based scholarships are available for students from economically weaker sections with family income below 8 lakhs per annum. SC/ST students are eligible for post-matric scholarships from the government. Sports scholarships available for national/state level players. Research scholarships available for M.Tech and PhD students. Scholarship renewal requires maintaining the minimum CGPA criteria. Application deadline is within 30 days of semester registration. Required documents include income certificate, caste certificate (if applicable), academic transcripts, and bonafide certificate."},
    {"title": "Anti-Ragging Policy", "category": "Policy", "content": "The institution follows strict anti-ragging policy as per UGC regulations. Ragging in any form is a criminal offense. Anti-ragging committee and squad are active throughout the year. Students can report incidents through the anti-ragging helpline, email, or anonymous complaint box. Punishment for ragging includes suspension, expulsion, FIR with police, and debarment from placements. All students must sign an anti-ragging affidavit at the time of admission. Freshers orientation program includes anti-ragging awareness sessions."},
    {"title": "Library Rules and Services", "category": "Policy", "content": "The central library is open from 8:00 AM to 10:00 PM on all working days. Digital library access is available 24/7. Students can borrow up to 4 books at a time for a period of 14 days. Reference books and journals are for in-library use only. Late fee of Rs. 5 per day per book. Lost books must be replaced or compensated at current market price plus 25% penalty. Inter-library loan facility available. Online databases include IEEE, ACM Digital Library, Springer, and ScienceDirect. Photocopying services available at nominal charges."},
    {"title": "Hostel Rules and Regulations", "category": "Policy", "content": "Hostel accommodation is available on first-come-first-served basis. Separate hostels for boys and girls. Mess facility is compulsory for all hostel residents. Hostel timings: Gate closes at 10:00 PM. Overnight stay outside requires prior written permission from warden. Electrical appliances like heaters and irons are not allowed in rooms. Visitors are allowed only in the visitor room during designated hours. Damage to hostel property will be charged to the responsible student. Ragging is strictly prohibited. Wi-Fi facility available in all hostels."},
    {"title": "Placement Cell Guidelines", "category": "Placement", "content": "The Training and Placement Cell coordinates campus recruitment activities. Students must register with the placement cell by 7th semester. Minimum eligibility: 60% aggregate marks with no active backlogs. Students can participate in a maximum of 3 placement drives. Once selected, the student is out of the placement process. Pre-placement training includes aptitude tests, group discussions, and mock interviews. Companies visiting campus include TCS, Infosys, Wipro, HCL, Cognizant, Accenture, Capgemini, and many more. Average package ranges from 4-8 LPA. Dream and super-dream categories allow additional placement opportunities."},
    {"title": "Fee Structure 2024-25", "category": "Fee Structure", "content": "B.Tech annual tuition fee: Rs. 1,20,000. MCA annual tuition fee: Rs. 85,000. MBA annual tuition fee: Rs. 1,50,000. Hostel fee: Rs. 60,000 per annum (including mess). Laboratory fee: Rs. 10,000 per annum. Library fee: Rs. 5,000 per annum. Examination fee: Rs. 3,000 per semester. Development fee: Rs. 15,000 per annum. Caution deposit: Rs. 10,000 (refundable). Late payment penalty: 1% per month. Installment facility available: 2 installments per semester. Fee concession available for merit and economically weaker students."},
    {"title": "Research & Development Policy", "category": "Academic", "content": "The institution encourages research and innovation among faculty and students. Seed funding available up to Rs. 5 lakhs for research projects. Publication incentive of Rs. 10,000 for SCI/Scopus indexed journal papers. Conference travel grants available for paper presentations. Intellectual property rights assistance provided for patents. Collaboration with industries for sponsored research. Research labs equipped with high-performance computing facilities. Annual research symposium organized for student presentations. Faculty development programs conducted regularly."},
    {"title": "Code of Conduct for Students", "category": "Policy", "content": "Students must maintain discipline and decorum on campus. Identity card must be worn at all times within the campus. Dress code: formal attire during lab sessions and presentations. Attendance minimum: 75% per subject per semester. Usage of mobile phones during lectures is prohibited. Consumption of alcohol, tobacco, and drugs on campus is strictly forbidden. Damage to institutional property attracts monetary penalty. Students must follow laboratory safety protocols. Academic dishonesty including plagiarism will result in disciplinary action. Respectful behavior towards faculty, staff, and fellow students is expected at all times."},
    {"title": "Internship Policy and Guidelines", "category": "Internship", "content": "Industrial internship is mandatory for all undergraduate and postgraduate programs. B.Tech students must complete a minimum 6-week internship after 6th semester. MCA students must complete a 4-month internship in the final semester. MBA students must complete an 8-week summer internship after 2nd semester. Internship must be in a registered organization relevant to the student's discipline. Students must submit internship report and present findings to a faculty panel. Internship evaluation carries credit points. The placement cell maintains a database of internship opportunities. Students can also identify their own internship with approval from the department."},
    {"title": "Academic Calendar 2024-25", "category": "Academic", "content": "Odd Semester: July 15 to December 15. Even Semester: January 10 to May 30. Mid-semester examinations: 8th week of semester. End-semester examinations: Last 2 weeks. Summer vacation: June 1 to July 14. Winter break: December 20 to January 9. National holidays observed as per government calendar. Orientation for new students: First week of odd semester. Convocation ceremony: March. Annual cultural festival: October. Annual technical festival: February. Sports week: November. Parent-teacher meeting: After mid-semester results."},
    {"title": "Grading System Explanation", "category": "Academic", "content": "The institution follows a 10-point CGPA grading system. Grade points: O (Outstanding) = 10, A+ = 9, A = 8, B+ = 7, B = 6, C = 5, P (Pass) = 4, F (Fail) = 0. SGPA is calculated as weighted average of grade points in a semester. CGPA is cumulative across all semesters. Percentage equivalent = (CGPA - 0.5) × 10. Minimum CGPA for graduation: 5.0. Dean's List: SGPA >= 9.0. Chancellor's Medal: Highest CGPA in the graduating batch. Improvement examination allowed for up to 4 subjects. Best of the two attempts is considered for SGPA calculation."},
    {"title": "IT Infrastructure and Labs", "category": "Infrastructure", "content": "The campus houses 15 state-of-the-art computer laboratories with over 500 workstations. All labs are equipped with latest software including Visual Studio, PyCharm, Eclipse, MATLAB, AutoCAD, and ANSYS. High-speed internet connectivity of 1 Gbps. Cloud computing lab with AWS and Azure access. AI/ML lab with GPU workstations (NVIDIA Tesla V100). IoT and Embedded Systems lab. Network Security lab with ethical hacking tools. Each department has a dedicated research lab. 24/7 server room with redundant power supply. Campus-wide Wi-Fi coverage. Video conferencing facilities in all seminar halls."},
    {"title": "Student Welfare and Counseling", "category": "Welfare", "content": "Student counseling center provides academic and personal counseling. Professional counselors available on all working days. Mental health awareness programs conducted monthly. Peer support groups for first-year students. Career guidance and mentoring programs. Financial aid office assists with scholarship applications. Health center with resident doctor and nurse. Ambulance service available 24/7. Insurance coverage for all enrolled students. Grievance redressal cell addresses student complaints within 15 working days. Equal opportunity cell for differently-abled students."},
    {"title": "Sports and Cultural Activities", "category": "Extracurricular", "content": "The institution has facilities for cricket, football, basketball, volleyball, badminton, table tennis, and athletics. Indoor sports complex with gymnasium, yoga room, and chess room. Annual inter-college sports meet. Cultural committee organizes events including music, dance, drama, and art. Technical clubs include coding club, robotics club, AI club, and IoT club. Annual hackathon and coding competitions. NSS and NCC units active on campus. Community service initiatives including blood donation camps and environmental awareness drives. Student chapters of IEEE, ACM, and CSI active on campus."},
    {"title": "Environmental and Sustainability Policy", "category": "Policy", "content": "The institution is committed to environmental sustainability. Solar panels installed on rooftops generating 500 KW. Rainwater harvesting system with storage capacity of 50,000 liters. Waste segregation and recycling programs active. Paperless administration initiative. Energy-efficient LED lighting throughout campus. Electric vehicle charging stations. Green belt covering 30% of campus area. Annual tree plantation drive. Ban on single-use plastics on campus. Environmental audit conducted annually. Green building certification for new constructions."},
    {"title": "Alumni Association Charter", "category": "Alumni", "content": "The alumni association connects graduates with the institution and current students. Annual alumni meet organized in January. Alumni mentoring program for final year students. Alumni entrepreneurship cell supports startup ventures. Distinguished alumni awards given annually. Alumni contribution fund for infrastructure development. Job referral program through alumni network. Guest lectures and workshops by industry alumni. Alumni chapters in major cities across India and abroad. Online alumni portal for networking and job postings. Alumni can access library and sports facilities with alumni card."},
]

# ── Faculty Names ──────────────────────────────────────────────────────────────

FACULTY_TITLES = ["Dr.", "Prof.", "Mr.", "Ms.", "Mrs."]
FACULTY_ROLES = ["Professor", "Associate Professor", "Assistant Professor", "Senior Lecturer", "Lecturer"]

# ── Helper Functions ───────────────────────────────────────────────────────────

def generate_phone():
    """Generate a realistic Indian phone number."""
    prefixes = ["98", "97", "96", "95", "94", "93", "91", "90", "89", "88", "87", "86", "85", "84", "83", "82", "81", "80", "79", "78", "77", "76", "75", "74", "73", "72", "70"]
    return random.choice(prefixes) + "".join([str(random.randint(0, 9)) for _ in range(8)])


def generate_dob(year_of_admission, course):
    """Generate a realistic date of birth based on admission year and course."""
    if course in ["MCA", "MBA", "M.Tech"]:
        birth_year = year_of_admission - random.randint(21, 26)
    else:
        birth_year = year_of_admission - random.randint(17, 20)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{birth_year}-{month:02d}-{day:02d}"


def calculate_grade(total_marks):
    """Calculate grade based on total marks (out of 100)."""
    if total_marks >= 90: return "O"
    elif total_marks >= 80: return "A+"
    elif total_marks >= 70: return "A"
    elif total_marks >= 60: return "B+"
    elif total_marks >= 50: return "B"
    elif total_marks >= 40: return "C"
    elif total_marks >= 35: return "P"
    else: return "F"


def generate_student_cgpa(dept_name: str) -> float:
    """
    Generate realistic CGPA following the requested distribution:
    - Below 5.0: ~4% (Small number)
    - 5.0 - 5.9: ~12% (Some students)
    - 6.0 - 6.9: ~28% (Many students)
    - 7.0 - 7.9: ~32% (Many students)
    - 8.0 - 8.9: ~19% (Many students)
    - 9.0 - 10.0: ~5% (Some students)
    """
    roll = random.random()
    offset = DEPT_OFFSETS.get(dept_name, 0.0)

    # 1. Below 5.0
    if roll < 0.04:
        val = random.choice([3.8, 4.1, 4.2, 4.3, 4.5, 4.6, 4.7, 4.8, 4.9]) + (offset * 0.1)
    # 2. 5.0 - 5.9
    elif roll < 0.16:
        val = random.choice([5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9]) + (offset * 0.15)
    # 3. 6.0 - 6.9
    elif roll < 0.44:
        val = random.choice([6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9]) + (offset * 0.2)
    # 4. 7.0 - 7.9
    elif roll < 0.76:
        val = random.choice([7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9]) + (offset * 0.2)
    # 5. 8.0 - 8.9
    elif roll < 0.95:
        val = random.choice([8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9]) + (offset * 0.2)
    # 6. 9.0 - 10.0
    else:
        val = random.choice([9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8]) + (offset * 0.1)

    return round(max(3.2, min(9.9, val)), 2)


# ── Main Setup Function ───────────────────────────────────────────────────────

def create_database():
    """Create the database and all tables, then populate with sample data."""

    # Remove existing database if present
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"  Removed existing database: {DB_PATH}")

    os.makedirs(DB_DIR, exist_ok=True)

    # Create engine and tables
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("=" * 60)
    print("  CampusAI Database Setup")
    print("=" * 60)

    # ── 1. Create Departments ──────────────────────────────────────────────
    print("\n[1/9] Creating Departments...")
    dept_objects = {}
    for dept_data in DEPARTMENTS:
        dept = Department(
            department_name=dept_data["name"],
            hod_name=dept_data["hod"],
            total_faculty=dept_data["faculty_count"],
            location=dept_data["location"]
        )
        session.add(dept)
        session.flush()
        dept_objects[dept_data["name"]] = dept.department_id
    session.commit()
    print(f"  [OK] Created {len(DEPARTMENTS)} departments")

    # ── 2. Create Faculty ──────────────────────────────────────────────────
    print("\n[2/9] Creating Faculty...")
    faculty_count = 0
    for dept_name, dept_id in dept_objects.items():
        num_faculty = next(d["faculty_count"] for d in DEPARTMENTS if d["name"] == dept_name)
        for i in range(num_faculty):
            gender = random.choice(["Male", "Female"])
            if gender == "Male":
                fname = random.choice(MALE_FIRST_NAMES)
                title = random.choice(["Dr.", "Prof.", "Mr."])
            else:
                fname = random.choice(FEMALE_FIRST_NAMES)
                title = random.choice(["Dr.", "Prof.", "Ms.", "Mrs."])
            lname = random.choice(LAST_NAMES)
            full_name = f"{title} {fname} {lname}"
            email = f"{fname.lower()}.{lname.lower()}{random.randint(1,99)}@campusai.edu.in"
            role = FACULTY_ROLES[min(i, len(FACULTY_ROLES) - 1)]

            faculty = Faculty(
                name=full_name,
                email=email,
                department_id=dept_id,
                role=role,
                password="faculty123"
            )
            session.add(faculty)
            faculty_count += 1
    session.commit()
    print(f"  [OK] Created {faculty_count} faculty members")

    # ── 3. Create Students ─────────────────────────────────────────────────
    print("\n[3/9] Creating Students (2000)...")
    student_ids_by_dept = {}
    student_total = 0
    used_emails = set()
    used_rolls = set()

    for dept_name, count in STUDENT_DISTRIBUTION.items():
        dept_id = dept_objects[dept_name]
        course = DEPT_COURSES[dept_name]
        max_year = DEPT_MAX_YEAR[dept_name]
        dept_student_ids = []

        for i in range(count):
            gender = random.choices(["Male", "Female"], weights=[0.55, 0.45])[0]
            fname = random.choice(MALE_FIRST_NAMES if gender == "Male" else FEMALE_FIRST_NAMES)
            lname = random.choice(LAST_NAMES)

            year = random.randint(1, max_year)
            semester = year * 2 - random.choice([0, 1])
            admission_year = 2026 - year

            # Unique roll number
            dept_code = dept_name[:3].upper()
            while True:
                roll = f"{dept_code}{admission_year % 100:02d}{random.randint(1000, 9999)}"
                if roll not in used_rolls:
                    used_rolls.add(roll)
                    break

            # Unique email
            while True:
                email = f"{fname.lower()}.{lname.lower()}{random.randint(1, 9999)}@student.campusai.edu.in"
                if email not in used_emails:
                    used_emails.add(email)
                    break

            phone = generate_phone()
            dob = generate_dob(admission_year, course)
            city = random.choice(CITIES)
            category = random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS)[0]

            student = Student(
                roll_number=roll,
                name=f"{fname} {lname}",
                email=email,
                phone=phone,
                gender=gender,
                date_of_birth=dob,
                department_id=dept_id,
                course=course,
                year=year,
                semester=semester,
                admission_year=admission_year,
                city=city,
                category=category,
                password="student123"
            )
            session.add(student)
            session.flush()
            dept_student_ids.append((student.student_id, dept_name, semester, year))
            student_total += 1

            if student_total % 500 == 0:
                print(f"    ... {student_total} students created")

        student_ids_by_dept[dept_name] = dept_student_ids

    session.commit()
    print(f"  [OK] Created {student_total} students")

    # ── 4. Create Academic Records with Realistic CGPA ─────────────────────
    print("\n[4/9] Creating Academic Records...")
    record_count = 0

    for dept_name, students in student_ids_by_dept.items():
        subjects_map = SUBJECTS_BY_DEPT[dept_name]

        for sid, dname, sem, yr in students:
            # Current semester subjects
            sem_key = min(sem, max(subjects_map.keys()))
            subjects = subjects_map.get(sem_key, subjects_map[1])

            # Realistic CGPA generated for this student
            cgpa = generate_student_cgpa(dept_name)

            # Target marks corresponding to student CGPA
            target_marks = max(30.0, min(98.0, (cgpa * 9.5) + random.uniform(-2.5, 2.5)))

            for subject in subjects:
                jitter = random.uniform(-4.0, 4.0)
                total = max(20.0, min(100.0, round(target_marks + jitter, 1)))
                internal = round(total * 0.4, 1)
                external = round(total - internal, 1)
                grade = calculate_grade(total)

                record = AcademicRecord(
                    student_id=sid,
                    semester=sem,
                    subject_name=subject,
                    internal_marks=internal,
                    external_marks=external,
                    total_marks=total,
                    grade=grade,
                    cgpa=cgpa,
                    academic_year=f"{2025 + (sem % 2)}-{2026 + (sem % 2)}"
                )
                session.add(record)
                record_count += 1

        if record_count % 3000 == 0:
            print(f"    ... {record_count} records created")

    session.commit()
    print(f"  [OK] Created {record_count} academic records")

    # ── 5. Create Attendance Records ───────────────────────────────────────
    print("\n[5/9] Creating Attendance Records...")
    attendance_count = 0

    for dept_name, students in student_ids_by_dept.items():
        subjects_map = SUBJECTS_BY_DEPT[dept_name]

        for sid, dname, sem, yr in students:
            sem_key = min(sem, max(subjects_map.keys()))
            subjects = subjects_map.get(sem_key, subjects_map[1])

            base_attendance = random.gauss(78, 12)
            base_attendance = max(40, min(98, base_attendance))

            for subject in subjects:
                total_classes = random.randint(35, 50)
                attend_pct = max(30, min(100, random.gauss(base_attendance, 8)))
                attended = int(total_classes * attend_pct / 100)
                actual_pct = round((attended / total_classes) * 100, 2)

                att = Attendance(
                    student_id=sid,
                    subject_name=subject,
                    total_classes=total_classes,
                    attended_classes=attended,
                    attendance_percent=actual_pct,
                    semester=sem
                )
                session.add(att)
                attendance_count += 1

        if attendance_count % 3000 == 0:
            print(f"    ... {attendance_count} records created")

    session.commit()
    print(f"  [OK] Created {attendance_count} attendance records")

    # ── 6. Create Fee Records ──────────────────────────────────────────────
    print("\n[6/9] Creating Fee Records...")
    fee_count = 0

    fee_by_course = {
        "B.Tech CSE": 120000, "B.Tech IT": 110000, "B.Tech ECE": 110000,
        "B.Tech ME": 105000, "B.Tech CE": 100000, "B.Tech EE": 105000,
        "MCA": 85000, "MBA": 150000
    }

    for dept_name, students in student_ids_by_dept.items():
        course = DEPT_COURSES[dept_name]
        total_fee = fee_by_course.get(course, 100000)

        for sid, dname, sem, yr in students:
            status_roll = random.random()
            if status_roll < 0.65:
                paid = total_fee
                pending = 0
                status = "Paid"
            elif status_roll < 0.85:
                paid = round(total_fee * random.uniform(0.4, 0.8))
                pending = total_fee - paid
                status = "Partial"
            else:
                paid = 0
                pending = total_fee
                status = "Pending"

            scholarship = random.choices(["Yes", "No"], weights=[0.2, 0.8])[0]
            academic_year = f"{2025 + (sem % 2)}-{2026 + (sem % 2)}"

            fee = Fee(
                student_id=sid,
                total_fee=total_fee,
                paid_amount=paid,
                pending_amount=pending,
                payment_status=status,
                scholarship_applied=scholarship,
                academic_year=academic_year
            )
            session.add(fee)
            fee_count += 1

    session.commit()
    print(f"  [OK] Created {fee_count} fee records")

    # ── 7. Create Scholarships ─────────────────────────────────────────────
    print("\n[7/9] Creating Scholarship Records...")
    scholarship_count = 0

    all_student_ids = []
    for students in student_ids_by_dept.values():
        all_student_ids.extend([s[0] for s in students])

    scholarship_students = random.sample(all_student_ids, min(400, len(all_student_ids)))

    for sid in scholarship_students:
        num_scholarships = random.choices([1, 2], weights=[0.8, 0.2])[0]
        for _ in range(num_scholarships):
            sch_name = random.choice(SCHOLARSHIP_NAMES)
            provider = random.choice(SCHOLARSHIP_PROVIDERS)
            amount = random.choice([5000, 10000, 15000, 20000, 25000, 30000, 50000, 75000, 100000])
            eligibility = random.choices(["Eligible", "Not Eligible"], weights=[0.7, 0.3])[0]
            app_status = random.choices(["Approved", "Pending", "Rejected"], weights=[0.4, 0.35, 0.25])[0]

            sch = Scholarship(
                student_id=sid,
                scholarship_name=sch_name,
                provider=provider,
                amount=amount,
                eligibility_status=eligibility,
                application_status=app_status
            )
            session.add(sch)
            scholarship_count += 1

    session.commit()
    print(f"  [OK] Created {scholarship_count} scholarship records")

    # ── 8. Create Internships ──────────────────────────────────────────────
    print("\n[8/9] Creating Internship Listings...")
    for intern_data in INTERNSHIP_DATA:
        deadline_date = datetime(2026, random.randint(1, 12), random.randint(1, 28))
        internship = Internship(
            company_name=intern_data["company"],
            domain=intern_data["domain"],
            role=intern_data["role"],
            location=intern_data["location"],
            duration=intern_data["duration"],
            stipend=intern_data["stipend"],
            eligibility=intern_data["eligibility"],
            deadline=deadline_date.strftime("%Y-%m-%d")
        )
        session.add(internship)
    session.commit()
    print(f"  [OK] Created {len(INTERNSHIP_DATA)} internship listings")

    # ── 9. Create Documents ────────────────────────────────────────────────
    print("\n[9/9] Creating Document Records...")
    for doc_data in DOCUMENT_DATA:
        doc = Document(
            title=doc_data["title"],
            category=doc_data["category"],
            file_path=f"uploads/{doc_data['title'].lower().replace(' ', '_')}.pdf",
            content=doc_data["content"],
            uploaded_date=datetime(2024, random.randint(1, 12), random.randint(1, 28)).strftime("%Y-%m-%d")
        )
        session.add(doc)
    session.commit()
    print(f"  [OK] Created {len(DOCUMENT_DATA)} document records")

    # ── Summary ────────────────────────────────────────────────────────────
    session.close()

    total_records = (
        len(DEPARTMENTS) + faculty_count + student_total +
        record_count + attendance_count + fee_count +
        scholarship_count + len(INTERNSHIP_DATA) + len(DOCUMENT_DATA)
    )

    print("\n" + "=" * 60)
    print("  DATABASE CREATION COMPLETE!")
    print("=" * 60)
    print(f"\n  Database Path: {DB_PATH}")
    print(f"\n  Record Summary:")
    print(f"    Departments:      {len(DEPARTMENTS)}")
    print(f"    Faculty:          {faculty_count}")
    print(f"    Students:         {student_total}")
    print(f"    Academic Records: {record_count}")
    print(f"    Attendance:       {attendance_count}")
    print(f"    Fee Records:      {fee_count}")
    print(f"    Scholarships:     {scholarship_count}")
    print(f"    Internships:      {len(INTERNSHIP_DATA)}")
    print(f"    Documents:        {len(DOCUMENT_DATA)}")
    print(f"    -------------------------")
    print(f"    TOTAL RECORDS:    {total_records}")
    print(f"\n  Default Credentials:")
    print(f"    Faculty Login:  any faculty email / password: faculty123")
    print(f"    Student Login:  any student email / password: student123")
    print("=" * 60)


if __name__ == "__main__":
    create_database()
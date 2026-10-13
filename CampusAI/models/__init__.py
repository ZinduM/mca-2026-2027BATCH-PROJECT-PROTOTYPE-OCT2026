"""
CampusAI - SQLAlchemy ORM Models
Defines all database tables for the College ERP system.
"""

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False, unique=True)
    hod_name = Column(String(100))
    total_faculty = Column(Integer)
    location = Column(String(100))

    # Relationships
    students = relationship('Student', back_populates='department')
    faculty_members = relationship('Faculty', back_populates='department')

    def to_dict(self):
        return {
            'department_id': self.department_id,
            'department_name': self.department_name,
            'hod_name': self.hod_name,
            'total_faculty': self.total_faculty,
            'location': self.location
        }


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    phone = Column(String(15))
    gender = Column(String(10))
    date_of_birth = Column(String(20))
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    course = Column(String(50))
    year = Column(Integer)
    semester = Column(Integer)
    admission_year = Column(Integer)
    city = Column(String(50))
    category = Column(String(30))
    password = Column(String(100))

    # Relationships
    department = relationship('Department', back_populates='students')
    academic_records = relationship('AcademicRecord', back_populates='student', cascade='all, delete-orphan')
    attendance_records = relationship('Attendance', back_populates='student', cascade='all, delete-orphan')
    fee_records = relationship('Fee', back_populates='student', cascade='all, delete-orphan')
    scholarship_records = relationship('Scholarship', back_populates='student', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'roll_number': self.roll_number,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'department_id': self.department_id,
            'course': self.course,
            'year': self.year,
            'semester': self.semester,
            'admission_year': self.admission_year,
            'city': self.city,
            'category': self.category
        }


class AcademicRecord(Base):
    __tablename__ = 'academic_record'

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    semester = Column(Integer)
    subject_name = Column(String(100))
    internal_marks = Column(Float)
    external_marks = Column(Float)
    total_marks = Column(Float)
    grade = Column(String(5))
    cgpa = Column(Float)
    academic_year = Column(String(20))

    # Relationships
    student = relationship('Student', back_populates='academic_records')

    def to_dict(self):
        return {
            'record_id': self.record_id,
            'student_id': self.student_id,
            'semester': self.semester,
            'subject_name': self.subject_name,
            'internal_marks': self.internal_marks,
            'external_marks': self.external_marks,
            'total_marks': self.total_marks,
            'grade': self.grade,
            'cgpa': self.cgpa,
            'academic_year': self.academic_year
        }


class Attendance(Base):
    __tablename__ = 'attendance'

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_name = Column(String(100))
    total_classes = Column(Integer)
    attended_classes = Column(Integer)
    attendance_percent = Column(Float)
    semester = Column(Integer)

    # Relationships
    student = relationship('Student', back_populates='attendance_records')

    def to_dict(self):
        return {
            'attendance_id': self.attendance_id,
            'student_id': self.student_id,
            'subject_name': self.subject_name,
            'total_classes': self.total_classes,
            'attended_classes': self.attended_classes,
            'attendance_percent': self.attendance_percent,
            'semester': self.semester
        }


class Fee(Base):
    __tablename__ = 'fees'

    fee_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    total_fee = Column(Float)
    paid_amount = Column(Float)
    pending_amount = Column(Float)
    payment_status = Column(String(20))
    scholarship_applied = Column(String(5))
    academic_year = Column(String(20))

    # Relationships
    student = relationship('Student', back_populates='fee_records')

    def to_dict(self):
        return {
            'fee_id': self.fee_id,
            'student_id': self.student_id,
            'total_fee': self.total_fee,
            'paid_amount': self.paid_amount,
            'pending_amount': self.pending_amount,
            'payment_status': self.payment_status,
            'scholarship_applied': self.scholarship_applied,
            'academic_year': self.academic_year
        }


class Scholarship(Base):
    __tablename__ = 'scholarships'

    scholarship_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    scholarship_name = Column(String(100))
    provider = Column(String(100))
    amount = Column(Float)
    eligibility_status = Column(String(20))
    application_status = Column(String(20))

    # Relationships
    student = relationship('Student', back_populates='scholarship_records')

    def to_dict(self):
        return {
            'scholarship_id': self.scholarship_id,
            'student_id': self.student_id,
            'scholarship_name': self.scholarship_name,
            'provider': self.provider,
            'amount': self.amount,
            'eligibility_status': self.eligibility_status,
            'application_status': self.application_status
        }


class Internship(Base):
    __tablename__ = 'internships'

    internship_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(100))
    domain = Column(String(100))
    role = Column(String(100))
    location = Column(String(100))
    duration = Column(String(50))
    stipend = Column(Float)
    eligibility = Column(String(200))
    deadline = Column(String(20))

    def to_dict(self):
        return {
            'internship_id': self.internship_id,
            'company_name': self.company_name,
            'domain': self.domain,
            'role': self.role,
            'location': self.location,
            'duration': self.duration,
            'stipend': self.stipend,
            'eligibility': self.eligibility,
            'deadline': self.deadline
        }


class Document(Base):
    __tablename__ = 'documents'

    document_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    category = Column(String(50))
    file_path = Column(String(300))
    content = Column(Text)
    uploaded_date = Column(String(20))

    def to_dict(self):
        return {
            'document_id': self.document_id,
            'title': self.title,
            'category': self.category,
            'file_path': self.file_path,
            'content': self.content,
            'uploaded_date': self.uploaded_date
        }


class Faculty(Base):
    __tablename__ = 'faculty'

    faculty_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    role = Column(String(50))
    password = Column(String(100))

    # Relationships
    department = relationship('Department', back_populates='faculty_members')

    def to_dict(self):
        return {
            'faculty_id': self.faculty_id,
            'name': self.name,
            'email': self.email,
            'department_id': self.department_id,
            'role': self.role
        }

"""Seeding script to populate initial data."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import get_db_context, init_database
from datetime import datetime


def seed_default_hospital():
    """Seed default hospital data."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        # Check if hospital already exists
        cursor.execute("SELECT COUNT(*) FROM hospitals WHERE code='DEMO'")
        if cursor.fetchone()[0] > 0:
            print("✓ Default hospital already exists")
            return
        
        sql = """
        INSERT INTO hospitals (name, code, email, phone, address, city, state, postal_code, country, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            'Demo Hospital',
            'DEMO',
            'contact@demohospital.com',
            '9876543210',
            '123 Hospital Lane',
            'New Delhi',
            'Delhi',
            '110001',
            'India',
            True
        ))
        
        db.commit()
        print("✓ Default hospital created")


def seed_default_super_admin():
    """Seed default super admin user."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
        if cursor.fetchone()[0] > 0:
            print("✓ Default admin user already exists")
            return
        
        # Hash password
        from utils.security import hash_password
        password_hash = hash_password('admin@123')
        
        sql = """
        INSERT INTO users (username, email, first_name, last_name, role, password_hash, is_verified, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            'admin',
            'admin@hospital.com',
            'System',
            'Administrator',
            'super_admin',
            password_hash,
            True,
            True
        ))
        
        db.commit()
        print("✓ Default super admin user created (username: admin, password: admin@123)")


def seed_departments():
    """Seed default departments."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        departments = [
            ('CARD', 'Cardiology', 'Heart and Cardiovascular diseases'),
            ('ORTHO', 'Orthopedics', 'Bones and joint disorders'),
            ('ENT', 'ENT', 'Ear, Nose and Throat'),
            ('NEURO', 'Neurology', 'Brain and nervous system'),
            ('PEDS', 'Pediatrics', 'Children healthcare'),
            ('OBGYN', 'Obstetrics & Gynecology', 'Women and maternal health'),
        ]
        
        # Get demo hospital ID
        cursor.execute("SELECT id FROM hospitals WHERE code='DEMO'")
        hospital_result = cursor.fetchone()
        if not hospital_result:
            print("✗ Demo hospital not found")
            return
        
        hospital_id = hospital_result[0]
        
        for code, name, description in departments:
            cursor.execute(
                "SELECT COUNT(*) FROM departments WHERE hospital_id=%s AND code=%s",
                (hospital_id, code)
            )
            if cursor.fetchone()[0] == 0:
                sql = """
                INSERT INTO departments (hospital_id, code, name, description, is_active)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (hospital_id, code, name, description, True))
        
        db.commit()
        print("✓ Default departments seeded")


def seed_panels():
    """Seed default insurance panels."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        panels = [
            ('SELF', 'Self/Cash Patient', 'cash'),
            ('AROGYA', 'Arogya Insurance', 'insurance'),
            ('APOLLO', 'Apollo Insurance', 'insurance'),
            ('CORPORATE', 'Corporate Panel', 'corporate'),
        ]
        
        # Get demo hospital ID
        cursor.execute("SELECT id FROM hospitals WHERE code='DEMO'")
        hospital_result = cursor.fetchone()
        if not hospital_result:
            print("✗ Demo hospital not found")
            return
        
        hospital_id = hospital_result[0]
        
        for code, name, panel_type in panels:
            cursor.execute(
                "SELECT COUNT(*) FROM panels WHERE hospital_id=%s AND code=%s",
                (hospital_id, code)
            )
            if cursor.fetchone()[0] == 0:
                sql = """
                INSERT INTO panels (hospital_id, code, name, panel_type, is_active)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (hospital_id, code, name, panel_type, True))
        
        db.commit()
        print("✓ Default insurance panels seeded")


def seed_services():
    """Seed default services."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        services = [
            ('CONS', 'Consultation', 'Medical consultation'),
            ('ECG', 'ECG', 'Electrocardiography'),
            ('ECHO', 'Echocardiography', 'Heart ultrasound'),
            ('CT', 'CT Scan', 'Computed Tomography'),
            ('MRI', 'MRI Scan', 'Magnetic Resonance Imaging'),
            ('LABS', 'Laboratory Tests', 'Blood and pathology tests'),
            ('XRAY', 'X-Ray', 'X-Ray imaging'),
            ('SURGERY', 'Surgery', 'Surgical procedures'),
        ]
        
        # Get demo hospital ID
        cursor.execute("SELECT id FROM hospitals WHERE code='DEMO'")
        hospital_result = cursor.fetchone()
        if not hospital_result:
            print("✗ Demo hospital not found")
            return
        
        hospital_id = hospital_result[0]
        
        for code, name, description in services:
            cursor.execute(
                "SELECT COUNT(*) FROM services WHERE hospital_id=%s AND code=%s",
                (hospital_id, code)
            )
            if cursor.fetchone()[0] == 0:
                sql = """
                INSERT INTO services (hospital_id, code, name, description, is_active)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (hospital_id, code, name, description, True))
        
        db.commit()
        print("✓ Default services seeded")


def seed_service_rates():
    """Seed default service rates for panels."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        # Get demo hospital ID
        cursor.execute("SELECT id FROM hospitals WHERE code='DEMO'")
        hospital_result = cursor.fetchone()
        if not hospital_result:
            print("✗ Demo hospital not found")
            return
        
        hospital_id = hospital_result[0]
        
        # Get all services and panels
        cursor.execute("SELECT id, code FROM services WHERE hospital_id=%s", (hospital_id,))
        services = cursor.fetchall()
        
        cursor.execute("SELECT id, code FROM panels WHERE hospital_id=%s", (hospital_id,))
        panels = cursor.fetchall()
        
        # Define rates for different panels
        rates = {
            'CONS': {'SELF': 500, 'AROGYA': 400, 'APOLLO': 450, 'CORPORATE': 350},
            'ECG': {'SELF': 300, 'AROGYA': 250, 'APOLLO': 280, 'CORPORATE': 200},
            'ECHO': {'SELF': 2000, 'AROGYA': 1800, 'APOLLO': 1900, 'CORPORATE': 1500},
            'CT': {'SELF': 5000, 'AROGYA': 4500, 'APOLLO': 4800, 'CORPORATE': 4000},
            'MRI': {'SELF': 8000, 'AROGYA': 7000, 'APOLLO': 7500, 'CORPORATE': 6000},
            'LABS': {'SELF': 500, 'AROGYA': 400, 'APOLLO': 450, 'CORPORATE': 300},
            'XRAY': {'SELF': 300, 'AROGYA': 250, 'APOLLO': 280, 'CORPORATE': 200},
            'SURGERY': {'SELF': 15000, 'AROGYA': 13000, 'APOLLO': 14000, 'CORPORATE': 12000},
        }
        
        for service_id, service_code in services:
            for panel_id, panel_code in panels:
                cursor.execute(
                    "SELECT COUNT(*) FROM service_rates WHERE service_id=%s AND panel_id=%s",
                    (service_id, panel_id)
                )
                if cursor.fetchone()[0] == 0:
                    rate = rates.get(service_code, {}).get(panel_code, 1000)
                    sql = """
                    INSERT INTO service_rates (hospital_id, service_id, panel_id, rate, is_active)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (hospital_id, service_id, panel_id, rate, True))
        
        db.commit()
        print("✓ Service rates seeded")


def run_all_seeds():
    """Run all seeding scripts."""
    print("\n" + "="*60)
    print("Starting Database Seeding")
    print("="*60 + "\n")
    
    try:
        # Initialize database first
        print("Initializing database connection...")
        init_database()
        print("✓ Database connection initialized\n")
        
        # Run seeds
        seed_default_hospital()
        seed_default_super_admin()
        seed_departments()
        seed_panels()
        seed_services()
        seed_service_rates()
        
        print("\n" + "="*60)
        print("✓ All seeding completed successfully!")
        print("="*60)
        print("\nDefault Login Credentials:")
        print("  Username: admin")
        print("  Password: admin@123")
        print("\n")
        
    except Exception as e:
        print(f"\n✗ Seeding failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_all_seeds()

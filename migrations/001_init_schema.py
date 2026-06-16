"""Database migration scripts for Hospital Information System."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import get_db_context, init_database
from config.settings import AppSettings


def migration_001_create_users_table():
    """Migration: Create users table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20),
            role VARCHAR(50) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_verified BOOLEAN DEFAULT FALSE,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE SET NULL
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 001: Users table created")


def migration_002_create_hospitals_table():
    """Migration: Create hospitals table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS hospitals (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            code VARCHAR(50) UNIQUE NOT NULL,
            license_number VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            website VARCHAR(150),
            address TEXT,
            city VARCHAR(100),
            state VARCHAR(100),
            postal_code VARCHAR(10),
            country VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 002: Hospitals table created")


def migration_003_create_patients_table():
    """Migration: Create patients table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            uhid VARCHAR(50) UNIQUE NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50),
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE,
            gender VARCHAR(10),
            blood_group VARCHAR(5),
            mobile_primary VARCHAR(20),
            mobile_secondary VARCHAR(20),
            email VARCHAR(100),
            aadhar_number VARCHAR(20),
            abha_id VARCHAR(100),
            address TEXT,
            city VARCHAR(100),
            state VARCHAR(100),
            postal_code VARCHAR(10),
            country VARCHAR(100) DEFAULT 'India',
            occupation VARCHAR(100),
            marital_status VARCHAR(20),
            emergency_contact_name VARCHAR(100),
            emergency_contact_phone VARCHAR(20),
            emergency_contact_relation VARCHAR(50),
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            INDEX idx_hospital_uhid (hospital_id, uhid),
            INDEX idx_hospital_phone (hospital_id, mobile_primary)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 003: Patients table created")


def migration_004_create_departments_table():
    """Migration: Create departments table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            code VARCHAR(50) NOT NULL,
            name VARCHAR(150) NOT NULL,
            description TEXT,
            head_name VARCHAR(100),
            head_phone VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            UNIQUE KEY unique_hospital_code (hospital_id, code)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 004: Departments table created")


def migration_005_create_consultants_table():
    """Migration: Create consultants table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS consultants (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            registration_number VARCHAR(50) NOT NULL,
            specialization VARCHAR(100),
            qualification VARCHAR(200),
            experience_years INT,
            availability_status VARCHAR(20) DEFAULT 'available',
            consultation_fee DECIMAL(10, 2),
            phone VARCHAR(20),
            office_address TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_hospital_reg (hospital_id, registration_number)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 005: Consultants table created")


def migration_006_create_services_table():
    """Migration: Create services table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS services (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            code VARCHAR(50) NOT NULL,
            name VARCHAR(150) NOT NULL,
            description TEXT,
            category VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            UNIQUE KEY unique_hospital_code (hospital_id, code)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 006: Services table created")


def migration_007_create_service_rates_table():
    """Migration: Create service rates (panel-wise) table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS service_rates (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            panel_id INTEGER NOT NULL,
            rate DECIMAL(10, 2) NOT NULL,
            discount_percentage DECIMAL(5, 2) DEFAULT 0,
            effective_from DATE,
            effective_to DATE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
            FOREIGN KEY (panel_id) REFERENCES panels(id) ON DELETE CASCADE,
            UNIQUE KEY unique_service_panel (service_id, panel_id),
            INDEX idx_hospital_panel (hospital_id, panel_id)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 007: Service rates table created")


def migration_008_create_panels_table():
    """Migration: Create insurance/company panels table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS panels (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            code VARCHAR(50) NOT NULL,
            name VARCHAR(150) NOT NULL,
            panel_type VARCHAR(50),
            contact_person VARCHAR(100),
            contact_phone VARCHAR(20),
            contact_email VARCHAR(100),
            commission_percentage DECIMAL(5, 2),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            UNIQUE KEY unique_hospital_code (hospital_id, code)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 008: Panels table created")


def migration_009_create_billings_table():
    """Migration: Create billings table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS billings (
            id SERIAL PRIMARY KEY,
            hospital_id INTEGER NOT NULL,
            bill_number VARCHAR(50) NOT NULL,
            patient_id INTEGER NOT NULL,
            bill_type VARCHAR(20) NOT NULL,
            billing_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(12, 2),
            discount_amount DECIMAL(12, 2) DEFAULT 0,
            tax_amount DECIMAL(12, 2) DEFAULT 0,
            net_amount DECIMAL(12, 2),
            paid_amount DECIMAL(12, 2) DEFAULT 0,
            payment_status VARCHAR(20) DEFAULT 'pending',
            payment_method VARCHAR(50),
            billing_notes TEXT,
            status VARCHAR(20) DEFAULT 'active',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users(id),
            UNIQUE KEY unique_hospital_bill (hospital_id, bill_number),
            INDEX idx_patient_date (patient_id, billing_date),
            INDEX idx_status (payment_status)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 009: Billings table created")


def migration_010_create_billing_items_table():
    """Migration: Create billing items table."""
    with get_db_context() as db:
        cursor = db.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS billing_items (
            id SERIAL PRIMARY KEY,
            billing_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            quantity DECIMAL(10, 2) DEFAULT 1,
            unit_price DECIMAL(10, 2) NOT NULL,
            discount_percentage DECIMAL(5, 2) DEFAULT 0,
            discount_amount DECIMAL(10, 2) DEFAULT 0,
            amount DECIMAL(12, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (billing_id) REFERENCES billings(id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES services(id),
            INDEX idx_billing (billing_id)
        )
        """
        
        cursor.execute(sql)
        db.commit()
        print("✓ Migration 010: Billing items table created")


def run_all_migrations():
    """Run all database migrations."""
    print("\n" + "="*60)
    print("Starting Database Migrations")
    print("="*60 + "\n")
    
    try:
        # Initialize database first
        print("Initializing database connection...")
        init_database()
        print("✓ Database connection initialized\n")
        
        # Run migrations
        migration_002_create_hospitals_table()
        migration_001_create_users_table()
        migration_003_create_patients_table()
        migration_004_create_departments_table()
        migration_005_create_consultants_table()
        migration_006_create_services_table()
        migration_008_create_panels_table()
        migration_007_create_service_rates_table()
        migration_009_create_billings_table()
        migration_010_create_billing_items_table()
        
        print("\n" + "="*60)
        print("✓ All migrations completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_all_migrations()

# Hospital Information System (HIS)

A comprehensive, production-ready hospital management software system built with Python, Streamlit, and PostgreSQL.

## Overview

This system is designed to streamline hospital operations with modules for:
- Inpatient Department (IPD) Management
- Outpatient Department (OPD) Management
- Cash and Credit Billing
- Panel-wise Billing (Insurance/Company Panels)
- Master Data Management
- UHID & ABHA ID Management
- Advanced Reporting & Printing
- Multi-Hospital Support
- Role-Based Access Control

## Key Features

### 1. Department Management
- Inpatient and Outpatient workflows
- Patient admission, discharge, and transfers
- Department-wise resource allocation

### 2. Billing System
- Cash and credit billing workflows
- Panel-wise billing with insurance/company rates
- Service code and rate management
- Billing reconciliation and reports

### 3. Master Data Management
- Departments, Services, Sub-Services
- Consultants and Staff
- Patients with UHID
- Panels and Insurance
- Floors, Rooms, and Beds
- Service Packages

### 4. Patient Management
- UHID Generation and Management
- ABHA ID Integration
- Patient Demographics and History
- Patient-Panel Linking

### 5. Reporting & Printing
- Customizable report designer (no-code)
- Print template customization
- Ad-hoc reporting
- Scheduled reports

### 6. Configuration Management
- Front-end database management (multi-hospital)
- Screen and field customization
- Workflow configuration
- User roles and permissions

### 7. Multi-Hospital Support
- Super user management for multiple hospitals
- Hospital-wise data isolation
- Centralized admin controls

## Technology Stack

- **Backend**: Python with Streamlit
- **Database**: PostgreSQL
- **Frontend**: Streamlit UI
- **ORM**: SQLAlchemy
- **Authentication**: Role-based access control (RBAC)

## Project Structure

```
HIS/
├── app.py                          # Main Streamlit application
├── config/
│   ├── database.py                 # Database configuration
│   ├── settings.py                 # Application settings
│   └── constants.py                # Application constants
├── modules/
│   ├── ipd/                        # Inpatient Department
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   ├── opd/                        # Outpatient Department
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   ├── billing/                    # Billing Module
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   ├── masters/                    # Master Data Management
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   ├── patient/                    # Patient Management
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   ├── reports/                    # Reporting Module
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   ├── users/                      # User Management
│   │   ├── models.py
│   │   ├── controllers.py
│   │   └── views.py
│   └── settings/                   # Configuration Management
│       ├── models.py
│       ├── controllers.py
│       └── views.py
├── utils/
│   ├── database.py                 # Database utilities
│   ├── auth.py                     # Authentication utilities
│   ├── validators.py               # Data validators
│   ├── generators.py               # ID generators (UHID, ABHA)
│   └── helpers.py                  # Helper functions
├── migrations/                     # Database migrations
├── tests/                          # Unit and integration tests
├── docs/                           # Documentation
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── setup.sh                        # Installation script
```

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArunPrasad82/HIS.git
   cd HIS
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run database migrations:**
   ```bash
   python -m alembic upgrade head
   ```

6. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

### Super User Setup
1. Login with default super user credentials
2. Create hospital(s)
3. Configure database for each hospital
4. Create admin users for each hospital

### Admin Setup
1. Login to assigned hospital
2. Configure master data
3. Set up billing panels and rates
4. Configure user roles and permissions
5. Design custom reports

### End Users
- Use IPD/OPD modules for patient management
- Process billing as per configured rules
- Generate custom reports
- Access patient records via UHID

## Documentation

Detailed documentation is available in the `/docs` directory:
- **Installation Guide**: Setup and deployment instructions
- **User Manual**: How to use the system
- **Administrator Guide**: Configuration and management
- **Consultant Guide**: Customization without coding
- **Technical Guide**: Architecture and development

## Security

- Role-based access control (RBAC)
- Password encryption
- Session management
- Audit logging
- Data encryption at rest

## Support

For issues, questions, or feature requests, please create an issue in the GitHub repository.

## License

Proprietary - Hospital Information System

## Version

v1.0.0 - Initial Release

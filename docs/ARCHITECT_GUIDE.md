# System Architecture Guide

## Project Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────┐
│   Streamlit UI Layer                │
│  (Views, Components, Navigation)    │
├─────────────────────────────────────┤
│   Business Logic Layer              │
│  (Controllers, Services)            │
├─────────────────────────────────────┤
│   Data Access Layer                 │
│  (Models, ORM, Repositories)        │
├─────────────────────────────────────┤
│   Database Layer                    │
│  (PostgreSQL)                       │
└─────────────────────────────────────┘
```

## Module Structure

Each module follows this pattern:

```
module_name/
├── models.py          # SQLAlchemy models
├── controllers.py     # Business logic
├── views.py           # Streamlit UI
├── validators.py      # Data validation
└── schemas.py         # Pydantic schemas
```

## Key Components

### 1. Database Layer
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Connection Pooling**: SQLAlchemy engine

### 2. Business Logic
- Controllers handle business operations
- Services for cross-module operations
- Validators for data integrity

### 3. UI Layer
- Streamlit components
- Session state management
- Form handling and validation

### 4. Authentication
- Role-based access control (RBAC)
- JWT tokens for sessions
- Password hashing with bcrypt

## Data Flow

```
User Input (Streamlit UI)
        ↓
  Validation Layer
        ↓
  Controller/Service
        ↓
  Repository Pattern
        ↓
  SQLAlchemy ORM
        ↓
  PostgreSQL Database
```

## Security Implementation

1. **Authentication**
   - Username/password login
   - JWT token-based sessions
   - Bcrypt password hashing

2. **Authorization**
   - Role-based permissions
   - Resource-level access control
   - Hospital-wise data isolation

3. **Data Protection**
   - SQL injection prevention (ORM)
   - XSS protection (Streamlit)
   - CSRF tokens for forms

## Database Design Principles

1. **Normalization**: 3NF applied
2. **Relationships**: Proper foreign keys
3. **Indexes**: On frequently queried columns
4. **Audit Trail**: Created_at, updated_at on all tables
5. **Soft Deletes**: Where applicable

## API Design

Controller methods follow this pattern:

```python
def create_resource(self, data: dict) -> dict:
    # Validate input
    # Create database object
    # Return result with status
    pass

def read_resource(self, resource_id: int) -> dict:
    # Fetch from database
    # Check permissions
    # Return result
    pass

def update_resource(self, resource_id: int, data: dict) -> dict:
    # Validate input
    # Update database
    # Return result
    pass

def delete_resource(self, resource_id: int) -> dict:
    # Check if can delete
    # Soft delete or hard delete
    # Return result
    pass
```

## Error Handling

- Custom exception classes for different errors
- Consistent error response format
- Logging of all errors
- User-friendly error messages

## Performance Considerations

1. **Database Queries**
   - Use eager loading for related data
   - Pagination for large datasets
   - Caching where applicable

2. **UI Rendering**
   - Use Streamlit caching (@st.cache_data)
   - Lazy loading of components
   - Minimize re-renders

3. **Scalability**
   - Connection pooling
   - Query optimization
   - Proper indexing strategy

## Testing Strategy

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test module interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Load and stress testing

## Deployment

1. **Development**: Local machine with SQLite/PostgreSQL
2. **Staging**: Separate environment for testing
3. **Production**: Load-balanced with persistent database

## Monitoring & Logging

- Structured logging with JSON format
- Error tracking and alerting
- Performance monitoring
- Audit logging for compliance

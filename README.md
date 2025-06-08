# Bank Card Management System API

A secure REST API for managing bank cards with authentication, role-based access, and financial operations.

## Main Features

### Security
- JWT Authentication
- Role-based access control (`ADMIN` and `USER`)
- Card data encryption
- Masked card numbers (`**** **** **** 1234`)

### Card Operations
- Card/User CRUD operations (ADMIN only)
- View personal cards (USER)
- Transfers between own cards
- Filtering and pagination

### Tech Stack
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL
- **Documentation**: Swagger UI

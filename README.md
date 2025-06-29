# Bank Card Management System API

A secure REST API for managing bank cards with authentication, role-based access, and financial operations.

## Main Features

### Security
- JWT Authentication
- Role-based access control (`ADMIN` and `USER`)
- Auto creating superuser:
  - username - `admin`
  - password - `qwerty`
- Card data encryption
- Masked card numbers (`**** **** **** 1234`)

### Card Operations
- Card/User CRUD operations (`ADMIN` only)
- View personal cards (`USER`)
- Transfers between own cards
- Filtering and pagination

### Tech Stack
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL
- **Documentation**: Swagger UI
- **Deploy**: Docker

### Smooth Start
1. Clone Repository:
   ```bash
   git clone https://github.com/stashevskii/card-manager-api.git
   cd card-manager-api
2. Create `.env` file similar to `.env.template`
3. Run Application
   ```bash
   docker compose up -d
After running go to http://localhost:8000

# 💰 FinanceTrack — Personal Expense Tracker API with FastAPI

**FinanceTrack** is a secure, lightweight REST API built with FastAPI that allows users to register, log in, and manage their personal finances. Track expenses by categories, update them, and get clear structured data for budgeting — all with JWT-based authentication.

---

## ⚙️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Authentication**: OAuth2 with JWT
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy + Alembic for migrations
- **Schemas**: Pydantic
- **Docs**: Swagger UI (`/docs`)
- **Extras**: Uvicorn, dotenv, CORS

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Evgen-Jekov/financial-tracker
cd finance-track
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file:
```ini
DB=postgresql://user:password@localhost/db_name
JWT=your_secret_key
```

### 5. Run migrations
```bash
alembic upgrade head
```

### 6. Launch the app
```bash
uvicorn main:app --reload
```

---

## 🔐 Authentication

All protected endpoints use **OAuth2** with **JWT** tokens.

- To obtain a token: `POST /user/login`
- Use the token in headers:  
  `Authorization: Bearer <your_token_here>`

---

## 🧩 API Endpoints

### 🧑 User
- `POST /user/register` — Create a new user
- `POST /user/login` — Login and receive access token
- `GET /user/get-user/{id}` — Get authenticated user's profile

### 💵 Finance
- `POST /finance/add-finance` — Add a new expense
- `GET /finance/get-all-finance` — Retrieve all user's expenses
- `POST /finance/get-category-finance` — Filter expenses by category
- `PUT /finance/update-finance-all/{id}` — Fully update an expense
- `PATCH /finance/update-finance-optional` — Partially update an expense
- `DELETE /finance/delete-finance/{id}` — Delete an expense

---

## 📦 Example Request

```bash
curl -X POST http://localhost:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "Str0ngP@ssword!"
}'
```

---

## 📊 Features

- Secure user authentication with hashed passwords
- JWT token system with access expiry
- Categorized expense tracking
- Fully documented via Swagger UI
- Clean modular architecture with routers, services, and schemas

---

## 💡 Future Enhancements

- Data visualization with charts (D3.js, Chart.js)
- Daily/weekly financial reports via email
- Limit alerts and budget goals
- Mobile-friendly frontend with React Native or Flutter

---

## 👨‍💻 Author

Crafted with ❤️ by **Evgen Jekov**  
Feel free to connect: [GitHub](https://github.com/Evgen-Jekov) · [LinkedIn](#) · [Telegram](#)

---

## 📄 License

This project is licensed under the MIT License.

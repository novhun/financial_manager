from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, incomes, expenses, budgets, projects, tasks, groups, analytics, types
from app.setup_db import setup_database

# Initialize the FastAPI app
app = FastAPI(
    title="Finance App API",
    description="A FastAPI-based personal finance management system with multi-user support, income/expense tracking, budgeting, project management, and group sharing.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(incomes.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(groups.router)
app.include_router(analytics.router)
app.include_router(types.router)

@app.get("/", summary="Root endpoint", description="Welcome message for the Finance App API.")
def read_root():
    return {"message": "Welcome to Finance App"}

# Defer database setup to runtime
if __name__ == "__main__":
    setup_database()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
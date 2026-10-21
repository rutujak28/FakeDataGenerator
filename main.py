
import csv
import io
import json
import random
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, StreamingResponse
from faker import Faker

app = FastAPI(
    title="Fake Data Generator API",
    description="Generate fictional datasets for testing and development.",
    version="2.0.0"
)

fake = Faker()
BASE_DIR = Path(__file__).resolve().parent


PRODUCTS = {
    "Electronics": [
        "Wireless Headphones",
        "Bluetooth Speaker",
        "Mechanical Keyboard",
        "Wireless Mouse",
        "USB-C Charger",
        "Smart Watch",
        "Portable Power Bank",
    ],
    "Home & Kitchen": [
        "Ceramic Coffee Mug",
        "Wooden Desk Organizer",
        "Stainless Steel Bottle",
        "LED Desk Lamp",
        "Storage Basket",
    ],
    "Fashion": [
        "Cotton T-Shirt",
        "Travel Backpack",
        "Running Shoes",
        "Leather Wallet",
        "Canvas Tote Bag",
    ],
    "Books & Stationery": [
        "Notebook Set",
        "Hardcover Journal",
        "Ballpoint Pen Set",
        "Desk Planner",
    ],
}


def create_users(count: int):
    return [
        {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.safe_email(),
            "city": fake.city(),
        }
        for i in range(count)
    ]


def create_products(count: int):
    products = []

    for i in range(count):
        category = random.choice(list(PRODUCTS.keys()))

        products.append({
            "id": i + 1,
            "name": random.choice(PRODUCTS[category]),
            "price": round(fake.pyfloat(min_value=10, max_value=1000), 2),
            "category": category,
        })

    return products


def create_students(count: int):
    return [
        {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.safe_email(),
            "course": random.choice([
                "Information Technology",
                "Computer Engineering",
                "Data Science",
                "Artificial Intelligence",
            ]),
            "year": random.randint(1, 4),
            "city": fake.city(),
        }
        for i in range(count)
    ]


def create_employees(count: int):
    return [
        {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.safe_email(),
            "department": random.choice([
                "Engineering",
                "Human Resources",
                "Finance",
                "Marketing",
                "Sales",
            ]),
            "job_title": random.choice([
                "Software Engineer",
                "Data Analyst",
                "Project Manager",
                "QA Engineer",
                "Business Analyst",
            ]),
            "city": fake.city(),
        }
        for i in range(count)
    ]


def create_csv(records):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
    output.seek(0)
    return output


def csv_response(records, filename: str):
    output = create_csv(records)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        },
    )


def json_response(records, filename: str):
    content = json.dumps(records, indent=2)

    return StreamingResponse(
        iter([content]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        },
    )


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/users")
def generate_users(count: int = Query(default=5, ge=1, le=100)):
    users = create_users(count)
    return {"count": len(users), "users": users}


@app.get("/products")
def generate_products(count: int = Query(default=5, ge=1, le=100)):
    products = create_products(count)
    return {"count": len(products), "products": products}


@app.get("/students")
def generate_students(count: int = Query(default=5, ge=1, le=100)):
    students = create_students(count)
    return {"count": len(students), "students": students}


@app.get("/employees")
def generate_employees(count: int = Query(default=5, ge=1, le=100)):
    employees = create_employees(count)
    return {"count": len(employees), "employees": employees}


@app.get("/users/csv")
def download_users_csv(count: int = Query(default=5, ge=1, le=100)):
    return csv_response(create_users(count), "users.csv")


@app.get("/products/csv")
def download_products_csv(count: int = Query(default=5, ge=1, le=100)):
    return csv_response(create_products(count), "products.csv")


@app.get("/students/csv")
def download_students_csv(count: int = Query(default=5, ge=1, le=100)):
    return csv_response(create_students(count), "students.csv")


@app.get("/employees/csv")
def download_employees_csv(count: int = Query(default=5, ge=1, le=100)):
    return csv_response(create_employees(count), "employees.csv")


@app.get("/users/json")
def download_users_json(count: int = Query(default=5, ge=1, le=100)):
    return json_response(create_users(count), "users.json")


@app.get("/products/json")
def download_products_json(count: int = Query(default=5, ge=1, le=100)):
    return json_response(create_products(count), "products.json")


@app.get("/students/json")
def download_students_json(count: int = Query(default=5, ge=1, le=100)):
    return json_response(create_students(count), "students.json")


@app.get("/employees/json")
def download_employees_json(count: int = Query(default=5, ge=1, le=100)):
    return json_response(create_employees(count), "employees.json")

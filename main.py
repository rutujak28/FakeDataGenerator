import csv
import io
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, StreamingResponse
from faker import Faker

app = FastAPI(
    title="Fake Data Generator API",
    description="Generate fictional data for testing and development.",
    version="1.1.0"
)

fake = Faker()

BASE_DIR = Path(__file__).resolve().parent


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


def create_users(count: int):
    users = []

    for i in range(count):
        users.append({
            "id": i + 1,
            "name": fake.name(),
            "email": fake.safe_email(),
            "city": fake.city()
        })

    return users


def create_products(count: int):
    products = []

    for i in range(count):
        products.append({
            "id": i + 1,
            "name": fake.word().title(),
            "price": round(fake.pyfloat(min_value=10, max_value=1000), 2),
            "category": fake.word().title()
        })

    return products


def create_csv(records):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

    output.seek(0)
    return output


@app.get("/users")
def generate_users(count: int = Query(default=5, ge=1, le=100)):
    users = create_users(count)
    return {"count": len(users), "users": users}


@app.get("/products")
def generate_products(count: int = Query(default=5, ge=1, le=100)):
    products = create_products(count)
    return {"count": len(products), "products": products}


@app.get("/users/csv")
def download_users_csv(count: int = Query(default=5, ge=1, le=100)):
    users = create_users(count)
    output = create_csv(users)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=users.csv"
        }
    )


@app.get("/products/csv")
def download_products_csv(count: int = Query(default=5, ge=1, le=100)):
    products = create_products(count)
    output = create_csv(products)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=products.csv"
        }
    )

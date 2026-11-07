from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from models import ProductDB, ProductData
from scraper import scrape_product
from sqlmodel import Session, SQLModel, create_engine, select

# Setup SQLite database connection
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def create_db_and_tables():
  SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
  # Create database tables on startup
  create_db_and_tables()
  yield


app = FastAPI(
    title="AI Data Extraction Pipeline", lifespan=lifespan
)


@app.post("/scrape", response_model=ProductDB)
def scrape_and_save(url: str):
  try:
    extracted_data: ProductData = scrape_product(url)

  
    db_product = ProductDB(
        name=extracted_data.name,
        price=extracted_data.price,
        in_stock=extracted_data.in_stock,
        rating=extracted_data.rating,
        summary=extracted_data.summary,
    )

    with Session(engine) as session:
      session.add(db_product)
      session.commit()
      session.refresh(db_product)
      return db_product

  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


@app.get("/products", response_model=List[ProductDB])
def get_products():
  # Retrieve all saved products from SQLite
  with Session(engine) as session:
    products = session.exec(select(ProductDB)).all()
    return products
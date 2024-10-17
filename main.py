from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth
from auth import get_current_user


app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

class MerchantBase(BaseModel):
    username: str
    password: str

class ProductBase(BaseModel):
    namabarang: str
    hargabarang: int

class SalesBase(BaseModel):
    idbarang: int
    hargabarang: int
    jumlah: int
    pembeli: str
    subtotal: int
    namabarang: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.post("/belanja/")
async def sales(belanja: SalesBase, db:db_dependency):
    harga_beli = db.query(models.Product.hargabarang,models.Product.namabarang).filter(models.Product.id == belanja.idbarang).first()
    if harga_beli is None:
        raise HTTPException(status_code=404, detail=f"produk dengan id = {belanja.id} tidak ada !")
    subs = harga_beli[0]*belanja.jumlah
    belanja = belanja.copy(update={'hargabarang': harga_beli[0] , 'subtotal': subs, 'namabarang' : harga_beli[1]})
    db_sales = models.Sales(**belanja.dict())
    db.add(db_sales)
    db.commit()
    diskon = 0
    ongkir = "ADA BIAYA ONGKIR"
    if subs > 50000:
        diskon = 0.1 * subs
    if subs > 15000:
        ongkir ="GRATIS ONGKIR"
    payload = {"message": "Belanja berhasil","diskon" : diskon, "Ongkir" : ongkir}
    return JSONResponse(content=payload)

@app.get("/merchant/sales/", status_code=status.HTTP_200_OK)
async def tampil_prod(username: user_dependency, db: db_dependency):
    if username is None:
        raise HTTPException(status_code=401, detail='Khusus Merchant')
    all_prod = db.query(models.Sales).all()
    return all_prod


@app.delete("/merchant/{prod_id}", status_code=status.HTTP_200_OK)
async def hapus_prod(username: user_dependency, prod_id: int, db: db_dependency):
    if username is None:
        raise HTTPException(status_code=401, detail='Khusus Merchant')
    db_prod = db.query(models.Product).filter(models.Product.id == prod_id).first()
    if db_prod is None:
        raise HTTPException(status_code=404, detail='produk tidak ada ')
    db.query(models.Product).filter(models.Product.id == prod_id).delete()
    db.commit()

@app.get("/produk/", status_code=status.HTTP_200_OK)
async def tampil_prod(db: db_dependency):
    all_prod = db.query(models.Product).all()
    return all_prod


@app.post("/merchant/buatproduk/", status_code=status.HTTP_201_CREATED)
async def buat_produk(username: user_dependency, produk: ProductBase, db: db_dependency):
    if username is None:
        raise HTTPException(status_code=401, detail='Khusus Merchant')
    buatproduk=models.Product(**produk.dict())
    db.add(buatproduk)
    db.commit()


@app.get("/",status_code=status.HTTP_200_OK)
def cek_web():
    return JSONResponse(content={"status":"WEB OK"})

 

    
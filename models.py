from sqlalchemy import Column, Integer, String, Boolean, Unicode
from database import Base

class Merchant(Base):
    __tablename__ = 'penjual'
    idm = Column(Integer, primary_key=True, index=True) 
    usermerchant = Column(String(30))
    password = Column(String(100))

class Product(Base):
    __tablename__ = 'produk'
    id = Column(Integer, primary_key=True, index=True) 
    namabarang = Column(String(20))
    hargabarang = Column(Integer)


class Sales(Base):
    __tablename__ = 'penjualan'
    id = Column(Integer, primary_key=True, index=True) 
    idbarang = Column(Integer)
    pembeli = Column(String(20))
    namabarang = Column(String(20))
    hargabarang = Column(Integer)
    jumlah = Column(Integer)
    subtotal = Column(Integer)


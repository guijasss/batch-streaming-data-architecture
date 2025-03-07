from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
    order_purchase_timestamp = Column(DateTime, nullable=False)
    order_approved_at = Column(DateTime)
    order_delivered_carrier_date = Column(DateTime)
    order_delivered_customer_date = Column(DateTime)
    order_estimated_delivery_date = Column(DateTime)
    
    reviews = relationship("Review", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    items = relationship("Item", back_populates="order")

class Review(Base):
    __tablename__ = "reviews"
    
    review_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.order_id"), nullable=False)
    review_score = Column(Integer, nullable=False)
    review_comment_title = Column(String)
    review_comment_message = Column(String)
    review_creation_date = Column(DateTime, nullable=False)
    review_answer_timestamp = Column(DateTime, nullable=False)
    
    order = relationship("Order", back_populates="reviews")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.order_id"), nullable=False)
    payment_sequential = Column(Integer, nullable=False)
    payment_type = Column(String, nullable=False)
    payment_installments = Column(Integer, nullable=False)
    payment_value = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="payments")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.order_id"), nullable=False)
    order_item_id = Column(Integer, nullable=False)
    product_id = Column(String, nullable=False)
    seller_id = Column(String, nullable=False)
    shipping_limit_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    freight_value = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")

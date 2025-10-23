import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///talentlink.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

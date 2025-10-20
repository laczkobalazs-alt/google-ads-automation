"""
Alkalmazás konfigurációs beállítások
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Alkalmazás beállítások környezeti változókból"""
    
    # API Configuration
    API_TITLE: str = "Google Ads Automation API"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Google Ads API Configuration
    GOOGLE_ADS_DEVELOPER_TOKEN: str = ""
    GOOGLE_ADS_CLIENT_ID: str = ""
    GOOGLE_ADS_CLIENT_SECRET: str = ""
    GOOGLE_ADS_REFRESH_TOKEN: str = ""
    GOOGLE_ADS_LOGIN_CUSTOMER_ID: str = ""
    GOOGLE_ADS_CONFIG_FILE: str = "google-ads.yaml"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./google_ads_automation.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Automation Settings
    AUTO_BID_OPTIMIZATION_ENABLED: bool = False
    AUTO_BUDGET_OPTIMIZATION_ENABLED: bool = False
    AUTOMATION_CHECK_INTERVAL_MINUTES: int = 60
    
    # Performance Thresholds
    MIN_ROAS_THRESHOLD: float = 2.0
    MAX_CPA_THRESHOLD: float = 50.0
    MIN_CTR_THRESHOLD: float = 0.01
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Globális settings instance
settings = Settings()


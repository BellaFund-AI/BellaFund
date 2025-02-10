"""
Data integrity checks and preprocessing
Ensures quality of input data for AI models
"""
from pydantic import BaseModel, confloat, validator

class TokenDataSchema(BaseModel):
    symbol: str
    price_volatility: confloat(ge=0)
    trading_volume: confloat(ge=0)
    social_activity: confloat(ge=0)
    
    @validator('*', pre=True)
    def replace_nan(cls, value):
        """Handle missing values before validation"""
        return 0 if pd.isna(value) else value

class AnalysisMetrics(BaseModel):
    liquidity_depth: confloat(ge=0)
    whale_activity: confloat(ge=0)
    github_activity: confloat(ge=0) 
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ProductMemory(BaseModel):
    # Inputs
    artisan_profile: Dict[str, Any] = Field(default_factory=dict)
    product: Dict[str, Any] = Field(default_factory=dict)
    story_input: Dict[str, Any] = Field(default_factory=dict)
    market_input: Dict[str, Any] = Field(default_factory=dict)

    # Agent Outputs
    story: Dict[str, Any] = Field(default_factory=dict)
    market: Dict[str, Any] = Field(default_factory=dict)
    listing: Dict[str, Any] = Field(default_factory=dict)
    translation: Dict[str, Any] = Field(default_factory=dict)
    score: Dict[str, Any] = Field(default_factory=dict)

    def add_field(self, section: str, data: Dict[str, Any]):
        if hasattr(self, section):
            current_data = getattr(self, section)
            current_data.update(data)
            setattr(self, section, current_data)
        else:
            raise ValueError(f"Section {section} does not exist in memory.")

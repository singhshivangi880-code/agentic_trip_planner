from pydantic import BaseModel, Field

class VisaRequirement(BaseModel):
    is_visa_required: bool
    details: str
    official_link: str = Field(description="Official government or embassy link. Crucial for volatile info.")
    is_volatile: bool = Field(default=True, description="Always true for visa info since rules change.")

class DocumentRequirement(BaseModel):
    document_name: str
    description: str

class ReadinessPlan(BaseModel):
    visa_requirement: VisaRequirement
    documents: list[DocumentRequirement]
    insurance_reminder: str
    connectivity_checklist: list[str] = Field(description="e.g. eSim, adapter types")
    currency_checklist: list[str] = Field(description="e.g. local currency, cash vs card")
    travel_advisory: str = Field(description="Current travel advisory level or warnings")
    advisory_link: str = Field(description="Official advisory link")

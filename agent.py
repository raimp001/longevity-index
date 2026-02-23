from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import anthropic
import httpx
import json
import os

app = FastAPI(title="Longevity Index", description="AI-powered longevity biomarker analysis and healthspan optimization agent")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

class BiomarkerProfile(BaseModel):
  age: int
  sex: str
  biomarkers: Dict[str, float]
  lifestyle: Optional[Dict[str, str]] = None

class LongevityScore(BaseModel):
  biological_age: float
  chronological_age: int
  longevity_score: float
  top_risk_factors: List[str]
  top_interventions: List[str]
  estimated_healthspan_gain_years: float
  summary: str

class InterventionQuery(BaseModel):
  intervention: str
  age: int
  current_biomarkers: Optional[Dict[str, float]] = None

class InterventionAnalysis(BaseModel):
  intervention: str
  evidence_level: str
  expected_lifespan_impact_years: float
  expected_healthspan_impact_years: float
  mechanisms: List[str]
  side_effects: List[str]
  recommended_protocol: str
  pubmed_references: List[str]

BIOMARKER_RANGES = {
  "hba1c": {"optimal": (4.5, 5.2), "unit": "%", "name": "HbA1c"},
  "crp": {"optimal": (0, 1.0), "unit": "mg/L", "name": "C-Reactive Protein"},
  "igf1": {"optimal": (100, 200), "unit": "ng/mL", "name": "IGF-1"},
  "testosterone": {"optimal": (400, 700), "unit": "ng/dL", "name": "Testosterone (male)"},
  "vitamin_d": {"optimal": (40, 80), "unit": "ng/mL", "name": "Vitamin D"},
  "homocysteine": {"optimal": (0, 9), "unit": "umol/L", "name": "Homocysteine"},
  "triglycerides": {"optimal": (0, 100), "unit": "mg/dL", "name": "Triglycerides"},
  "hdl": {"optimal": (60, 100), "unit": "mg/dL", "name": "HDL Cholesterol"},
  "fasting_glucose": {"optimal": (70, 90), "unit": "mg/dL", "name": "Fasting Glucose"},
  "telomere_length": {"optimal": (7, 9), "unit": "kb", "name": "Telomere Length"},
}

LONGEVITY_INTERVENTIONS = [
  "caloric restriction", "time-restricted eating", "metformin", "rapamycin",
  "NAD+ precursors", "senolytics", "exercise", "sleep optimization",
  "cold exposure", "heat therapy", "omega-3", "resveratrol"
]

async def search_longevity_papers(query: str) -> List[str]:
  async with httpx.AsyncClient() as hclient:
    try:
      url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
      params = {"db": "pubmed", "term": f"{query} longevity aging lifespan", "retmax": 5, "retmode": "json"}
      r = await hclient.get(url, params=params, timeout=10)
      data = r.json()
      ids = data.get("esearchresult", {}).get("idlist", [])
      return [f"https://pubmed.ncbi.nlm.nih.gov/{pid}/" for pid in ids[:3]]
    except:
      return []

def analyze_biomarker_deviations(biomarkers: Dict[str, float]) -> List[str]:
  issues = []
  for marker, value in biomarkers.items():
    if marker in BIOMARKER_RANGES:
      low, high = BIOMARKER_RANGES[marker]["optimal"]
      name = BIOMARKER_RANGES[marker]["name"]
      unit = BIOMARKER_RANGES[marker]["unit"]
      if value < low:
        issues.append(f"{name}: {value} {unit} (below optimal {low}-{high})")
      elif value > high:
        issues.append(f"{name}: {value} {unit} (above optimal {low}-{high})")
  return issues

@app.post("/analyze-longevity", response_model=LongevityScore)
async def analyze_longevity(profile: BiomarkerProfile):
  deviations = analyze_biomarker_deviations(profile.biomarkers)
  papers = await search_longevity_papers("biomarker biological age")

  prompt = f"""You are a longevity medicine AI agent specializing in biological age assessment.

Patient Profile:
- Chronological Age: {profile.age}
- Sex: {profile.sex}
- Biomarkers: {profile.biomarkers}
- Lifestyle: {profile.lifestyle or 'not provided'}
- Biomarker Deviations from Optimal: {deviations}
- Reference Ranges: {BIOMARKER_RANGES}
- Recent Research: {papers}

Provide a comprehensive longevity analysis:
1. Estimated biological age (based on biomarker patterns)
2. Longevity score 0-100 (100 = exceptional)
3. Top 3 risk factors
4. Top 3 interventions to improve healthspan
5. Estimated healthspan gain from interventions (years)
6. 2-3 sentence summary

Respond as JSON:
{{
  "biological_age": 0.0,
  "longevity_score": 0.0,
  "top_risk_factors": ["factor1"],
  "top_interventions": ["intervention1"],
  "estimated_healthspan_gain_years": 0.0,
  "summary": "text"
}}"""

  response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1200,
    messages=[{"role": "user", "content": prompt}]
  )
  text = response.content[0].text
  start = text.find("{")
  end = text.rfind("}") + 1
  try:
    result = json.loads(text[start:end])
  except json.JSONDecodeError:
    result = {"biological_age": float(profile.age), "longevity_score": 50.0, "top_risk_factors": deviations[:3], "top_interventions": LONGEVITY_INTERVENTIONS[:3], "estimated_healthspan_gain_years": 2.0, "summary": text}

  return LongevityScore(
    chronological_age=profile.age,
    biological_age=result.get("biological_age", float(profile.age)),
    longevity_score=result.get("longevity_score", 50.0),
    top_risk_factors=result.get("top_risk_factors", []),
    top_interventions=result.get("top_interventions", []),
    estimated_healthspan_gain_years=result.get("estimated_healthspan_gain_years", 0.0),
    summary=result.get("summary", "")
  )

@app.post("/analyze-intervention", response_model=InterventionAnalysis)
async def analyze_intervention(query: InterventionQuery):
  papers = await search_longevity_papers(query.intervention)

  prompt = f"""You are a longevity research AI agent analyzing interventions.

Intervention: {query.intervention}
Patient Age: {query.age}
Current Biomarkers: {query.current_biomarkers or 'not provided'}
PubMed References: {papers}

Analyze this longevity intervention as JSON:
{{"evidence_level": "strong/moderate/weak/experimental", "expected_lifespan_impact_years": 0.0, "expected_healthspan_impact_years": 0.0, "mechanisms": ["mechanism1"], "side_effects": ["effect1"], "recommended_protocol": "dosage and timing", "pubmed_references": {papers}}}"""

  response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=900,
    messages=[{"role": "user", "content": prompt}]
  )
  text = response.content[0].text
  start = text.find("{")
  end = text.rfind("}") + 1
  try:
    result = json.loads(text[start:end])
  except json.JSONDecodeError:
    result = {"evidence_level": "moderate", "expected_lifespan_impact_years": 1.0, "expected_healthspan_impact_years": 2.0, "mechanisms": [], "side_effects": [], "recommended_protocol": text, "pubmed_references": papers}

  return InterventionAnalysis(intervention=query.intervention, **result)

@app.get("/biomarker-reference")
def get_biomarker_reference():
  return BIOMARKER_RANGES

@app.get("/interventions-list")
def get_interventions():
  return {"interventions": LONGEVITY_INTERVENTIONS}

@app.get("/health")
def health():
  return {"status": "ok", "service": "longevity-index"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)

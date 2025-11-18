"""FastAPI application for the SOCI Act Compliance Automation Platform.

This module intentionally keeps in-memory stores so the API can be exercised
inside the kata environment without any external dependencies. The design is
compatible with PostgreSQL persistence and the data models map directly to the
schema documented under ``docs/openapi.yaml``.
"""

from __future__ import annotations

import csv
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Ensure demo data is seeded exactly once per application lifecycle."""

    seed_demo_data()
    yield


app = FastAPI(
    title="Australian SOCI Act Compliance Automation Platform",
    description=(
        "API surface for asset automation, CIRMP templates, compliance "
        "monitoring, and ACSC reporting."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AssetBase(BaseModel):
    name: str
    sector: str = Field(
        description="One of the 11 SOCI sectors", examples=["Energy", "Communications"]
    )
    category: str = Field(description="Detailed category inside the sector")
    asset_type: str = Field(description="Asset classification, e.g. IT server, OT")
    criticality: str = Field(description="Criticality rating", default="High")
    owner: str = Field(description="Responsible owner or team")


class Asset(AssetBase):
    id: str
    created_at: datetime


class AssetCreate(AssetBase):
    pass


class BulkImportPayload(BaseModel):
    csv: str = Field(description="CSV payload with headers matching AssetCreate")


class TemplateRequest(BaseModel):
    asset_type: str
    organisation_size: str = Field(pattern="^(small|medium|large)$")
    sector: str


class Template(BaseModel):
    id: str
    asset_type: str
    organisation_size: str
    sector: str
    hazards: List[str]
    controls: List[str]
    evidence: List[str]
    review_cadence_days: int


class ComplianceScore(BaseModel):
    asset_id: Optional[str]
    score: float
    drift_indicators: List[str]
    open_issues: int
    timestamp: datetime


class Incident(BaseModel):
    id: str
    asset_id: Optional[str]
    title: str
    severity: str
    description: str
    impact_assessment: str
    evidence_bundle: List[str]
    status: str
    created_at: datetime


class IncidentCreate(BaseModel):
    asset_id: Optional[str]
    title: str
    severity: str
    description: str
    evidence_bundle: List[str] = []


class Supplier(BaseModel):
    id: str
    name: str
    geo: str
    tier: int = 1
    risk_score: float


class SupplierIngestRequest(BaseModel):
    name: str
    geo: str
    tier: int = 1
    dependencies: List[str] = []


class BoardReportRequest(BaseModel):
    audience: str = Field(description="E.g. Board, Audit & Risk Committee")
    include_supply_chain: bool = True
    include_incident_summary: bool = True


class BoardReport(BaseModel):
    id: str
    generated_at: datetime
    kpis: Dict[str, str]
    executive_summary: str
    next_quarter_priorities: List[str]
    top_risks: List[str]
    attachments: List[str]


DATABASE: Dict[str, Dict[str, object]] = {
    "assets": {},
    "templates": {},
    "incidents": {},
    "suppliers": {},
}

ALL_HAZARDS = [
    "Physical security",
    "Personnel insider threat",
    "Supply chain compromise",
    "Cyber intrusion",
    "Operational technology disruption",
]

SECTOR_CONTROLS = {
    "Energy": [
        "NIST CSF alignment",
        "Backup fuel logistics checks",
        "Protected SCADA network zoning",
    ],
    "Communications": [
        "DDoS response plans",
        "Satellite uplink redundancy",
        "Critical spares availability",
    ],
    "Finance": [
        "Payment system segregation",
        "SOAR automation for ACSC uplift",
        "CPS 234 attestations",
    ],
}


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "SOCI Act Compliance Automation Platform API"}


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "healthy"}


@app.get("/assets", response_model=List[Asset])
def list_assets() -> List[Asset]:
    return list(DATABASE["assets"].values())


@app.post("/assets", response_model=Asset, status_code=201)
def create_asset(asset: AssetCreate) -> Asset:
    asset_id = str(uuid4())
    record = Asset(
        id=asset_id, created_at=datetime.now(timezone.utc), **asset.model_dump()
    )
    DATABASE["assets"][asset_id] = record
    return record


@app.post("/assets/bulk_import", response_model=Dict[str, int])
def bulk_import(payload: BulkImportPayload) -> Dict[str, int]:
    rows = payload.csv.splitlines()
    created = 0
    reader = csv.DictReader(rows)
    for row in reader:
        asset = AssetCreate(
            name=row["name"],
            sector=row["sector"],
            category=row["category"],
            asset_type=row["asset_type"],
            criticality=row.get("criticality", "High"),
            owner=row.get("owner", "Unassigned"),
        )
        create_asset(asset)
        created += 1
    return {"imported": created}


@app.get("/cirmp/templates", response_model=List[Template])
def list_templates() -> List[Template]:
    return list(DATABASE["templates"].values())


@app.post("/cirmp/templates/generate", response_model=Template)
def generate_template(payload: TemplateRequest) -> Template:
    template = build_cirmp_template(payload)
    DATABASE["templates"][template.id] = template
    return template


@app.get("/compliance/score", response_model=ComplianceScore)
def overall_compliance_score() -> ComplianceScore:
    return build_compliance_score()


@app.get("/compliance/score/{asset_id}", response_model=ComplianceScore)
def asset_score(asset_id: str) -> ComplianceScore:
    if asset_id not in DATABASE["assets"]:
        raise HTTPException(status_code=404, detail="Asset not found")
    return build_compliance_score(asset_id)


@app.post("/incidents", response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate) -> Incident:
    incident_id = str(uuid4())
    record = Incident(
        id=incident_id,
        created_at=datetime.now(timezone.utc),
        status="triage",
        impact_assessment="Pending",
        evidence_bundle=payload.evidence_bundle,
        **payload.model_dump(exclude={"evidence_bundle"}),
    )
    DATABASE["incidents"][incident_id] = record
    return record


@app.post("/incidents/{incident_id}/report")
def report_incident(incident_id: str) -> Dict[str, object]:
    incident = DATABASE["incidents"].get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    payload = build_acsc_payload(incident)
    incident.status = "reported"
    incident.impact_assessment = payload["impact_assessment"]
    return payload


@app.post("/supplychain/ingest", response_model=Supplier)
def ingest_supplier(payload: SupplierIngestRequest) -> Supplier:
    supplier_id = str(uuid4())
    risk_score = 50 + payload.tier * 10 + len(payload.dependencies) * 5
    supplier = Supplier(
        id=supplier_id,
        name=payload.name,
        geo=payload.geo,
        tier=payload.tier,
        risk_score=min(risk_score, 99),
    )
    DATABASE["suppliers"][supplier_id] = supplier
    return supplier


@app.get("/supplychain/risk-score", response_model=Dict[str, float])
def supply_chain_score() -> Dict[str, float]:
    suppliers = DATABASE["suppliers"].values()
    if not suppliers:
        return {"average_risk": 0.0}
    return {"average_risk": sum(s.risk_score for s in suppliers) / len(suppliers)}


@app.post("/reports/board", response_model=BoardReport)
def generate_board_report(payload: BoardReportRequest) -> BoardReport:
    report = BoardReport(
        id=str(uuid4()),
        generated_at=datetime.now(timezone.utc),
        kpis={
            "overall_compliance": f"{overall_compliance_score().score}%",
            "open_incidents": str(len(DATABASE["incidents"])),
        },
        executive_summary=(
            "CIRMP coverage improving with automation of ACSC reporting. "
            "Supply chain automation live for critical vendors."
        ),
        next_quarter_priorities=[
            "Complete OT segmentation uplift",
            "Roll out IEC 62443 mapping to all OT zones",
            "Automate evidence capture for SOC2",
        ],
        top_risks=[
            "Converged IT/OT credential compromise",
            "Single points of failure in satellite backhaul",
            "Legacy vendor patch fatigue",
        ],
        attachments=[
            "docs/reports/board_report_sample.md",
            "docs/CIRMP_templates/README.md",
        ],
    )
    return report


def _asset_exists(name: str) -> bool:
    return any(asset.name == name for asset in DATABASE["assets"].values())


def _template_exists(sample: Dict[str, str]) -> bool:
    return any(
        template.asset_type == sample["asset_type"]
        and template.organisation_size == sample["organisation_size"]
        and template.sector == sample["sector"]
        for template in DATABASE["templates"].values()
    )


def _supplier_exists(name: str) -> bool:
    return any(supplier.name == name for supplier in DATABASE["suppliers"].values())


def seed_demo_data(force: bool = False) -> Dict[str, int]:
    """Seed demo data safely so that repeated calls are idempotent."""

    if force:
        for store in DATABASE.values():
            store.clear()

    for row in SAMPLE_ASSETS:
        if not _asset_exists(row["name"]):
            create_asset(AssetCreate(**row))

    for template_request in SAMPLE_TEMPLATES:
        if not _template_exists(template_request):
            generate_template(TemplateRequest(**template_request))

    for supplier in SAMPLE_SUPPLIERS:
        if not _supplier_exists(supplier["name"]):
            ingest_supplier(SupplierIngestRequest(**supplier))

    return {name: len(store) for name, store in DATABASE.items()}


@app.post("/demo/seed", response_model=Dict[str, int])
def trigger_seed(force: bool = False) -> Dict[str, int]:
    """HTTP wrapper that mirrors the helper used by lifespan + CLI flows."""

    return seed_demo_data(force=force)


def build_cirmp_template(payload: TemplateRequest) -> Template:
    controls = SECTOR_CONTROLS.get(payload.sector, ["Baseline access reviews", "Multi-factor authentication"])
    additional_controls = [
        f"IEC 62443 alignment for {payload.asset_type}",
        f"Incident runbook for {payload.asset_type}",
        "Supply chain verification checks",
    ]
    template = Template(
        id=str(uuid4()),
        asset_type=payload.asset_type,
        organisation_size=payload.organisation_size,
        sector=payload.sector,
        hazards=ALL_HAZARDS,
        controls=controls + additional_controls,
        evidence=[
            "ACSC incident tickets",
            "Patch compliance exports",
            "Risk workshop notes",
        ],
        review_cadence_days=90 if payload.organisation_size == "large" else 180,
    )
    return template


def build_compliance_score(asset_id: Optional[str] = None) -> ComplianceScore:
    base = 75.0
    if asset_id:
        asset = DATABASE["assets"].get(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        modifier = 5 if asset.criticality == "Low" else -5
        base = max(min(base + modifier, 100), 0)
    drift = ["Evidence overdue", "MFA exceptions"] if base < 80 else []
    return ComplianceScore(
        asset_id=asset_id,
        score=round(base, 2),
        drift_indicators=drift,
        open_issues=len(DATABASE["incidents"]),
        timestamp=datetime.now(timezone.utc),
    )


def build_acsc_payload(incident: Incident) -> Dict[str, object]:
    return {
        "acsc_version": "2023-incident-schema",
        "incident_id": incident.id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "severity": incident.severity,
        "impact_assessment": "Service disruption < 4 hours",
        "asset_reference": incident.asset_id,
        "evidence_manifest": incident.evidence_bundle,
        "chain_of_custody": {
            "reporter": "demo.security.officer@asacap.example",
            "signed": True,
        },
    }


SAMPLE_ASSETS = [
    {
        "name": "Sydney Core Switching",
        "sector": "Communications",
        "category": "Network",
        "asset_type": "Comms tower",
        "criticality": "Critical",
        "owner": "Network Operations",
    },
    {
        "name": "Pilbara OT SCADA",
        "sector": "Energy",
        "category": "OT",
        "asset_type": "SCADA RTU",
        "criticality": "High",
        "owner": "OT Reliability",
    },
    {
        "name": "Payments Cluster",
        "sector": "Finance",
        "category": "IT",
        "asset_type": "Linux server",
        "criticality": "High",
        "owner": "Banking Platforms",
    },
]

SAMPLE_TEMPLATES = [
    {"asset_type": "IT server", "organisation_size": "large", "sector": "Finance"},
    {"asset_type": "SCADA RTU", "organisation_size": "medium", "sector": "Energy"},
    {"asset_type": "Comms tower", "organisation_size": "small", "sector": "Communications"},
]

SAMPLE_SUPPLIERS = [
    {"name": "Critical Power Pty Ltd", "geo": "AU", "tier": 1, "dependencies": ["Logistics"]},
    {"name": "Satellite Partners", "geo": "AU", "tier": 2, "dependencies": ["Launch", "Spectrum"]},
]



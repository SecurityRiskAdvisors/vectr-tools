import re

from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator
from enum import Enum


class TestCaseOutcomeEnum(str, Enum):
    tbd = 'TBD'
    blocked = 'Blocked'
    detected = 'Detected'
    not_detected = 'NotDetected'


class AlertSeverityEnum(str, Enum):
    tbd = 'TBD'
    info = 'Info'
    low = 'Low'
    med = 'Med'
    high = 'High'
    critical = 'Critical'


class AlertTriggeredEnum(str, Enum):
    tbd = 'TBD',
    yes = 'Yes',
    no = 'No'


class ActivityLoggedEnum(str, Enum):
    tbd = 'TBD',
    yes = 'Yes',
    no = 'No'


class TestCase(BaseModel):
    name: str = Field(alias="Variant")
    description: Optional[str] = Field(alias="Objective")
    command: Optional[str] = Field(alias="Command")
    attacker_tools: Optional[List[str]] = Field(alias="Attacker Tools")
    phase: Optional[str] = Field(alias="Phase")
    mitre_id: Optional[str] = Field(alias="MitreID")
    technique: Optional[str] = Field(alias="Method")
    status: Optional[str] = Field(alias="Status")
    outcome: Optional[str] = Field(alias="Outcome")
    outcome_notes: Optional[str] = Field(alias="Outcome Notes")
    alert_severity: Optional[str] = Field(alias="Alert Severity")
    alert_triggered: Optional[str] = Field(alias="Alert Triggered")
    activity_logged: Optional[str] = Field(alias="Activity Logged")
    detection_recommendations: Optional[str] = Field(alias="Detection Recommendations")
    sources: Optional[List[str]] = Field(alias="SourceIps")
    targets: Optional[List[str]] = Field(alias="TargetAssets")
    defense_layers: Optional[List[str]]
    detecting_tools: Optional[List[str]]
    start_time: Optional[str]
    start_time_epoch: Optional[int]
    stop_time: Optional[str]
    stop_time_epoch: Optional[int]
    detection_time: Optional[str]
    detection_time_epoch: Optional[int]
    organizations: Optional[List[str]]
    tags: Optional[List[str]]
    references: Optional[List[str]]

    # @TODO - combine for reuse, getting weird behavior
    @validator('sources', pre=True, allow_reuse=True)
    def validate_sources(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('attacker_tools', pre=True, allow_reuse=True)
    def validate_csv(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('targets', pre=True, allow_reuse=True)
    def validate_targets(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('outcome', pre=True, allow_reuse=True)
    @validator('status', pre=True, allow_reuse=True)
    @validator('alert_severity', pre=True, allow_reuse=True)
    def validate_upper_enum(cls, v: str) -> str:
        return v.upper()


class Campaign(BaseModel):
    name: str
    test_cases: Optional[List[TestCase]]


class Assessment(BaseModel):
    name = str
    campaigns: Optional[Dict[str, Campaign]]

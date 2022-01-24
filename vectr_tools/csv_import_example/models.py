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
    defense_layers: Optional[List[str]] = Field(alias="ExpectedDetectionLayers")
    detecting_tools: Optional[List[str]] = Field(alias="DetectingTools")
    start_time: Optional[str] = Field(alias="Start Time")
    # start_time_epoch: Optional[int]
    stop_time: Optional[str] = Field(alias="Stop Time")
    # stop_time_epoch: Optional[int]
    detection_time: Optional[str] = Field(alias="Detection Time")
    # detection_time_epoch: Optional[int]
    organizations: Optional[List[str]] = Field(alias="Organizations")
    tags: Optional[List[str]] = Field(alias="Tags")
    references: Optional[List[str]] = Field(alias="References")

    # @TODO - combine for reuse, getting weird behavior
    @validator('sources', pre=True, allow_reuse=True)
    def validate_sources(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('references', pre=True, allow_reuse=True)
    def validate_references(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('tags', pre=True, allow_reuse=True)
    def validate_tags(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('organizations', pre=True, allow_reuse=True)
    def validate_organizations(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('defense_layers', pre=True, allow_reuse=True)
    def validate_defense_layers(cls, v: str) -> List[str]:
        return v.split(',')

    @validator('detecting_tools', pre=True, allow_reuse=True)
    def validate_detecting_tools(cls, v: str) -> List[str]:
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

# import re
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator, root_validator

"""
[
          {
            "testCaseData": {
              "name": "Bulk Template Test 1",
              "description": "testing this input",
              "operatorGuidance": "Do something suspicious like listen to ska music",
              "phase": "Execution",
              "technique": "T1110",
              "organization": "Security Risk Advisors",
              "status": "INPROGRESS",
              "outcome": "NOTDETECTED",
              "activityLogged": "YES",
              "redTools":  [{
                "name": "Native Windows Commands"
              }]
            }
          }
"""


class TestCase(BaseModel):
    name: str = Field(alias="Variant")
    description: Optional[str] = Field(alias="Objective")
    phase: Optional[str] = Field(alias="Phase")
    technique: Optional[str] = Field(alias="MitreID")
    tags: Optional[List[str]] = Field(alias="Tags")
    organization: Optional[str] = Field(alias="Organizations")
    status: Optional[str] = Field(alias="Status")
    targets: Optional[List[str]] = Field(alias="TargetAssets")
    sources: Optional[List[str]] = Field(alias="SourceIps")
    defenses: Optional[List[str]] = Field(alias="ExpectedDetectionLayers")
    detectionSteps: Optional[str] = Field(alias="Detection Recommendations")
    outcome: Optional[str] = Field(alias="Outcome")
    outcomeNotes: Optional[str] = Field(alias="Outcome Notes")
    alertSeverity: Optional[str] = Field(alias="Alert Severity")
    alertTriggered: Optional[str] = Field(alias="Alert Triggered")
    activityLogged: Optional[str] = Field(alias="Activity Logged")
    detectionTime: Optional[str] = Field(alias="Detection Time")
    detectingDefenseTools: Optional[List[Dict[str, str]]] = Field(alias="DetectingTools")
    references: Optional[List[str]] = Field(alias="References")
    redTools: Optional[List[Dict[str, str]]] = Field(alias="Attacker Tools")
    operatorGuidance: Optional[str] = Field(alias="Command")
    attackStart: Optional[str] = Field(alias="Start Time")
    attackStop: Optional[str] = Field(alias="Stop Time")

    # @TODO - need to add to API
    # -------------------------------------
    # outcome_notes: Optional[str] = Field(alias="Outcome Notes")
    # -------------------------------------
    # @NOTE - Not supported by API
    # -------------------------------------
    # technique: Optional[str] = Field(alias="Method")
    # start_time_epoch: Optional[int]
    # stop_time_epoch: Optional[int]
    # detection_time_epoch: Optional[int]

    @root_validator(pre=True)
    def check_technique(cls, values):
        if 'MitreID' in values and values['MitreID']:
            # everything is fine, MitreID exists, continue
            return values

        if 'Method' in values and values['Method']:
            values['MitreID'] = values['Method']
            return values

        print(values)
        raise ValueError("Non-empty Method (Attack Technique) or MitreID required for Test Case creation")

    # @TODO - combine for reuse, getting weird behavior with multiple annotations
    @validator('sources', pre=True, allow_reuse=True)
    def validate_sources(cls, v: str) -> Optional[List[str]]:
        sources = v.split(',')
        if not sources:
            return None
        return list(filter(None, sources))

    @validator('references', pre=True, allow_reuse=True)
    def validate_references(cls, v: str) -> Optional[List[str]]:
        refs = v.split(',')
        if not refs:
            return None
        return list(filter(None, refs))

    @validator('tags', pre=True, allow_reuse=True)
    def validate_tags(cls, v: str) -> Optional[List[str]]:
        tags = v.split(',')
        if not tags:
            return None
        return list(filter(None, tags))

    @validator('organization', pre=True, allow_reuse=True)
    def validate_organization(cls, v: str) -> Optional[str]:
        orgs = v.split(',')
        if orgs:
            return orgs[0]
        else:
            return None

    @validator('defenses', pre=True, allow_reuse=True)
    def validate_defenses(cls, v: str) -> Optional[List[str]]:
        defenses = v.split(',')
        if not defenses:
            return None
        return list(filter(None, defenses))

    @validator('detectingDefenseTools', pre=True, allow_reuse=True)
    def validate_detecting_tools(cls, v: str) -> List[Dict[str, str]]:
        tools = []
        tool_names = v.split(',')
        tool_names = list(filter(None, tool_names))

        for tool_name in tool_names:
            tools.append({"name": tool_name})

        return tools

    @validator('redTools', pre=True, allow_reuse=True)
    def validate_attack_tools(cls, v: str) -> List[Dict[str, str]]:
        tools = []
        tool_names = v.split(',')
        tool_names = list(filter(None, tool_names))

        for tool_name in tool_names:
            tools.append({"name": tool_name})

        return tools

    @validator('targets', pre=True, allow_reuse=True)
    def validate_targets(cls, v: str) -> Optional[List[str]]:
        targets = v.split(',')
        if not targets:
            return None
        return list(filter(None, targets))

    @validator('status', pre=True, allow_reuse=True)
    def validate_upper_enum1(cls, v: str) -> str:
        return v.upper()

    @validator('outcome', pre=True, allow_reuse=True)
    def validate_upper_enum2(cls, v: str) -> str:
        return v.upper()

    @validator('alertSeverity', pre=True, allow_reuse=True)
    def validate_upper_enum3(cls, v: str) -> str:
        return v.upper()

    @validator('alertTriggered', pre=True, allow_reuse=True)
    def validate_upper_enum4(cls, v: str) -> str:
        return v.upper()

    @validator('activityLogged', pre=True, allow_reuse=True)
    def validate_upper_enum5(cls, v: str) -> str:
        return v.upper()

    @validator('attackStart', pre=True, allow_reuse=True)
    def validate_attack_start(cls, v: str) -> Optional[str]:
        if not v:
            return None
        return v

    @validator('attackStop', pre=True, allow_reuse=True)
    def validate_attack_stop(cls, v: str) -> Optional[str]:
        if not v:
            return None
        return v

    @validator('detectionTime', pre=True, allow_reuse=True)
    def validate_detection_time(cls, v: str) -> Optional[str]:
        if not v:
            return None
        return v


class Campaign(BaseModel):
    name: str
    test_cases: Optional[List[TestCase]]


class Assessment(BaseModel):
    name = str
    campaigns: Optional[Dict[str, Campaign]]

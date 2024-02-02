from __future__ import annotations
from typing import List, Optional, Union
from pydantic import BaseModel, Field


class LineageNode(BaseModel):
    filePath: str
    name: str
    uniqueId: str


class DiscoLineageResponse(BaseModel):
    lineage: List[LineageNode]


class DiscoEnvironmentResponse(BaseModel):
    applied: DiscoLineageResponse


class LineageDiscoResponse(BaseModel):
    environment: DiscoEnvironmentResponse

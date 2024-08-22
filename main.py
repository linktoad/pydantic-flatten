from __future__ import annotations

from typing import Any

import jmespath
from pydantic import BaseModel, ValidationInfo, model_validator


class JMESPathFieldExtractor(BaseModel):

    @model_validator(mode="before")
    def evaluate(cls, data: Any, info: ValidationInfo):
        if not isinstance(data, dict):
            return data
        if info.context and info.context.get("jmesq") is False:  # Optionally disable the logic
            return data

        query_fields = {
            field: query
            for field, info in cls.model_fields.items()
            if (query := (info.json_schema_extra or {}).get("jmesq"))
        }
        multiselect_hash = "{" + ",".join(f"{k}: {v}" for k, v in query_fields.items()) + "}"
        return data | jmespath.search(multiselect_hash, data)


if __name__ == "__main__":
    from pydantic import Field

    json_data = """
    {
        "uid": "bb28471e-cde6-4eff-ace4-9a7f4f50882a",
        "vendor": "TESLA",
        "information": {
            "vin": "2HGFB2F5XEH542858",
            "model": "Model S P85",
            "year": "2020"
        }
    }
    """

    class Vehicle(JMESPathFieldExtractor):
        uid: str = Field(jmesq="uid")
        model: str = Field(jmesq="information.model")
        vin: str = Field(jmesq="information.vin")
        year: int = Field(jmesq="information.year")

    m = Vehicle.model_validate_json(json_data)
    print(m.model_dump_json(indent=4))

    """
    {
        "uid": "bb28471e-cde6-4eff-ace4-9a7f4f50882a",
        "model": "Model S P85",
        "vin": "2HGFB2F5XEH542858",
        "year": 2020
    }
    """

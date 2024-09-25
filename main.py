from __future__ import annotations

from typing import Any

import jmespath
from pydantic import BaseModel, model_validator

JMESPATH_FIELD_KEY = "q"


class JMESPathFieldExtractor(BaseModel):

    @model_validator(mode="before")
    @classmethod
    def evaluate_jmespath_fields_from_input(cls, data: Any) -> Any:
        """Evaluate the subclass' specified fields with `Field(q=<JMESPath query expression>)`"""
        query_fields = {
            field: query
            for field, info in cls.model_fields.items()
            if (query := (info.json_schema_extra or {}).get(JMESPATH_FIELD_KEY))
        }
        if not query_fields:
            return data

        multiselect_hash_expr = "{" + ",".join(f"{k}:{v}" for k, v in query_fields.items()) + "}"
        return data | jmespath.search(multiselect_hash_expr, data)


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
        uid: str = Field(q="uid")
        model: str = Field(q="information.model")
        vin: str = Field(q="information.vin")
        year: int = Field(q="information.year")

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

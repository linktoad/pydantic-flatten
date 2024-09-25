# pydantic-flatten

A proof of concept of how to extract nested JSON API data into a (typically flat) Pydantic model.

In this example I use [Jmespath](https://jmespath.org/), but this technique is not limited to this JSON query language/tool (I chose Jmespath because it's a dependency of [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and I work in an AWS environment, but you could use [jq](https://jqlang.github.io/jq/) or even `types.SimpleNamespace` for the same results).

It merely showcases a practical application on the misuse of `json_schema_extra` in `pydantic.Field` to embed arbitrary information at the model field level.

## Motivation

Often when ingesting JSON API data into a RDBMS table, you will need to flatten it, and JSON documents can get heavily nested.

The canonical way of parsing data like this is to create sub-models that faithfully model the structure of the JSON data. However, this can get quite tedious and a lot of set up is required. Then furthermore, a post-processing step is required to bring that field out to the final flattened model.

It would instead be great if we could tell Pydantic how to parse the data in the model definition itself. This also expands upon the philosophy and usefulness of Pydantic in having the validation and serialisation logic all in one place so that the code becomes almost declarative.

## Notes

**Requires Python3.9+**


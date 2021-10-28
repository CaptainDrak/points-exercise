from jsonschema import validate, SchemaError, ValidationError

def add_json_validation(request):
    schema = {
        "type" : "object",
        "properties" : {
            "payer" : {"type" : "string"},
            "points" : {"type" : "number"},
            "timestamp" : {"type" : "string", "format" : "date-time"}
        },
        "required": ["payer", "points", "timestamp"],
        "additionalProperties": False
    }

    try:
        validate(instance=request, schema=schema)
    except ValidationError as error:
        return error.message


def spend_json_validation(request):
    schema = {
        "type" : "object",
        "properties" : {
            "points" : {"type" : "number"},
        },
        "required": ["points"],
        "additionalProperties": False
    }

    try:
        validate(instance=request, schema=schema)
    except ValidationError as error:
        return error.message
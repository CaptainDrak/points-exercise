from jsonschema import validate, SchemaError, ValidationError

def error_handling(request, schema):
    try:
        validate(instance=request, schema=schema)
    except ValidationError as error:
        return error.message
    except SchemaError as error:
        return error.message

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

    return error_handling(request, schema)


def spend_json_validation(request):
    schema = {
        "type" : "object",
        "properties" : {
            "points" : {"type" : "number"},
        },
        "required": ["points"],
        "additionalProperties": False
    }

    return error_handling(request, schema)
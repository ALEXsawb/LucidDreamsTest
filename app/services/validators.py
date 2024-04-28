def validate_not_null_field_of_table(table, field_name: str, field_value: str):
    if not field_value:
        raise ValueError(f"The '{field_name}' field do not must be nullable")


def validate_max_length_string_field_of_table(table, field_name: str, field_value: str):
    if not isinstance(field_value, str):
        raise ValueError(f"The '{field_name}' field must be a string")

    columns = table.__table__.c
    max_length_password_field = getattr(columns, field_name).type.length
    if len(field_value) > max_length_password_field:
        raise ValueError(f"The '{field_name}' field must be less than {max_length_password_field} characters")

from django.core.exceptions import ValidationError

def custom_validation(data):
    # Example: Check if 'id' and 'password' fields are present in the data
    if 'id' not in data or 'password' not in data:
        raise ValidationError('Both "id" and "password" fields are required.')

    # You can add more custom validation logic here

    # If all validations pass, return the cleaned data
    return data

def validate_id(data):
    # Example: Check if 'id' field is present and is a valid id address
    id = data.get('id')
    if not id:
        raise ValidationError('id is required.')
    
    # You can add more email validation logic if needed

def validate_password(data):
    # Example: Check if 'password' field is present and meets certain criteria
    password = data.get('password')
    if not password:
        raise ValidationError('Password is required.')

    # You can add more password validation logic if needed

from rest_framework import serializers


def is_valid_string(value):
    for v in value.split():
        if not str(v).isalpha():
            raise serializers.ValidationError("Value should be a String. No Numeric and Special Characters allowed")


def is_valid_address(value):
    if not str(value).isascii():
        raise serializers.ValidationError("Value should be a String and only have ascii value")


def is_valid_contact(value):
    if not str(value).isdigit():
        raise serializers.ValidationError("Value should be a Integer Value. No Characters allowed")

    if len(str(value)) != 10:
        raise serializers.ValidationError("Length should be equal to 10 characters")


def is_valid_aadhar(value):
    if not str(value).isdigit():
        raise serializers.ValidationError("Value should be a Integer Value. No Characters allowed")

    if len(str(value)) != 12:
        raise serializers.ValidationError("Length should be equal 12 characters")


def is_valid_amount(value):
    try:
        float(value)
    except ValueError:
        raise serializers.ValidationError("It should be Float value")

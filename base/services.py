from django.core.exceptions import ValidationError
from django.db import models
from django.apps import apps

class BaseService:
    @classmethod
    def validate_required_fields(cls, fields: list, input: dict):
        """
        Validates that all required fields are present in kwargs.

        :param fields: A list of strings representing required field names.
        :param input: A dictionary of parameters to validate.
        :raises: ValidationError if any required field is missing.
        """
        missing_fields = [field for field in fields if field not in input]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}.")

    @classmethod
    def validate_and_extract_id(cls, key, kwargs):
        """
        Validates and extracts an ID for a given key (owner or wallet) from kwargs.

        :param key: The key prefix (e.g., 'owner' or 'wallet') to look for in kwargs.
        :param kwargs: A dictionary of parameters from which to extract the ID.
        :return: The extracted ID.
        :raises: ValidationError if the ID is missing or invalid.
        """
        object_info = kwargs.get(key, {})
        if isinstance(object_info, models.Model):
            return object_info.id
        object_id = object_info.get('id') if isinstance(object_info, dict) else object_info.get('id')
        direct_id = kwargs.get(f"{key}_id")

        # Validate that at least one valid ID is present
        if not object_id and not direct_id:
            raise ValidationError(f"Either {key} object with 'id' or {key}_id is required.")

        return object_id or direct_id

    @classmethod
    def get_instance_by_id(cls, model, obj_id):
        """
        Retrieves an instance of a given model by ID, with error handling for non-existent or invalid IDs.

        :param model: The Django model class to fetch an instance from.
        :param obj_id: The ID of the instance to retrieve.
        :return: An instance of the model.
        :raises: DoesNotExist if the instance does not exist.
        :raises: ValidationError if the instance does not exist or the ID is invalid.
        """
        try:
            return cls.get_instance_by_field(model, 'id', obj_id)
        except ValueError:
            raise ValidationError(f"Invalid {model.__name__} ID format. A valid integer is required.")

    @classmethod
    def get_instance_by_field(cls, model, field, value):
        """
        Retrieves an instance of a given model by a specific field value.

        :param model: The Django model class to fetch an instance from.
        :param field: The field name to filter by.
        :param value: The value to filter by.
        :return: An instance of the model.
        :raises: DoesNotExist if the instance does not exist.
        """
        return cls.lookup_model(model).objects.get(**{field: value})

    @classmethod
    def is_exists(cls, model, **kwargs):
        """
        Checks if a user exists with the given kwargs.

        :param model: The Django model class to check for.
        :param kwargs: Fields and their values to search for.
        :return: True if a user exists with the given fields, False otherwise.
        """
        return cls.lookup_model(model).objects.filter(**kwargs).exists()

    @classmethod
    def create_instance(cls, model, **kwargs):
        """
        Creates an instance of a given model with the provided kwargs.

        :param model: The Django model class to create an instance of.
        :param kwargs: Fields and their values for the new instance.
        :return: The newly created instance.
        """
        return cls.lookup_model(model).objects.create(**kwargs)

    @classmethod
    def get_queryset(cls, model):
        """
        Retrieves a queryset for a given model class.

        :param model: The Django model class to retrieve
        :return: A queryset of all instances of the model.
        """
        return cls.lookup_model(model).objects.all()

    @classmethod
    def lookup_model(cls, model):
        """
        Looks up a Django model class based on the provided input.
        """
        if isinstance(model, str) and '.' in model and len(model.split('.')) == 2:
            app = model.split('.')[0]
            model_name = model.split('.')[1]
            return apps.get_model(app, model_name)
        elif issubclass(model, models.Model):
            return model
        else:
            raise ValueError("Invalid model format. Must be a Django model class or 'app_name.model_name' string.")

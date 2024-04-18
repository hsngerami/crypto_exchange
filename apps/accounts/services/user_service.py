import logging
from typing import Union

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.accounts.models import User
from base.services import BaseService

logger = logging.getLogger(__name__)

class UserService(BaseService):

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.get_instance_by_id(User, user_id)

    @classmethod
    @transaction.atomic
    def update_user(cls, user_id, **kwargs):
        """
        Updates a user with the given kwargs, applying field validations as necessary.

        :param user_id: ID of the user to update.
        :param kwargs: Fields and their new values to update.
        :return: The updated User instance.
        :raises: ValidationError if any validations fail or the user does not exist.
        """
        # Fetch the user instance
        try:
            user = User.objects.select_for_update().get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist.")

        # Update fields from kwargs
        for field, value in kwargs.items():
            # Add any specific field validation here if necessary
            if hasattr(user, field):
                setattr(user, field, value)
            else:
                raise ValidationError(f"Field '{field}' is not valid for the User model.")

        # Perform additional model-specific validations if necessary
        user.full_clean()

        # Save the user instance
        user.save()
        return user

    @classmethod
    def update_profile(cls, user, **kwargs):
        """
        Updates a user profile with the given kwargs, applying field validations as necessary.

        :param user: The user to update the profile for.
        :param kwargs: Fields and their new values to update.
        :return: The updated Profile instance.
        :raises: ValidationError if any validations fail.
        """
        # Fetch the profile instance
        profile = user.profile

        # Update fields from kwargs
        for field, value in kwargs.items():
            # Add any specific field validation here if necessary
            if hasattr(profile, field):
                setattr(profile, field, value)
            else:
                raise ValidationError(f"Field '{field}' is not valid for the Profile model.")

        # Perform additional model-specific validations if necessary
        profile.full_clean()

        # Save the profile instance
        profile.save()

        return profile

    @classmethod
    def get_user_by_invitation_code(cls, invitation_code: str) -> Union[User, None]:
        """
        Retrieves a user by their invitation code, if it exists.

        :param invitation_code: The invitation code to search for.
        :return: The User instance with the given invitation code, if found.
        """
        return cls.get_instance_by_field(User, 'invitation_code', invitation_code)

    @classmethod
    def get_user_by_username(cls, username) -> User:
        """
        Retrieves a user by their mobile number or email, if it exists.

        :param identifier: The mobile number or email to search for.
        :return: The User instance with the given mobile number or email, if found.
        """
        user = User.objects.filter(username=username).first()
        if user is None:
            raise User.DoesNotExist(f"User with this mobile number or email does not exist.")
        return user

    @classmethod
    def is_user_exists(cls, **kwargs):
        """
        Checks if a user exists with the given kwargs.

        :param kwargs: Fields and their values to search for.
        :return: True if a user exists with the given fields, False otherwise.
        """
        return cls.is_exists(User, **kwargs)

    @classmethod
    def create_user(cls, **kwargs):
        """
        Creates a new user.

        :param kwargs: Keyword arguments containing user data.
        :return: The newly created User instance.
        """
        cls.validate_required_fields(['mobile_number', 'email', 'password'], kwargs)

        if cls.is_user_exists(mobile_number=kwargs['mobile_number']):
            raise ValidationError("User with this mobile number already exists.")
        if cls.is_user_exists(email=kwargs['email']):
            raise ValidationError("User with this email already exists.")

        # Hash the user's password
        kwargs['password'] = make_password(kwargs['password'])

        # Create the new user instance
        user = User.objects.create(**kwargs)
        return user

    @classmethod
    def create_profile(cls, user, **kwargs):
        """
        Creates a new user profile.
        :param user: The user to create the profile for.
        :param kwargs: Keyword arguments containing user profile data.
        :return: The newly created User instance.
        """
        cls.validate_required_fields(['national_code', 'birth_date'], kwargs)

        # Create the new user profile instance
        profile = cls.create_instance('accounts.Profile', owner=user, **kwargs)
        return profile

    @classmethod
    def create_user_validation_result(cls, user: User):
        """
        Creates a new validation result for the given user.

        :param user: The user to create the validation result for.
        :return: The newly created ValidationResultModel instance.
        """
        return cls.create_instance('accounts.ValidationResultModel', owner=user)

    @classmethod
    def is_validated_user_by_validation_field(cls, identifier, field):
        """
        Checks if a user is validated by the given field.

        :param identifier: The mobile number or email to search for.
        :param field: The field to check for validation.
        :return: True if the user is validated by the given field, False otherwise.
        """
        try:
            user = cls.get_user_by_username(identifier)
        except User.DoesNotExist:
            return False  # ignore if user does not exist
        return getattr(user.validated_result, field)

    @classmethod
    def user_is_validated(cls, identifier):
        """
        Checks if a user is validated by all fields.

        :param identifier: The mobile number or email to search for.
        :return: True if the user is validated by all fields, False otherwise.
        """
        try:
            user = cls.get_user_by_username(identifier)
        except User.DoesNotExist:
            return False  # ignore if user does not exist
        return user.validated_result.is_verified

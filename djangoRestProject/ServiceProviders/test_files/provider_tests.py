from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

from djangoRestProject.ServiceProviders.models import Provider


def test_save_provider_model(transactional_db):
    provider = Provider()
    provider.name = "Test Provider"
    provider.email = "provider@test.com"
    provider.phone_number = "123456789"
    provider.language = "en"
    provider.currency = "USD"
    provider.save()
    provider.full_clean()


def test_save_provider_model_invalid_email(transactional_db):
    provider = Provider()
    provider.name = "Test Provider"
    provider.email = "provider@test   . asdas "
    provider.phone_number = "123456789"
    provider.language = "en"
    provider.currency = "USD"
    provider.save()
    with pytest.raises(ValidationError):
        provider.full_clean()


def test_save_provider_model_missing_field(transactional_db):
    provider = Provider()
    provider.name = ""
    provider.email = "provider@test.com"
    provider.phone_number = "123456789"
    provider.language = "en"
    provider.currency = "USD"
    provider.save()
    with pytest.raises(ValidationError):
        provider.full_clean()

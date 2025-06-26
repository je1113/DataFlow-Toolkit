"""Unit tests for exception classes."""

import pytest

from dataflow_toolkit.core.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ConnectionError,
    DataFlowError,
    ExecutionError,
    PermissionError,
    ResourceError,
    RetryError,
    TimeoutError,
    TransformationError,
    ValidationError,
)


class TestDataFlowError:
    """Test base DataFlowError exception."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = DataFlowError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {}
        assert error.cause is None

    def test_error_with_details(self):
        """Test error with details."""
        error = DataFlowError("Test error", details={"key": "value", "number": 42})
        assert "Test error" in str(error)
        assert "key=value" in str(error)
        assert "number=42" in str(error)

    def test_error_with_cause(self):
        """Test error with cause."""
        cause = ValueError("Original error")
        error = DataFlowError("Wrapped error", cause=cause)
        assert "Wrapped error" in str(error)
        assert "Caused by: ValueError: Original error" in str(error)
        assert error.cause is cause


class TestConfigurationError:
    """Test ConfigurationError exception."""

    def test_config_error(self):
        """Test configuration error."""
        error = ConfigurationError(
            "Invalid configuration", config_key="database.host", config_value="invalid-host"
        )
        assert error.message == "Invalid configuration"
        assert error.details["config_key"] == "database.host"
        assert error.details["config_value"] == "invalid-host"

    def test_config_error_minimal(self):
        """Test minimal configuration error."""
        error = ConfigurationError("Bad config")
        assert error.message == "Bad config"
        assert "config_key" not in error.details
        assert "config_value" not in error.details


class TestValidationError:
    """Test ValidationError exception."""

    def test_validation_error(self):
        """Test validation error."""
        error = ValidationError(
            "Validation failed", field="email", value="not-an-email", constraint="email_format"
        )
        assert error.message == "Validation failed"
        assert error.details["field"] == "email"
        assert error.details["value"] == "not-an-email"
        assert error.details["constraint"] == "email_format"

    def test_validation_error_minimal(self):
        """Test minimal validation error."""
        error = ValidationError("Invalid data")
        assert error.message == "Invalid data"
        assert len(error.details) == 0


class TestConnectionError:
    """Test ConnectionError exception."""

    def test_connection_error(self):
        """Test connection error."""
        error = ConnectionError(
            "Failed to connect", host="localhost", port=5432, service="postgresql"
        )
        assert error.message == "Failed to connect"
        assert error.details["host"] == "localhost"
        assert error.details["port"] == 5432
        assert error.details["service"] == "postgresql"

    def test_connection_error_with_cause(self):
        """Test connection error with cause."""
        import socket

        cause = socket.error("Connection refused")
        error = ConnectionError("Database connection failed", host="db.example.com", cause=cause)
        assert error.cause is cause
        assert "socket.error" in str(error) or "error" in str(error)


class TestTransformationError:
    """Test TransformationError exception."""

    def test_transformation_error(self):
        """Test transformation error."""
        error = TransformationError(
            "Transform failed", transformer="JSONTransformer", input_type="str", output_type="dict"
        )
        assert error.message == "Transform failed"
        assert error.details["transformer"] == "JSONTransformer"
        assert error.details["input_type"] == "str"
        assert error.details["output_type"] == "dict"


class TestExecutionError:
    """Test ExecutionError exception."""

    def test_execution_error(self):
        """Test execution error."""
        error = ExecutionError(
            "Task failed", operator="DataExtractor", task_id="extract_users_001", retry_count=3
        )
        assert error.message == "Task failed"
        assert error.details["operator"] == "DataExtractor"
        assert error.details["task_id"] == "extract_users_001"
        assert error.details["retry_count"] == 3


class TestTimeoutError:
    """Test TimeoutError exception."""

    def test_timeout_error(self):
        """Test timeout error."""
        error = TimeoutError(
            "Operation timed out", timeout=30, elapsed=35.5, operator="SlowOperator"
        )
        assert error.message == "Operation timed out"
        assert error.details["timeout"] == 30
        assert error.details["elapsed"] == 35.5
        assert error.details["operator"] == "SlowOperator"


class TestRetryError:
    """Test RetryError exception."""

    def test_retry_error(self):
        """Test retry error."""
        failures = [
            "Attempt 1: Connection refused",
            "Attempt 2: Timeout",
            "Attempt 3: Authentication failed",
        ]
        error = RetryError("All retry attempts failed", max_retries=3, failures=failures)
        assert error.message == "All retry attempts failed"
        assert error.details["max_retries"] == 3
        assert error.details["retry_count"] == 3
        assert error.details["failures"] == failures


class TestResourceError:
    """Test ResourceError exception."""

    def test_resource_error(self):
        """Test resource error."""
        error = ResourceError(
            "Resource not found", resource_type="S3Bucket", resource_id="my-data-bucket"
        )
        assert error.message == "Resource not found"
        assert error.details["resource_type"] == "S3Bucket"
        assert error.details["resource_id"] == "my-data-bucket"


class TestAuthenticationError:
    """Test AuthenticationError exception."""

    def test_authentication_error(self):
        """Test authentication error."""
        error = AuthenticationError(
            "Authentication failed", username="admin", auth_method="password", service="database"
        )
        assert error.message == "Authentication failed"
        assert error.details["username"] == "admin"
        assert error.details["auth_method"] == "password"
        assert error.details["service"] == "database"


class TestPermissionError:
    """Test PermissionError exception."""

    def test_permission_error(self):
        """Test permission error."""
        error = PermissionError(
            "Permission denied", action="write", resource="/data/sensitive.csv", user="guest"
        )
        assert error.message == "Permission denied"
        assert error.details["action"] == "write"
        assert error.details["resource"] == "/data/sensitive.csv"
        assert error.details["user"] == "guest"


class TestExceptionInheritance:
    """Test exception inheritance relationships."""

    def test_inheritance_chain(self):
        """Test that exceptions inherit properly."""
        # All custom exceptions should inherit from DataFlowError
        assert issubclass(ConfigurationError, DataFlowError)
        assert issubclass(ValidationError, DataFlowError)
        assert issubclass(ConnectionError, DataFlowError)
        assert issubclass(TransformationError, DataFlowError)
        assert issubclass(ExecutionError, DataFlowError)
        assert issubclass(ResourceError, DataFlowError)
        assert issubclass(PermissionError, DataFlowError)

        # Some exceptions have additional inheritance
        assert issubclass(TimeoutError, ExecutionError)
        assert issubclass(RetryError, ExecutionError)
        assert issubclass(AuthenticationError, ConnectionError)

        # All should inherit from Exception
        assert issubclass(DataFlowError, Exception)

    def test_exception_catching(self):
        """Test exception catching with inheritance."""
        # Should be able to catch specific exceptions
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Test")

        # Should be able to catch by parent class
        with pytest.raises(DataFlowError):
            raise ValidationError("Test")

        with pytest.raises(ExecutionError):
            raise TimeoutError("Test")

        with pytest.raises(ConnectionError):
            raise AuthenticationError("Test")

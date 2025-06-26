"""
Exception hierarchy for DataFlow Toolkit.

This module defines custom exceptions used throughout the framework
to provide clear and specific error handling.
"""

from typing import Any, Dict, Optional


class DataFlowError(Exception):
    """Base exception for all DataFlow Toolkit errors."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        """
        Initialize DataFlowError.

        Args:
            message: Error message
            details: Additional error details
            cause: Original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.cause = cause

    def __str__(self) -> str:
        """String representation of the error."""
        parts = [self.message]

        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            parts.append(f"Details: {details_str}")

        if self.cause:
            parts.append(f"Caused by: {type(self.cause).__name__}: {str(self.cause)}")

        return " | ".join(parts)


class ConfigurationError(DataFlowError):
    """Raised when there's an error in configuration."""

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_value: Any = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize ConfigurationError.

        Args:
            message: Error message
            config_key: Configuration key that caused the error
            config_value: Invalid configuration value
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if config_key:
            details["config_key"] = config_key
        if config_value is not None:
            details["config_value"] = config_value

        super().__init__(message, details=details, cause=kwargs.get("cause"))


class ValidationError(DataFlowError):
    """Raised when data validation fails."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Any = None,
        constraint: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize ValidationError.

        Args:
            message: Error message
            field: Field that failed validation
            value: Invalid value
            constraint: Constraint that was violated
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        if constraint:
            details["constraint"] = constraint

        super().__init__(message, details=details, cause=kwargs.get("cause"))


class ConnectionError(DataFlowError):
    """Raised when connection to external system fails."""

    def __init__(
        self,
        message: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        service: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize ConnectionError.

        Args:
            message: Error message
            host: Host that failed to connect
            port: Port number
            service: Service name
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if host:
            details["host"] = host
        if port:
            details["port"] = port
        if service:
            details["service"] = service

        super().__init__(message, details=details, cause=kwargs.get("cause"))


class TransformationError(DataFlowError):
    """Raised when data transformation fails."""

    def __init__(
        self,
        message: str,
        transformer: Optional[str] = None,
        input_type: Optional[str] = None,
        output_type: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize TransformationError.

        Args:
            message: Error message
            transformer: Transformer that failed
            input_type: Input data type
            output_type: Expected output data type
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if transformer:
            details["transformer"] = transformer
        if input_type:
            details["input_type"] = input_type
        if output_type:
            details["output_type"] = output_type

        super().__init__(message, details=details, cause=kwargs.get("cause"))


class ExecutionError(DataFlowError):
    """Raised when operator execution fails."""

    def __init__(
        self,
        message: str,
        operator: Optional[str] = None,
        task_id: Optional[str] = None,
        retry_count: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize ExecutionError.

        Args:
            message: Error message
            operator: Operator that failed
            task_id: Task identifier
            retry_count: Number of retries attempted
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if operator:
            details["operator"] = operator
        if task_id:
            details["task_id"] = task_id
        if retry_count is not None:
            details["retry_count"] = retry_count

        super().__init__(message, details=details, cause=kwargs.get("cause"))


class TimeoutError(ExecutionError):
    """Raised when operation times out."""

    def __init__(
        self,
        message: str,
        timeout: Optional[int] = None,
        elapsed: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize TimeoutError.

        Args:
            message: Error message
            timeout: Timeout limit in seconds
            elapsed: Elapsed time in seconds
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if timeout is not None:
            details["timeout"] = timeout
        if elapsed is not None:
            details["elapsed"] = elapsed

        super().__init__(message, **kwargs, details=details)


class RetryError(ExecutionError):
    """Raised when all retry attempts fail."""

    def __init__(
        self,
        message: str,
        max_retries: int,
        failures: Optional[list] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize RetryError.

        Args:
            message: Error message
            max_retries: Maximum retry attempts
            failures: List of failure reasons
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        details["max_retries"] = max_retries
        if failures:
            details["failures"] = failures

        super().__init__(message, retry_count=max_retries, **kwargs, details=details)


class ResourceError(DataFlowError):
    """Raised when resource allocation or access fails."""

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize ResourceError.

        Args:
            message: Error message
            resource_type: Type of resource
            resource_id: Resource identifier
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id

        super().__init__(message, details=details, cause=kwargs.get("cause"))


class AuthenticationError(ConnectionError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str,
        username: Optional[str] = None,
        auth_method: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize AuthenticationError.

        Args:
            message: Error message
            username: Username that failed authentication
            auth_method: Authentication method used
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if username:
            details["username"] = username
        if auth_method:
            details["auth_method"] = auth_method

        super().__init__(message, **kwargs, details=details)


class PermissionError(DataFlowError):
    """Raised when permission is denied."""

    def __init__(
        self,
        message: str,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize PermissionError.

        Args:
            message: Error message
            action: Action that was denied
            resource: Resource that was accessed
            user: User who was denied
            **kwargs: Additional details
        """
        details = kwargs.get("details", {})
        if action:
            details["action"] = action
        if resource:
            details["resource"] = resource
        if user:
            details["user"] = user

        super().__init__(message, details=details, cause=kwargs.get("cause"))

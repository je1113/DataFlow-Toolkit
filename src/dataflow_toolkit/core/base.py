"""
Base classes for DataFlow Toolkit.

This module provides abstract base classes and core functionality
for building data pipeline components.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, field_validator

from dataflow_toolkit.core.exceptions import ConfigurationError, DataFlowError, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseConfig(BaseModel):
    """Base configuration class for all components."""

    name: str = Field(..., description="Component name")
    description: Optional[str] = Field(None, description="Component description")
    retry_count: int = Field(default=3, ge=0, description="Number of retries")
    retry_delay: int = Field(default=60, ge=0, description="Retry delay in seconds")
    timeout: Optional[int] = Field(None, ge=0, description="Timeout in seconds")
    tags: List[str] = Field(default_factory=list, description="Component tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate component name."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Name must contain only alphanumeric characters, hyphens, and underscores"
            )
        return v.strip()

    class Config:
        """Pydantic config."""

        extra = "forbid"
        validate_assignment = True


class BaseComponent(ABC):
    """Abstract base class for all DataFlow components."""

    def __init__(self, config: BaseConfig) -> None:
        """
        Initialize base component.

        Args:
            config: Component configuration
        """
        self.config = config
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._initialized = False
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None

    @property
    def name(self) -> str:
        """Get component name."""
        return self.config.name

    @property
    def is_initialized(self) -> bool:
        """Check if component is initialized."""
        return self._initialized

    def initialize(self) -> None:
        """Initialize component."""
        if self._initialized:
            self._logger.warning(f"Component {self.name} already initialized")
            return

        self._logger.info(f"Initializing component: {self.name}")
        self._initialize()
        self._initialized = True
        self._logger.info(f"Component {self.name} initialized successfully")

    @abstractmethod
    def _initialize(self) -> None:
        """Component-specific initialization logic."""
        pass

    def cleanup(self) -> None:
        """Cleanup component resources."""
        if not self._initialized:
            return

        self._logger.info(f"Cleaning up component: {self.name}")
        self._cleanup()
        self._initialized = False
        self._logger.info(f"Component {self.name} cleaned up successfully")

    @abstractmethod
    def _cleanup(self) -> None:
        """Component-specific cleanup logic."""
        pass

    def validate(self) -> None:
        """Validate component configuration and state."""
        self._logger.debug(f"Validating component: {self.name}")
        self._validate()
        self._logger.debug(f"Component {self.name} validation passed")

    @abstractmethod
    def _validate(self) -> None:
        """Component-specific validation logic."""
        pass

    def __enter__(self) -> "BaseComponent":
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.cleanup()


class BaseOperator(BaseComponent):
    """
    Base class for all operators in DataFlow pipelines.

    Operators are the building blocks of data pipelines that perform
    specific tasks such as data extraction, transformation, or loading.
    """

    def __init__(self, config: BaseConfig) -> None:
        """Initialize operator."""
        super().__init__(config)
        self._context: Dict[str, Any] = {}

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Execute the operator logic.

        Args:
            context: Execution context containing runtime information

        Returns:
            Result of the operation

        Raises:
            DataFlowError: If execution fails
        """
        pass

    def pre_execute(self, context: Dict[str, Any]) -> None:
        """
        Hook called before execute.

        Args:
            context: Execution context
        """
        self._context = context
        self._start_time = datetime.utcnow()
        self._logger.info(f"Starting execution of operator: {self.name}")

    def post_execute(self, result: Any) -> Any:
        """
        Hook called after successful execute.

        Args:
            result: Result from execute method

        Returns:
            Processed result
        """
        self._end_time = datetime.utcnow()
        execution_time = (self._end_time - self._start_time).total_seconds()
        self._logger.info(
            f"Operator {self.name} executed successfully in {execution_time:.2f} seconds"
        )
        return result

    def on_failure(self, error: Exception) -> None:
        """
        Hook called when execute fails.

        Args:
            error: Exception that caused the failure
        """
        self._end_time = datetime.utcnow()
        self._logger.error(f"Operator {self.name} failed: {str(error)}")

    def run(self, context: Dict[str, Any]) -> Any:
        """
        Run the operator with pre/post hooks.

        Args:
            context: Execution context

        Returns:
            Result of the operation

        Raises:
            DataFlowError: If execution fails
        """
        try:
            self.pre_execute(context)
            result = self.execute(context)
            return self.post_execute(result)
        except Exception as e:
            self.on_failure(e)
            raise DataFlowError(f"Operator {self.name} execution failed") from e


class BaseConnector(BaseComponent):
    """
    Base class for all data connectors.

    Connectors handle connections to external data sources and sinks,
    providing methods for reading and writing data.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source/sink."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the data source/sink."""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test if connection is valid and working.

        Returns:
            True if connection is valid, False otherwise
        """
        pass

    def _initialize(self) -> None:
        """Initialize connector by establishing connection."""
        self.connect()

    def _cleanup(self) -> None:
        """Cleanup connector by closing connection."""
        self.disconnect()

    def _validate(self) -> None:
        """Validate connector by testing connection."""
        if not self.test_connection():
            raise ValidationError(f"Connection test failed for {self.name}")


class BaseTransformer(BaseOperator):
    """
    Base class for data transformers.

    Transformers are specialized operators that transform data
    from one format or structure to another.
    """

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        Transform input data.

        Args:
            data: Input data to transform

        Returns:
            Transformed data

        Raises:
            DataFlowError: If transformation fails
        """
        pass

    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Execute transformer by calling transform method.

        Args:
            context: Execution context containing 'data' key

        Returns:
            Transformed data
        """
        if "data" not in context:
            raise DataFlowError("No 'data' found in context")

        return self.transform(context["data"])


class BaseValidator(BaseComponent):
    """
    Base class for data validators.

    Validators check data quality and integrity according to
    defined rules and constraints.
    """

    @abstractmethod
    def validate_data(self, data: Any) -> bool:
        """
        Validate input data.

        Args:
            data: Data to validate

        Returns:
            True if data is valid, False otherwise
        """
        pass

    @abstractmethod
    def get_validation_errors(self, data: Any) -> List[str]:
        """
        Get detailed validation errors.

        Args:
            data: Data to validate

        Returns:
            List of validation error messages
        """
        pass

    def _initialize(self) -> None:
        """Initialize validator."""
        pass

    def _cleanup(self) -> None:
        """Cleanup validator."""
        pass

    def _validate(self) -> None:
        """Validate validator configuration."""
        pass

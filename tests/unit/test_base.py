"""Unit tests for base classes."""

from typing import Any, Dict, List

import pytest

from dataflow_toolkit.core.base import (
    BaseComponent,
    BaseConfig,
    BaseConnector,
    BaseOperator,
    BaseTransformer,
    BaseValidator,
)
from dataflow_toolkit.core.exceptions import ConfigurationError, DataFlowError, ValidationError


class TestBaseConfig:
    """Test BaseConfig class."""

    def test_valid_config(self):
        """Test creating valid configuration."""
        config = BaseConfig(
            name="test_component",
            description="Test component",
            retry_count=5,
            retry_delay=30,
            timeout=300,
            tags=["test", "unit"],
            metadata={"version": "1.0"},
        )

        assert config.name == "test_component"
        assert config.description == "Test component"
        assert config.retry_count == 5
        assert config.retry_delay == 30
        assert config.timeout == 300
        assert config.tags == ["test", "unit"]
        assert config.metadata == {"version": "1.0"}

    def test_minimal_config(self):
        """Test creating minimal configuration."""
        config = BaseConfig(name="minimal")

        assert config.name == "minimal"
        assert config.description is None
        assert config.retry_count == 3
        assert config.retry_delay == 60
        assert config.timeout is None
        assert config.tags == []
        assert config.metadata == {}

    def test_invalid_name(self):
        """Test invalid component names."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            BaseConfig(name="")

        with pytest.raises(ValueError, match="Name cannot be empty"):
            BaseConfig(name="   ")

        with pytest.raises(ValueError, match="Name must contain only"):
            BaseConfig(name="test@component")

    def test_invalid_retry_count(self):
        """Test invalid retry count."""
        with pytest.raises(ValueError):
            BaseConfig(name="test", retry_count=-1)

    def test_invalid_timeout(self):
        """Test invalid timeout."""
        with pytest.raises(ValueError):
            BaseConfig(name="test", timeout=-1)


class ConcreteComponent(BaseComponent):
    """Concrete implementation for testing."""

    def _initialize(self) -> None:
        """Initialize component."""
        self.initialized_data = "initialized"

    def _cleanup(self) -> None:
        """Cleanup component."""
        self.initialized_data = None

    def _validate(self) -> None:
        """Validate component."""
        if not self.config.name:
            raise ValidationError("Name is required")


class TestBaseComponent:
    """Test BaseComponent class."""

    def test_component_lifecycle(self):
        """Test component initialization and cleanup."""
        config = BaseConfig(name="test_component")
        component = ConcreteComponent(config)

        assert not component.is_initialized
        assert component.name == "test_component"

        # Initialize
        component.initialize()
        assert component.is_initialized
        assert hasattr(component, "initialized_data")
        assert component.initialized_data == "initialized"

        # Double initialization should be safe
        component.initialize()
        assert component.is_initialized

        # Cleanup
        component.cleanup()
        assert not component.is_initialized
        assert component.initialized_data is None

    def test_context_manager(self):
        """Test component as context manager."""
        config = BaseConfig(name="test_component")

        with ConcreteComponent(config) as component:
            assert component.is_initialized
            assert component.initialized_data == "initialized"

        assert not component.is_initialized
        assert component.initialized_data is None

    def test_validation(self):
        """Test component validation."""
        config = BaseConfig(name="test_component")
        component = ConcreteComponent(config)

        # Should pass validation
        component.validate()


class ConcreteOperator(BaseOperator):
    """Concrete operator implementation for testing."""

    def _initialize(self) -> None:
        """Initialize operator."""
        self.init_called = True

    def _cleanup(self) -> None:
        """Cleanup operator."""
        self.cleanup_called = True

    def _validate(self) -> None:
        """Validate operator."""
        pass

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute operator logic."""
        return context.get("input", "default_result")


class TestBaseOperator:
    """Test BaseOperator class."""

    def test_operator_execution(self):
        """Test operator execution with hooks."""
        config = BaseConfig(name="test_operator")
        operator = ConcreteOperator(config)

        context = {"input": "test_data"}
        result = operator.run(context)

        assert result == "test_data"
        assert operator._start_time is not None
        assert operator._end_time is not None
        assert operator._context == context

    def test_operator_execution_failure(self):
        """Test operator execution failure."""
        config = BaseConfig(name="failing_operator")

        class FailingOperator(ConcreteOperator):
            def execute(self, context: Dict[str, Any]) -> Any:
                raise ValueError("Execution failed")

        operator = FailingOperator(config)

        with pytest.raises(DataFlowError, match="execution failed"):
            operator.run({})

    def test_operator_hooks(self):
        """Test pre/post execution hooks."""
        config = BaseConfig(name="hook_operator")

        class HookOperator(ConcreteOperator):
            def __init__(self, config):
                super().__init__(config)
                self.pre_called = False
                self.post_called = False
                self.failure_called = False

            def pre_execute(self, context: Dict[str, Any]) -> None:
                super().pre_execute(context)
                self.pre_called = True

            def post_execute(self, result: Any) -> Any:
                result = super().post_execute(result)
                self.post_called = True
                return result + "_modified"

            def on_failure(self, error: Exception) -> None:
                super().on_failure(error)
                self.failure_called = True

        operator = HookOperator(config)
        result = operator.run({"input": "test"})

        assert operator.pre_called
        assert operator.post_called
        assert not operator.failure_called
        assert result == "test_modified"


class ConcreteConnector(BaseConnector):
    """Concrete connector implementation for testing."""

    def __init__(self, config):
        super().__init__(config)
        self.connected = False

    def connect(self) -> None:
        """Establish connection."""
        self.connected = True

    def disconnect(self) -> None:
        """Close connection."""
        self.connected = False

    def test_connection(self) -> bool:
        """Test connection."""
        return self.connected

    def _validate(self) -> None:
        """Validate connector."""
        super()._validate()


class TestBaseConnector:
    """Test BaseConnector class."""

    def test_connector_lifecycle(self):
        """Test connector connection lifecycle."""
        config = BaseConfig(name="test_connector")
        connector = ConcreteConnector(config)

        assert not connector.connected

        # Initialize should connect
        connector.initialize()
        assert connector.connected
        assert connector.test_connection()

        # Cleanup should disconnect
        connector.cleanup()
        assert not connector.connected
        assert not connector.test_connection()

    def test_connector_validation(self):
        """Test connector validation."""
        config = BaseConfig(name="test_connector")
        connector = ConcreteConnector(config)

        # Should fail validation when not connected
        with pytest.raises(ValidationError, match="Connection test failed"):
            connector.validate()

        # Should pass validation when connected
        connector.connect()
        connector.validate()


class ConcreteTransformer(BaseTransformer):
    """Concrete transformer implementation for testing."""

    def _initialize(self) -> None:
        """Initialize transformer."""
        pass

    def _cleanup(self) -> None:
        """Cleanup transformer."""
        pass

    def _validate(self) -> None:
        """Validate transformer."""
        pass

    def transform(self, data: Any) -> Any:
        """Transform data."""
        if isinstance(data, str):
            return data.upper()
        elif isinstance(data, list):
            return [str(item).upper() for item in data]
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")


class TestBaseTransformer:
    """Test BaseTransformer class."""

    def test_transformer_execution(self):
        """Test transformer execution."""
        config = BaseConfig(name="test_transformer")
        transformer = ConcreteTransformer(config)

        # Transform string
        result = transformer.run({"data": "hello"})
        assert result == "HELLO"

        # Transform list
        result = transformer.run({"data": ["hello", "world"]})
        assert result == ["HELLO", "WORLD"]

    def test_transformer_missing_data(self):
        """Test transformer with missing data."""
        config = BaseConfig(name="test_transformer")
        transformer = ConcreteTransformer(config)

        with pytest.raises(DataFlowError, match="No 'data' found in context"):
            transformer.run({})

    def test_transformer_error(self):
        """Test transformer error handling."""
        config = BaseConfig(name="test_transformer")
        transformer = ConcreteTransformer(config)

        with pytest.raises(DataFlowError, match="execution failed"):
            transformer.run({"data": 123})


class ConcreteValidator(BaseValidator):
    """Concrete validator implementation for testing."""

    def __init__(self, config, min_length: int = 0):
        super().__init__(config)
        self.min_length = min_length

    def validate_data(self, data: Any) -> bool:
        """Validate data."""
        if isinstance(data, str):
            return len(data) >= self.min_length
        elif isinstance(data, list):
            return all(len(str(item)) >= self.min_length for item in data)
        return False

    def get_validation_errors(self, data: Any) -> List[str]:
        """Get validation errors."""
        errors = []

        if isinstance(data, str):
            if len(data) < self.min_length:
                errors.append(f"String length {len(data)} is less than minimum {self.min_length}")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if len(str(item)) < self.min_length:
                    errors.append(f"Item {i} length is less than minimum {self.min_length}")
        else:
            errors.append(f"Unsupported data type: {type(data)}")

        return errors


class TestBaseValidator:
    """Test BaseValidator class."""

    def test_validator_string(self):
        """Test validator with string data."""
        config = BaseConfig(name="test_validator")
        validator = ConcreteValidator(config, min_length=5)

        assert validator.validate_data("hello world")
        assert not validator.validate_data("hi")

        errors = validator.get_validation_errors("hi")
        assert len(errors) == 1
        assert "less than minimum 5" in errors[0]

    def test_validator_list(self):
        """Test validator with list data."""
        config = BaseConfig(name="test_validator")
        validator = ConcreteValidator(config, min_length=3)

        assert validator.validate_data(["hello", "world"])
        assert not validator.validate_data(["hi", "world"])

        errors = validator.get_validation_errors(["hi", "world"])
        assert len(errors) == 1
        assert "Item 0" in errors[0]

    def test_validator_unsupported_type(self):
        """Test validator with unsupported data type."""
        config = BaseConfig(name="test_validator")
        validator = ConcreteValidator(config)

        assert not validator.validate_data(123)

        errors = validator.get_validation_errors(123)
        assert len(errors) == 1
        assert "Unsupported data type" in errors[0]

"""Unit tests for base classes."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from dataflow_toolkit.core.base import (
    BaseComponent,
    DataFlowBaseOperator,
    ExecutionContext,
    DataFlowException,
    ConfigurationError,
)


class TestComponent(BaseComponent):
    """Test implementation of BaseComponent."""
    
    def _validate_config(self):
        if 'required_field' not in self.config:
            raise ConfigurationError("Missing required_field")


class TestOperator(DataFlowBaseOperator):
    """Test implementation of DataFlowBaseOperator."""
    
    def process(self, context):
        return {'status': 'success', 'records': 100}
    
    def get_required_config_fields(self):
        return ['source', 'target']


class TestBaseComponent:
    """Test BaseComponent class."""
    
    def test_initialization(self):
        """Test component initialization."""
        config = {'required_field': 'value'}
        component = TestComponent(config)
        
        assert component.config == config
        assert hasattr(component, 'logger')
    
    def test_validation_error(self):
        """Test configuration validation."""
        with pytest.raises(ConfigurationError) as exc_info:
            TestComponent({})
        
        assert "Missing required_field" in str(exc_info.value)
    
    def test_error_handling(self):
        """Test error handling context manager."""
        component = TestComponent({'required_field': 'value'})
        
        # Test successful execution
        with component.error_handling():
            result = 1 + 1
        assert result == 2
        
        # Test error handling
        with pytest.raises(ValueError):
            with component.error_handling():
                raise ValueError("Test error")


class TestDataFlowBaseOperator:
    """Test DataFlowBaseOperator class."""
    
    def test_initialization(self, mock_airflow_context):
        """Test operator initialization."""
        config = {'source': 'test_source', 'target': 'test_target'}
        operator = TestOperator(
            task_id='test_task',
            config=config
        )
        
        assert operator.config == config
        assert operator.metrics_enabled is True
        assert operator.connectors == {}
    
    def test_execute(self, mock_airflow_context):
        """Test operator execution."""
        config = {'source': 'test_source', 'target': 'test_target'}
        operator = TestOperator(
            task_id='test_task',
            config=config
        )
        
        result = operator.execute(mock_airflow_context)
        
        assert result['status'] == 'success'
        assert result['records'] == 100
        assert 'execution_time' in result
        assert 'execution_context' in result
    
    def test_missing_config(self):
        """Test missing configuration fields."""
        with pytest.raises(ConfigurationError) as exc_info:
            TestOperator(
                task_id='test_task',
                config={'source': 'test'}  # missing 'target'
            )
        
        assert "Missing required config field: target" in str(exc_info.value)
    
    def test_error_during_execution(self, mock_airflow_context):
        """Test error handling during execution."""
        
        class FailingOperator(DataFlowBaseOperator):
            def process(self, context):
                raise RuntimeError("Processing failed")
        
        operator = FailingOperator(
            task_id='failing_task',
            config={}
        )
        
        with pytest.raises(RuntimeError) as exc_info:
            operator.execute(mock_airflow_context)
        
        assert "Processing failed" in str(exc_info.value)


class TestExecutionContext:
    """Test ExecutionContext dataclass."""
    
    def test_execution_context_creation(self):
        """Test ExecutionContext creation."""
        context = ExecutionContext(
            pipeline_id='test_pipeline',
            task_id='test_task',
            execution_date=datetime(2024, 1, 1),
            attempt_number=2,
            metadata={'key': 'value'}
        )
        
        assert context.pipeline_id == 'test_pipeline'
        assert context.task_id == 'test_task'
        assert context.execution_date == datetime(2024, 1, 1)
        assert context.attempt_number == 2
        assert context.metadata == {'key': 'value'}
    
    def test_execution_context_defaults(self):
        """Test ExecutionContext default values."""
        context = ExecutionContext(
            pipeline_id='test_pipeline',
            task_id='test_task',
            execution_date=datetime(2024, 1, 1)
        )
        
        assert context.attempt_number == 1
        assert context.metadata == {}

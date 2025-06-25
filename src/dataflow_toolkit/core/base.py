"""Base classes and exceptions for DataFlow Toolkit."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import logging
from dataclasses import dataclass, field
from contextlib import contextmanager
import traceback

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


@dataclass
class ExecutionContext:
    """Execution context information."""
    pipeline_id: str
    task_id: str
    execution_date: datetime
    attempt_number: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataFlowException(Exception):
    """Base exception for DataFlow framework."""
    pass


class ConfigurationError(DataFlowException):
    """Configuration related errors."""
    pass


class ConnectorError(DataFlowException):
    """Connector related errors."""
    pass


class ValidationError(DataFlowException):
    """Validation failure errors."""
    pass


class BaseComponent(ABC):
    """Base class for all components."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._validate_config()
    
    @abstractmethod
    def _validate_config(self):
        """Validate configuration."""
        pass
    
    @contextmanager
    def error_handling(self, context: Optional[ExecutionContext] = None):
        """Error handling context manager."""
        try:
            yield
        except Exception as e:
            error_details = {
                'component': self.__class__.__name__,
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traceback': traceback.format_exc()
            }
            
            if context:
                error_details.update({
                    'pipeline_id': context.pipeline_id,
                    'task_id': context.task_id,
                    'execution_date': context.execution_date.isoformat()
                })
            
            self.logger.error(f"Error in {self.__class__.__name__}: {error_details}")
            raise


class DataFlowBaseOperator(BaseOperator, BaseComponent):
    """Base operator for DataFlow framework."""
    
    template_fields = ['config']
    ui_color = '#4A90E2'
    
    @apply_defaults
    def __init__(
        self,
        config: Dict[str, Any],
        connectors: Optional[Dict[str, Any]] = None,
        error_handler: Optional[str] = None,
        metrics_enabled: bool = True,
        *args,
        **kwargs
    ):
        BaseOperator.__init__(self, *args, **kwargs)
        BaseComponent.__init__(self, config)
        
        self.connectors = connectors or {}
        self.error_handler = error_handler
        self.metrics_enabled = metrics_enabled
        self._execution_context = None
    
    def execute(self, context):
        """Airflow execute method."""
        self._execution_context = ExecutionContext(
            pipeline_id=context['dag'].dag_id,
            task_id=self.task_id,
            execution_date=context['execution_date'],
            attempt_number=context['ti'].try_number
        )
        
        with self.error_handling(self._execution_context):
            self.pre_execute(context)
            result = self.process(context)
            return self.post_execute(context, result)
    
    def pre_execute(self, context):
        """Pre-execution processing."""
        self.start_time = datetime.now()
        self.logger.info(
            f"Starting {self.task_id} "
            f"[attempt {self._execution_context.attempt_number}]"
        )
    
    @abstractmethod
    def process(self, context) -> Dict[str, Any]:
        """Main processing logic."""
        pass
    
    def post_execute(self, context, result: Dict[str, Any]) -> Dict[str, Any]:
        """Post-execution processing."""
        self.end_time = datetime.now()
        execution_time = (self.end_time - self.start_time).total_seconds()
        
        result['execution_time'] = execution_time
        result['execution_context'] = self._execution_context
        
        self.logger.info(
            f"Completed {self.task_id} in {execution_time:.2f} seconds. "
            f"Result: {result}"
        )
        
        return result
    
    def _validate_config(self):
        """Basic configuration validation."""
        required_fields = self.get_required_config_fields()
        for field in required_fields:
            if field not in self.config:
                raise ConfigurationError(f"Missing required config field: {field}")
    
    def get_required_config_fields(self) -> List[str]:
        """Required config fields (override in subclasses)."""
        return []

"""
DataFlow Toolkit - Enterprise-ready Data Pipeline Framework.

A comprehensive framework for building, managing, and monitoring
data pipelines with focus on reliability, scalability, and ease of use.
"""

__version__ = "0.1.0"

from dataflow_toolkit.core.base import (
    BaseComponent,
    BaseConfig,
    BaseConnector,
    BaseOperator,
    BaseTransformer,
    BaseValidator,
)
from dataflow_toolkit.core.exceptions import (
    ConfigurationError,
    ConnectionError,
    DataFlowError,
    ExecutionError,
    TransformationError,
    ValidationError,
)

__all__ = [
    # Version
    "__version__",
    # Base classes
    "BaseComponent",
    "BaseConfig",
    "BaseConnector",
    "BaseOperator",
    "BaseTransformer",
    "BaseValidator",
    # Common exceptions
    "DataFlowError",
    "ConfigurationError",
    "ValidationError",
    "ConnectionError",
    "TransformationError",
    "ExecutionError",
]

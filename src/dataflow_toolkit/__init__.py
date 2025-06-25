"""DataFlow Toolkit - Enterprise-ready Data Pipeline Framework.

A powerful, configuration-driven data pipeline framework built on Apache Airflow.
"""

__version__ = "0.1.0"
__author__ = "DataFlow Team"
__email__ = "team@dataflow-toolkit.org"

from dataflow_toolkit.core.base import (
    DataFlowException,
    ConfigurationError,
    ConnectorError,
    ValidationError,
)

__all__ = [
    "DataFlowException",
    "ConfigurationError", 
    "ConnectorError",
    "ValidationError",
]

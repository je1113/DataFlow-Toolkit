"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import yaml


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_pipeline_config():
    """Sample pipeline configuration for testing."""
    return {
        "pipeline": {
            "name": "test_pipeline",
            "description": "Test pipeline",
            "schedule": "@daily",
            "default_args": {"owner": "test", "retries": 1},
            "connections": {
                "test_db": {
                    "type": "postgres",
                    "config": {
                        "host": "localhost",
                        "port": 5432,
                        "database": "test",
                        "user": "test",
                        "password": "test",
                    },
                }
            },
            "tasks": [
                {
                    "id": "extract_data",
                    "type": "extract",
                    "connector": "test_db",
                    "config": {"query": "SELECT * FROM users"},
                    "outputs": ["raw_data"],
                },
                {
                    "id": "transform_data",
                    "type": "transform",
                    "inputs": ["raw_data"],
                    "config": {
                        "transformations": [
                            {
                                "type": "filter",
                                "conditions": [{"type": "is_not_null", "column": "email"}],
                            }
                        ]
                    },
                    "outputs": ["clean_data"],
                },
            ],
        }
    }


@pytest.fixture
def sample_yaml_file(temp_dir, sample_pipeline_config):
    """Create a sample YAML file for testing."""
    yaml_file = temp_dir / "test_pipeline.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(sample_pipeline_config, f)
    return yaml_file


@pytest.fixture
def mock_postgres_connection():
    """Mock PostgreSQL connection."""
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=None)
        mock_connect.return_value = mock_conn
        yield mock_conn


@pytest.fixture
def mock_airflow_context():
    """Mock Airflow execution context."""
    from datetime import datetime

    context = {
        "dag": Mock(dag_id="test_dag"),
        "task": Mock(task_id="test_task"),
        "execution_date": datetime(2024, 1, 1),
        "ds": "2024-01-01",
        "tomorrow_ds": "2024-01-02",
        "ti": Mock(try_number=1),
        "task_instance": Mock(),
    }
    return context

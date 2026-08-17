"""Secure local persistence for trusted forecasting models."""

import hashlib
import json
import os
import platform
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import joblib

from src.forecasting.base import BaseForecaster


class ModelPersistenceError(RuntimeError):
    """Raised when model persistence or loading fails."""


@dataclass(frozen=True, slots=True)
class ModelArtifact:
    """Describe one persisted forecasting model."""

    artifact_id: str
    model_path: Path
    metadata_path: Path
    sha256: str


class ModelStore:
    """
    Save and load trusted forecasting artifacts.

    Only artifacts created by the application should be loaded.
    """

    def __init__(
        self,
        base_directory: str | Path,
    ) -> None:
        """Initialize the model artifact directory."""
        self._base_directory = Path(base_directory).resolve()

        self._base_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def base_directory(self) -> Path:
        """Return the resolved model directory."""
        return self._base_directory

    @staticmethod
    def _safe_component(value: str) -> str:
        """Convert an identifier into a safe filename component."""
        if not isinstance(value, str):
            raise ModelPersistenceError("Artifact identifiers must be text.")

        cleaned = re.sub(
            r"[^A-Za-z0-9_.-]+",
            "-",
            value.strip(),
        ).strip("-._")

        if not cleaned:
            raise ModelPersistenceError("Artifact identifier cannot be empty.")

        return cleaned[:80]

    @staticmethod
    def _calculate_sha256(path: Path) -> str:
        """Calculate the SHA-256 hash of a model file."""
        digest = hashlib.sha256()

        with path.open("rb") as model_file:
            for block in iter(
                lambda: model_file.read(1024 * 1024),
                b"",
            ):
                digest.update(block)

        return digest.hexdigest()

    def save(
        self,
        model: BaseForecaster,
        sku_id: str,
        location_id: str | None = None,
    ) -> ModelArtifact:
        """
        Save a fitted forecasting model and metadata atomically.

        Args:
            model: Fitted forecasting model.
            sku_id: Product identifier.
            location_id: Optional location identifier.

        Returns:
            Information describing the saved artifact.
        """
        if not isinstance(model, BaseForecaster):
            raise ModelPersistenceError("Only BaseForecaster models can be persisted.")

        if not model.is_fitted:
            raise ModelPersistenceError(
                "The forecasting model must be fitted before persistence."
            )

        sku_component = self._safe_component(sku_id)
        location_component = (
            self._safe_component(location_id)
            if location_id is not None
            else "all-locations"
        )
        model_component = self._safe_component(model.model_name)

        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")

        artifact_id = (
            f"{sku_component}-{location_component}-"
            f"{model_component}-{timestamp}-"
            f"{uuid4().hex[:8]}"
        )

        model_path = self._base_directory / f"{artifact_id}.joblib"
        metadata_path = self._base_directory / f"{artifact_id}.json"

        temporary_model_path = model_path.with_suffix(".joblib.tmp")
        temporary_metadata_path = metadata_path.with_suffix(".json.tmp")

        try:
            joblib.dump(
                model,
                temporary_model_path,
                compress=3,
            )

            os.replace(
                temporary_model_path,
                model_path,
            )

            checksum = self._calculate_sha256(model_path)

            metadata: dict[str, Any] = {
                "artifact_id": artifact_id,
                "model_name": model.model_name,
                "sku_id": sku_id,
                "location_id": location_id,
                "created_at": datetime.now(UTC).isoformat(),
                "sha256": checksum,
                "model_file": model_path.name,
                "python_version": platform.python_version(),
            }

            temporary_metadata_path.write_text(
                json.dumps(
                    metadata,
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )

            os.replace(
                temporary_metadata_path,
                metadata_path,
            )

        except (
            OSError,
            TypeError,
            ValueError,
        ) as exc:
            temporary_model_path.unlink(missing_ok=True)
            temporary_metadata_path.unlink(missing_ok=True)
            model_path.unlink(missing_ok=True)
            metadata_path.unlink(missing_ok=True)

            raise ModelPersistenceError(
                f"Unable to save model artifact: {exc}"
            ) from exc

        return ModelArtifact(
            artifact_id=artifact_id,
            model_path=model_path,
            metadata_path=metadata_path,
            sha256=checksum,
        )

    def _resolve_artifact_paths(
        self,
        artifact_id: str,
    ) -> tuple[Path, Path]:
        """Resolve safe model and metadata paths."""
        safe_id = self._safe_component(artifact_id)

        if safe_id != artifact_id:
            raise ModelPersistenceError("Invalid model artifact identifier.")

        return (
            self._base_directory / f"{safe_id}.joblib",
            self._base_directory / f"{safe_id}.json",
        )

    def get_metadata(
        self,
        artifact_id: str,
    ) -> dict[str, Any]:
        """Read metadata for one persisted model."""
        _, metadata_path = self._resolve_artifact_paths(artifact_id)

        if not metadata_path.is_file():
            raise ModelPersistenceError("Model artifact metadata was not found.")

        try:
            raw_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (
            OSError,
            json.JSONDecodeError,
        ) as exc:
            raise ModelPersistenceError(
                "Unable to read model artifact metadata."
            ) from exc

        if not isinstance(raw_metadata, dict):
            raise ModelPersistenceError("Model artifact metadata is invalid.")

        return {str(key): value for key, value in raw_metadata.items()}

    def load(
        self,
        artifact_id: str,
    ) -> BaseForecaster:
        """
        Load and validate a trusted forecasting artifact.

        Never use this method for files from untrusted sources.
        """
        model_path, _ = self._resolve_artifact_paths(artifact_id)

        if not model_path.is_file():
            raise ModelPersistenceError("Model artifact was not found.")

        metadata = self.get_metadata(artifact_id)

        expected_checksum = metadata.get("sha256")

        actual_checksum = self._calculate_sha256(model_path)

        if expected_checksum != actual_checksum:
            raise ModelPersistenceError("Model artifact checksum validation failed.")

        try:
            loaded_model = joblib.load(model_path)
        except Exception as exc:
            raise ModelPersistenceError("Unable to load model artifact.") from exc

        if not isinstance(
            loaded_model,
            BaseForecaster,
        ):
            raise ModelPersistenceError(
                "Artifact does not contain a forecasting model."
            )

        if not loaded_model.is_fitted:
            raise ModelPersistenceError("Persisted forecasting model is not fitted.")

        return loaded_model

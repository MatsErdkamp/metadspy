from __future__ import annotations
import importlib
import importlib.util
import pathlib
from typing import Any, Callable, Dict, Union, Optional
import os

from pydantic import BaseModel, Field, model_validator
import dspy


def _load_callable(ref: str) -> Callable:
    """
    Load a Python callable given either:
      - "module.submodule:func_name"
      - "path/to/file.py::func_name"
    """
    if "::" in ref:
        path, fn = ref.split("::", 1)
        spec = importlib.util.spec_from_file_location("_tmp", pathlib.Path(path).expanduser())
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, fn)
    module_path, fn = ref.rsplit(":", 1)
    mod = importlib.import_module(module_path)
    return getattr(mod, fn)


class EmbedderSpec(BaseModel):
    name: str
    model: str
    batch_size: int = 200
    caching: bool = True
    api_key_env: Optional[str] = "OPENAI_API_KEY"
    extra: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_params(self):
        if self.batch_size <= 0:
            raise ValueError("batch_size must be > 0")
        return self

    def build(self) -> dspy.Embedder:
        # Resolve model references
        model_obj: Union[str, Callable] = (
            _load_callable(self.model) if ":" in self.model else self.model
        )

        kwargs: Dict[str, Any] = dict(
            model=model_obj,
            batch_size=self.batch_size,
            caching=self.caching,
            **self.extra,
        )

        # resolve API key from env at runtime (if set)
        if self.api_key_env and "api_key" not in kwargs:
            api_key_val = os.getenv(self.api_key_env)
            if api_key_val:
                kwargs["api_key"] = api_key_val
        
        # strip None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        return dspy.Embedder(**kwargs)

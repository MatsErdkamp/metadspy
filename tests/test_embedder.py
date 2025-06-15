import os
import numpy as np
import pytest
from metadspy.specs.embedder import EmbedderSpec

def fake_embedder(inputs, **kwargs):
    # Return a deterministic fake array with the expected shape
    return np.ones((len(inputs), 3))

def test_openai_embedder(monkeypatch):
    spec = EmbedderSpec(
        name="my_embedder",
        model="openai/text-embedding-3-small",
        batch_size=2,
        caching=True,
    )
    embedder = spec.build()

    # If no API key is set, monkeypatch the __call__ method
    if os.getenv("OPENAI_API_KEY") is None:
        monkeypatch.setattr(embedder, "__call__", fake_embedder)
    
    res = embedder(["Paris", "San Francisco"])
    assert hasattr(res, "shape") or isinstance(res, np.ndarray)
    assert res.shape[0] == 2

import os
import numpy as np
import pytest
from metadspy.specs.embedder import EmbedderSpec
import litellm

def fake_embedder(model, input, **kwargs):
    # Return a deterministic fake array with the expected shape
    return np.ones((len(input), 3))

def test_openai_embedder(monkeypatch):
    spec = EmbedderSpec(
        name="my_embedder",
        model="openai/text-embedding-3-small",
        batch_size=2,
        caching=True,
    )
    embedder = spec.build()

    if os.getenv("OPENAI_API_KEY") is None:
        # Patch litellm.embedding *everywhere* (not just this embedder)
        monkeypatch.setattr(litellm, "embedding", fake_embedder)
    
    res = embedder(["Paris", "San Francisco"])
    assert hasattr(res, "shape") or isinstance(res, np.ndarray)
    assert res.shape[0] == 2

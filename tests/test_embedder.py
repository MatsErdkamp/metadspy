import os
import pytest
from metadspy.specs.embedder import EmbedderSpec

@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API_KEY not set; skipping embedder integration test."
)
def test_openai_embedder():
    spec = EmbedderSpec(
        name="my_embedder",
        model="openai/text-embedding-3-small",
        batch_size=2,
        caching=True,
    )
    embedder = spec.build()
    res = embedder(["Paris", "San Francisco"])
    assert hasattr(res, "shape")
    assert res.shape[0] == 2

from metadspy.specs.embedder import EmbedderSpec


def test_openai_embedder(monkeypatch):

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

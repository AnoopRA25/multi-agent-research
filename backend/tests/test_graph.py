from backend.app.graph.workflow import critic_router


def test_critic_router_finishes_on_pass():
    state = {
        "critique": "VERDICT:\nPASS",
        "revision_count": 0,
    }

    assert critic_router(state) == "finish"


def test_critic_router_revises_when_needed():
    state = {
        "critique": "VERDICT:\nNEEDS_REVISION",
        "revision_count": 0,
    }

    assert critic_router(state) == "revise"


def test_critic_router_stops_after_one_revision():
    state = {
        "critique": "VERDICT:\nNEEDS_REVISION",
        "revision_count": 1,
    }

    assert critic_router(state) == "finish"
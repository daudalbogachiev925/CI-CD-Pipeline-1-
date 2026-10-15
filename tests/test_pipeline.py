from src.pipeline import Pipeline
from src.stages import Stage

def test_pipeline_runs_all_stages():
    p = Pipeline("test")
    p.add_stage(Stage("s1", lambda ctx: "ok"))
    p.add_stage(Stage("s2", lambda ctx: "ok"))
    result = p.run()
    assert result["success"] == 2
    assert result["failed"] == 0

def test_pipeline_stops_on_failure():
    def fail(ctx):
        raise RuntimeError("boom")
    p = Pipeline("test")
    p.add_stage(Stage("s1", fail))
    p.add_stage(Stage("s2", lambda ctx: "ok"))
    result = p.run()
    assert result["failed"] == 1
    assert result["success"] == 0

def test_pipeline_allow_failure():
    def fail(ctx):
        raise RuntimeError("boom")
    p = Pipeline("test")
    p.add_stage(Stage("s1", fail, allow_failure=True))
    p.add_stage(Stage("s2", lambda ctx: "ok"))
    result = p.run()
    assert result["total"] == 2

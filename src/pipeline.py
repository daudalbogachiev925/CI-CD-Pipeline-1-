from src.stages import Stage, StageResult, StageStatus
from datetime import datetime

class Pipeline:
    def __init__(self, name):
        self.name = name
        self.stages = []
        self.results = []
        self.context = {}

    def add_stage(self, stage: Stage):
        self.stages.append(stage)
        return self

    def run(self):
        self.results = []
        for stage in self.stages:
            print(f"[{datetime.utcnow().isoformat()}] >>> {stage.name}")
            result = stage.run(self.context)
            self.results.append(result)
            print(f"[{result.status.value}] {stage.name} ({result.duration:.2f}s)")
            if result.error:
                print(f"  error: {result.error}")
            if result.status == StageStatus.FAILED and not stage.allow_failure:
                print("Pipeline aborted")
                break
        return self.summary()

    def summary(self):
        return {
            "pipeline": self.name,
            "total": len(self.results),
            "success": sum(1 for r in self.results if r.status == StageStatus.SUCCESS),
            "failed": sum(1 for r in self.results if r.status == StageStatus.FAILED),
            "total_duration": round(sum(r.duration for r in self.results), 2),
            "stages": [r.__dict__ for r in self.results],
        }

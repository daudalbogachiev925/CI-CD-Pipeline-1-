from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Any

class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class StageResult:
    name: str
    status: StageStatus
    duration: float = 0.0
    output: str = ""
    error: str = ""

@dataclass
class Stage:
    name: str
    handler: Callable
    allow_failure: bool = False
    timeout: int = 600

    def run(self, context: dict) -> StageResult:
        import time
        start = time.time()
        try:
            output = self.handler(context)
            return StageResult(self.name, StageStatus.SUCCESS,
                               time.time() - start, output=str(output))
        except Exception as e:
            return StageResult(self.name, StageStatus.FAILED,
                               time.time() - start, error=str(e))

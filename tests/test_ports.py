"""Tests for core.ports ABC contracts and conformance harness."""
import pytest
from core.ports.worker_runtime import WorkerRuntime
from core.ports.work_queue import WorkQueue
from core.ports.intake import IntakeConnector
from core.ports.notifier import Notifier
from core.ports.review_bot import ReviewBot
from core.ports.merge_gate import MergeGate
from core.ports.voice_engine import VoiceEngine
from core.ports.speaker_id import SpeakerID
from core.ports.telephony import Telephony
from core.ports.conformance import ConformanceSuite


ALL_PORTS = [WorkerRuntime, WorkQueue, IntakeConnector, Notifier, ReviewBot,
             MergeGate, VoiceEngine, SpeakerID, Telephony]


@pytest.mark.parametrize("port_cls", ALL_PORTS)
def test_abc_cannot_be_instantiated(port_cls):
    with pytest.raises(TypeError):
        port_cls()


class FakeWorkQueue(WorkQueue):
    vendor = "fake"

    def file(self, title, body, labels) -> str:
        return "fake-1"

    def update(self, item_ref, **fields) -> None:
        pass

    def transition(self, item_ref, state) -> None:
        pass

    def query(self, **filters) -> list[dict]:
        return []


def test_fake_adapter_instantiates_and_passes_conformance():
    adapter = FakeWorkQueue()
    suite = ConformanceSuite()
    suite.port_cls = WorkQueue
    result = suite.run(adapter)
    assert result["passed"] is True
    assert result["port"] == "WorkQueue"
    assert result["vendor"] == "fake"

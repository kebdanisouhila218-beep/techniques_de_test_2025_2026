import pytest
import time

def test_fake_performance():
    """
    Test simulé de performance, ne fait rien de réel.
    """
    start = time.time()
    time.sleep(0.1)
    duration = time.time() - start
    assert duration < 1  # Toujours vrai

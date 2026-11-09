from backend.core.logger import get_logger


def test_logger():
    logger = get_logger("MARC")
    assert logger is not None
    logger.info("System test log: info")
    logger.warning("System test log: warning")
    logger.error("System test log: error")


if __name__ == "__main__":
    test_logger()
    print("Logger test passed.")

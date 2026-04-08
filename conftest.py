""" Pytest kan gebruik maken van de Python logging module om testresultaten te loggen. 
Dit is beter dan handmatig printen, omdat het meer flexibiliteit biedt en beter integreert met testresultaten."""
import logging

""" Deze method wordt automatisch door pytest aangeroepen om de logging configuratie in te stellen."""
def pytest_configure(config):
    """Configure logging for pytest."""
    logging.getLogger().setLevel(logging.DEBUG)

"""Deze method wordt automatisch door pytest aangeroepen na elke test om het resultaat te loggen."""
def pytest_runtest_logreport(report):
    """Log test results (pass/fail/skip) with details."""
    logger = logging.getLogger(__name__)
    
    if report.when == "call":
        if report.outcome == "passed":
            logger.info(f"✓ {report.nodeid} PASSED")
        elif report.outcome == "failed":
            logger.error(f"✗ {report.nodeid} FAILED")
            """ Log de reden van falen als er een reden beschikbaar is."""
            if report.longrepr:
                logger.error(f"  Reason: {report.longrepr}")
        elif report.outcome == "skipped":
            logger.warning(f"⊘ {report.nodeid} SKIPPED")
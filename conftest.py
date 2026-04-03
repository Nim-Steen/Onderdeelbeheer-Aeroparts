from datetime import datetime

LOG_FILE = None


def pytest_sessionstart(session):
    global LOG_FILE
    LOG_FILE = open("pytest_log/aeroparts_order_test_log.txt", "a")
    LOG_FILE.write(f"Test run at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n")
    LOG_FILE.write("________________________________________________________________________________\n")


def pytest_sessionfinish(session, exitstatus):
    global LOG_FILE
    if LOG_FILE:
        LOG_FILE.write("________________________________________________________________________________\n\n\n")
        LOG_FILE.close()
        LOG_FILE = None


def pytest_runtest_logreport(report):
   if report.when == "call":
    LOG_FILE.write(f"{report.head_line} \t {report.when} {report.outcome} \n{report.capstdout}\n")
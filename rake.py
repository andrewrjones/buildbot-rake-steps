import re
from twisted.python import log

from buildbot.status.results import SUCCESS, FAILURE, WARNINGS, SKIPPED
from buildbot.steps.shell import Test

class RakeTest(Test):
    command=["rake", "test"]

    def evaluateCommand(self, cmd):
        # Get stdio, stripping pesky newlines etc.
        lines = map(
            lambda line : line.replace('\r\n','').replace('\r','').replace('\n',''),
            self.getLog('stdio').readlines()
            )

        total = 0
        passed = 0
        failed = 0
        rc = SUCCESS
        if cmd.rc > 0:
            rc = FAILURE

        re_test_result = re.compile("^(\d+) tests, (\d+) assertions, (\d+) failures, (\d+) errors")

        mos = map(lambda line: re_test_result.search(line), lines)
        test_result_lines = [mo.groups() for mo in mos if mo]

        if test_result_lines:
            test_result_line = test_result_lines[0]

            passed = int(test_result_line[0])
            #assertions = int(test_result_line[1]) not currently used
            failed = int(test_result_line[2])
            errors = int(test_result_line[3])
            
            total = passed + failed

            if failed:
                rc = FAILURE

        warnings = 0
        if self.warningPattern:
            wre = self.warningPattern
            if isinstance(wre, str):
                wre = re.compile(wre)

            warnings = len([l for l in lines if wre.search(l)])

            if rc == SUCCESS and warnings:
                rc = WARNINGS

        self.setTestResults(total=total, failed=failed, passed=passed,
                            warnings=warnings)

        return rc

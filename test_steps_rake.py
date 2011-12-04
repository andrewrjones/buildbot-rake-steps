import rake

from twisted.trial import unittest
from buildbot.status.results import SKIPPED, SUCCESS, WARNINGS, FAILURE
from buildbot.test.util import steps, compat

class FakeLogFile:
    def __init__(self, text):
        self.text = text

    def getText(self):
        return self.text

class FakeCmd:
    def __init__(self, stdout, stderr, rc=0):
        self.logs = {'stdout': FakeLogFile(stdout),
                     'stderr': FakeLogFile(stderr)}
        self.rc = rc

class TestRakeCommandExecution(steps.BuildStepMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpBuildStep()

    def tearDown(self):
        return self.tearDownBuildStep()
        
    def test_rakePass(self):
        step = self.setupStep(rake.RakeTest())
        
        log = """(in /Users/ajones/dev/ruby/duck-duck-go)
/Users/ajones/.rvm/rubies/ruby-1.8.7-p334/bin/ruby -I"lib" "/Users/ajones/.rvm/gems/ruby-1.8.7-p334/gems/rake-0.8.7/lib/rake/rake_test_loader.rb" "test/tc_icon.rb" "test/tc_link.rb" "test/tc_live.rb" "test/tc_zero_click_info.rb" 
Loaded suite /Users/ajones/.rvm/gems/ruby-1.8.7-p334/gems/rake-0.8.7/lib/rake/rake_test_loader
Started
...........
Finished in 7.633432 seconds.

11 tests, 104 assertions, 0 failures, 0 errors"""
        step.addCompleteLog('stdio', log)

        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, SUCCESS)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 11,
            'tests-failed' : 0,
            'tests-passed' : 11,
            'tests-warnings' : 0,
        })

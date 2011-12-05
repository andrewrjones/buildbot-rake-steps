buildbot-rake-steps
===================

Buildbot build steps optimised for Rake.

Currently only 'test' is implemented

Usage
-----

Firstly, download or clone the code and put it somewhere near your buildmaster.

Then add the following (or similar):

    from rake import RakeTest

### RakeTest()

You can use this as follows:

    factory.addStep(RakeTest())

It will run the `rake test` command in the build directory. The output is then parsed to get the test results, which are then displayed in your waterfall

It is a subclass of `Test`, and takes the same arguments.

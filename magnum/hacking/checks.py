# Copyright (c) 2015 Intel, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re

"""
Guidelines for writing new hacking checks

 - Use only for Magnum specific tests. OpenStack general tests
   should be submitted to the common 'hacking' module.
 - Pick numbers in the range M3xx. Find the current test with
   the highest allocated number and then pick the next value.
   If nova has an N3xx code for that test, use the same number.
 - Keep the test method code in the source file ordered based
   on the M3xx value.
 - List the new rule in the top level HACKING.rst file
 - Add test cases for each new rule to magnum/tests/unit/test_hacking.py

"""

enforce_re = re.compile(r"@policy.enforce_wsgi*")
decorator_re = re.compile(r"@.*")
mutable_default_args = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")
asse_equal_end_with_none_re = re.compile(
    r"(.)*assertEqual\((\w|\.|\'|\"|\[|\])+, None\)")
asse_equal_start_with_none_re = re.compile(
    r"(.)*assertEqual\(None, (\w|\.|\'|\"|\[|\])+\)")
assert_equal_with_true_re = re.compile(
    r"assertEqual\(True,")
assert_equal_with_false_re = re.compile(
    r"assertEqual\(False,")
asse_equal_with_is_not_none_re = re.compile(
    r"assertEqual\(.*?\s+is+\s+not+\s+None\)$")


def check_policy_enforce_decorator(logical_line,
                                   previous_logical, blank_before,
                                   filename):
    msg = ("M301: the policy.enforce_wsgi decorator must be the "
           "first decorator on a method.")
    if (blank_before == 0 and re.match(enforce_re, logical_line)
            and re.match(decorator_re, previous_logical)):
        yield(0, msg)


def assert_equal_none(logical_line):
    """Check for assertEqual(A, None) or assertEqual(None, A) sentences

    M318
    """
    msg = ("M318: assertEqual(A, None) or assertEqual(None, A) "
           "sentences not allowed")
    res = (asse_equal_start_with_none_re.match(logical_line) or
           asse_equal_end_with_none_re.match(logical_line))
    if res:
        yield (0, msg)


def no_mutable_default_args(logical_line):
    msg = "M322: Method's default argument shouldn't be mutable!"
    if mutable_default_args.match(logical_line):
        yield (0, msg)


def assert_equal_true_or_false(logical_line):
    """Check for assertEqual(True, A) or assertEqual(False, A) sentences

    M323
    """
    res = (assert_equal_with_true_re.search(logical_line) or
           assert_equal_with_false_re.search(logical_line))
    if res:
        yield (0, "M323: assertEqual(True, A) or assertEqual(False, A) "
               "sentences not allowed")


def assert_equal_not_none(logical_line):
    """Check for assertEqual(A is not None) sentences M302"""
    msg = "M302: assertEqual(A is not None) sentences not allowed."
    res = asse_equal_with_is_not_none_re.search(logical_line)
    if res:
        yield (0, msg)


def factory(register):
    register(check_policy_enforce_decorator)
    register(no_mutable_default_args)
    register(assert_equal_none)
    register(assert_equal_true_or_false)
    register(assert_equal_not_none)

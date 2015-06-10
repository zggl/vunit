# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Lars Asplund lars.anders.asplund@gmail.com

from os.path import join, dirname
from vunit.verilog import VUnit

root = dirname(__file__)

ui = VUnit.from_argv()
lib = ui.add_library("lib")
lib.add_source_files(join(root, "*.sv"))


def configure_tb_with_parameter_config(ui):
    """
    Configure tb_with_parameter_config test bench
    """
    bench = lib.module("tb_with_parameter_config")
    tests = [bench.test("Test %i" % i) for i in range(5)]

    bench.set_parameter("set_parameter", "set-for-module")

    tests[1].add_config(parameters=dict(config_parameter="set-from-config"))

    tests[2].set_parameter("set_parameter", "set-for-test")

    tests[3].add_config(parameters=dict(set_parameter="set-for-test",
                                        config_parameter="set-from-config"))

    def post_check(output_path):
        with open(join(output_path, "post_check.txt"), "r") as fptr:
            return fptr.read() == "Test 4 was here"

    tests[4].add_config(parameters=dict(set_parameter="set-from-config",
                                        config_parameter="set-from-config"),
                        post_check=post_check)


def configure_tb_same_sim_all_pass(self):
    def post_check(output_path):
        with open(join(output_path, "post_check.txt"), "r") as fptr:
            return fptr.read() == "Test 3 was here"
    module = ui.library("lib").module("tb_same_sim_all_pass")
    module.add_config(post_check=post_check)

configure_tb_with_parameter_config(ui)
configure_tb_same_sim_all_pass(ui)
ui.main()
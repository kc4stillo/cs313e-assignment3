import unittest
from unittest.mock import patch
import sys
import io
import os
import difflib
import wordle


class TestWordle(unittest.TestCase):

    def check_diff(self, actual_output, output_file):
        """Helper function to check differences between actual output and the expected file content"""

        with open(
            os.path.join("expected_default_outputs", output_file), "r", encoding="UTF-8"
        ) as outfile:
            expected_default_output = outfile.read()

        with open(
            os.path.join("expected_high_contrast_outputs", output_file),
            "r",
            encoding="UTF-8",
        ) as outfile:
            expected_high_contrast_output = outfile.read()

        default_diff = list(
            difflib.unified_diff(
                expected_default_output.splitlines(keepends=True),
                actual_output.splitlines(keepends=True),
                fromfile="expected output",
                tofile="actual output",
                lineterm="",
            )
        )

        high_contrast_diff = list(
            difflib.unified_diff(
                expected_high_contrast_output.splitlines(keepends=True),
                actual_output.splitlines(keepends=True),
                fromfile="expected output",
                tofile="actual output",
                lineterm="",
            )
        )

        if len(default_diff) <= len(high_contrast_diff):
            diff_result = default_diff
        else:
            diff_result = high_contrast_diff

        if diff_result:
            diff_output = "\n".join(diff_result)
            self.fail(
                f"Differences found between actual output and {output_file}:\n{diff_output}"
            )

    def run_wordle_with_input(self, input_file):
        """Helper function to run wordle.py with input from a file, and capture output as a string"""
        with open(input_file, "r") as infile:
            inputs = infile.read().splitlines()
        i = 0

        # Function to mock each input call
        def input_mock(prompt=""):
            nonlocal i
            # Print or log each input as it's read from the file
            if i < len(inputs):
                current_input = inputs[i]
                print(f"{prompt}{current_input}")
                i += 1
                return current_input
            raise EOFError("EOF when reading a line")

        output_buffer = io.StringIO()
        with patch("builtins.input", input_mock), patch(
            "sys.stdout", new=output_buffer
        ):
            sys.argv = ["wordle.py"]
            sys.argv.extend(input_file.split(".in")[0].split())
            wordle.main()

        return output_buffer.getvalue()

    def run_test_case(self, test_case):
        """Helper function to handle test case execution and diff checking"""
        input_file = f"{test_case}.in"
        output_file = f"{test_case}.out"

        actual_output = self.run_wordle_with_input(input_file)
        self.check_diff(actual_output, output_file)

    def test_999(self):
        """python3 wordle.py 999 < 999.in"""
        self.run_test_case("999")

    def test_basil(self):
        """python3 wordle.py basil < basil.in"""
        self.run_test_case("basil")

    def test_brain(self):
        """python3 wordle.py brain < brain.in"""
        self.run_test_case("brain")

    def test_camel(self):
        """python3 wordle.py camel < camel.in"""
        self.run_test_case("camel")

    def test_hello_birdy(self):
        """python3 wordle.py hello birdy"""
        self.run_test_case("hello birdy")

    def test_hello(self):
        """python3 wordle.py hello < hello.in"""
        self.run_test_case("hello")

    def test_kappa(self):
        """python3 wordle.py kappa < kappa.in"""
        self.run_test_case("kappa")

    def test_lllll(self):
        """python3 wordle.py lllll < lllll.in"""
        self.run_test_case("lllll")

    def test_mello(self):
        """python3 wordle.py mello < mello.in"""
        self.run_test_case("mello")

    def test_pivot(self):
        """python3 wordle.py pivot < pivot.in"""
        self.run_test_case("pivot")

    def test_right(self):
        """python3 wordle.py right < right.in"""
        self.run_test_case("right")

    def test_riped(self):
        """python3 wordle.py riped < riped.in"""
        self.run_test_case("riped")

    def test_sleep(self):
        """python3 wordle.py sleep < sleep.in"""
        self.run_test_case("sleep")

    def test_smoge(self):
        """python3 wordle.py smoge < smoge.in"""
        self.run_test_case("smoge")

    def test_table(self):
        """python3 wordle.py table < table.in"""
        self.run_test_case("table")


def main():
    if len(sys.argv) > 1:
        test_name = "_".join(sys.argv[1:])
        # Check if the provided test name is valid
        valid_tests = [
            "999",
            "basil",
            "brain",
            "camel",
            "hello_birdy",
            "hello",
            "kappa",
            "lllll",
            "mello",
            "pivot",
            "right",
            "riped",
            "sleep",
            "smoge",
            "table",
        ]

        if test_name in valid_tests:
            loader = unittest.TestLoader()
            all_tests = loader.loadTestsFromTestCase(TestWordle)
            suite = unittest.TestSuite()

            for test in all_tests:
                if test_name == test.id().split(".")[-1][5:]:
                    suite.addTest(test)
                    break
            else:
                print(
                    f"Invalid test name: {test_name}. Please choose from {valid_tests}."
                )
            runner = unittest.TextTestRunner()
            runner.run(suite)
        else:
            print(f"Invalid test name: {test_name}. Please choose from {valid_tests}.")
    else:
        # If no argument is passed, run all tests
        unittest.main()


if __name__ == "__main__":
    main()

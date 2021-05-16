
from pseudocoder.runner import run
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('code_file', help='Pseudocode file to run')

    args = parser.parse_args()

    run(args.code_file)
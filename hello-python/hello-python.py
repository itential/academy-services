#!/usr/bin/env python3
import argparse

def main():
    # Create argument parser to receive command-line arguments from torero
    parser = argparse.ArgumentParser(description='Python hello world with two string variables')
    parser.add_argument('--first_string', type=str, default='Hello', 
                        help='First string to print')
    parser.add_argument('--second_string', type=str, default='World',
                        help='Second string to print')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Print the two strings
    print(args.first_string)
    print(args.second_string)

if __name__ == "__main__":
    main()
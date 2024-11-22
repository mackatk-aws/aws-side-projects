# S3 Incremental Cost Calculator

A Python script to calculate and project Amazon S3 storage costs over time, factoring in incremental storage growth. This tool helps you estimate costs across different regions and storage tiers, with an optional feature to export results to a CSV file.

## Script Location

The script is located in this repository:  
[`s3-incremental-calc.py`](https://github.com/mackatk-aws/aws-side-projects/blob/main/s3-incremental-calc.py)

## Features

- **Region-specific pricing:** Choose from AWS regions like `us-east-1`, `us-west-1`, and more.
- **Supports multiple S3 tiers:** Standard, Intelligent-Tiering, Glacier, and others.
- **Customizable projections:** Input initial storage size, monthly growth, and projection duration.
- **CSV Export:** Save results for further analysis.
- **User-friendly CLI:** Interactive prompts guide the user through region, tier, and storage input selection.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mackatk-aws/aws-side-projects.git
   cd aws-side-projects
Ensure you have Python installed (>=3.7).

## Install dependencies:
pip install pandas
Usage

## Run the script:

python s3-incremental-calc.py

## Follow the prompts:

Select your AWS region.
Choose a storage tier.
Specify initial storage size, monthly data increment, and projection duration in months.

## View and save results:

The tool displays a detailed monthly cost projection in the terminal.
Optionally save the results to a CSV file.

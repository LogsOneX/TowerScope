# TowerScope Operation Manual

## Overview
TowerScope is a SIGINT (Signals Intelligence) tool for BTS lookup and geospatial intelligence operations.

## Basic Usage
1. Run the application: `python src/towerscope.py`
2. Follow the interactive prompts:
   - Operation Codename
   - Operator Name
   - Country Code
   - MCC, MNC, LAC, Cell ID
   - IMSI and IMEI (optional)

## Output Files
The tool generates three types of output:
- Interactive maps (.html)
- Intelligence reports (.html)
- Data files (.csv)

All files are saved in the `output/` directory.

## Advanced Features
- Local server hosting for map access
- Batch processing capabilities
- Customizable coverage radius estimation

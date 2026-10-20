# A simulated look at campus commuting in Macau

## Question

How do hypothetical university commuters divide among travel modes, and how do the assumed average trip times compare?

## Data and permission

The six-row dataset in `commute_modes.csv` is **simulated for a course visualization exercise**. It describes a hypothetical group of 1,000 commuters. The shares and times were invented; no survey was conducted and no third-party dataset or personal information is used. The data can be reused with attribution to this project.

## Method and tools

`analyze.py` reads the CSV with Python's standard library, checks that the shares total 100%, calculates the shared-transport weighted mean, and uses Matplotlib to make two charts. `mode_share_and_time.png` aligns mode share with average trip time; `share_vs_time.png` shows the two measures in one scatter plot.

## Findings and limitation

In this assumed scenario, bus and campus shuttle account for 53% of commuters. Their weighted average one-way trip is about 25.8 minutes, compared with 12 minutes for walking. This illustrates a possible trade-off between reach and travel time. It is **not evidence about actual students or transport services**. The table omits waiting time, trip distance, cost, accessibility, and variation within each mode.

## Reproduce the analysis

1. Install Python 3.10 or newer.
2. From this folder, run `python -m pip install -r requirements.txt`.
3. Run `python analyze.py`.
4. Open the two PNG files in this folder.

The script reads only the included CSV and requires no API key or network access after installation.

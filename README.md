# **Inventory Intelligence**
## **Strategic Procurement Optimization for Engineering Equipment**


## Project Overview
This project is an end-to-end data solution designed to modernize the Supply and Logistics operations at an engineering firm. 
It transforms raw warehouse logs into an interactive Procurement Decision Support System, focusing on managing long-lead-time international imports (Japan, Europe, Australia).

## The Problem: Import Lead-Time Risk
In the water engineering sector, stockouts of critical items like Submersible Pumps or Solar Inverters can halt multi-million dollar projects.
- **Manual Tracking:** Traditional methods fail to account for demand volatility.
- **Import Delays:** Standard lead times of 45–120 days for international sourcing require advanced predictive ordering.
- **Capital Lock:** Overstocking low-value items ties up cash that should be used for "A-Class" high-revenue products.

## The Solution: Statistical Inventory Modeling
I engineered a three-phase analytical pipeline to automate the Local and Import Purchase Process:
- **Demand Forecasting:** Modeled 365 days of sales using a Poisson Distribution, accounting for Ethiopia's dry-season demand spikes (Oct–May).
- **ABC Classification:** Categorized 15 core SKUs to prioritize management of the 70% of capital tied up in "A-Class" items.
- **Safety Stock Math:** Applied the Square Root Law of Inventory using a 95% Service Level ($Z=1.645$) to calculate precise Reorder Points (ROP).
- **Operational Dashboard:** Developed a Streamlit Control Tower that identifies "Days of Cover" to prevent stockouts before they happen.

## Key Findings & Results Based on the latest run of the intelligence engine:
- **Current Health Summary:**  REORDER NOW: 13 SKUs (87% of portfolio), **HEALTHY:** 2 SKUs
- **Critical Bottlenecks:** 100% of current reorder needs are International Imports, representing a massive coordination task for bank documentation and customs clearance.

**Top Priority Items:** **Solar Pumps (Europe):** 120-day lead time; only 15 units remaining against a 195-unit ROP. 50kVA Generators (Australia): 118-day lead time; currently at 12 units (Critical Risk).

## Tech Stack
- **Python:** Core analytical engine (Pandas, NumPy, Scipy).
- **Plotly:** Interactive risk matrices and financial allocation charts.
- **Streamlit:** UI for the Executive Procurement Dashboard.

## **Professional Recommendations**

1. **Immediate Procurement:** Initiate L/C (Letter of Credit) applications for the 13 flagged international SKUs immediately to account for the 3-month average lead time.
2. **Strategic Sourcing:** For "A-Class" items like UV Sterilizers, investigate local buffering or air-freight options to reduce the 82-day Japan-to-Addis delay.
3. **Safety Stock Review:** Maintain the 95% service level for Pumps/Generators, but consider lowering the level for "C-Class" items to free up operational cash flow.

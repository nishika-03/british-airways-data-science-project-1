"""Build the lounge eligibility lookup table (Task 1).

Groups every flight by haul type and time of day, then calculates
Tier 1/2/3 eligibility as total eligible passengers / total seats.
Run from this folder:  python src/build_lookup_table.py
"""
import pandas as pd

df = pd.read_excel("data/british_airways_summer_schedule.xlsx")
df["TOTAL_SEATS"] = df[["FIRST_CLASS_SEATS", "BUSINESS_CLASS_SEATS", "ECONOMY_SEATS"]].sum(axis=1)

grouped = df.groupby(["HAUL", "TIME_OF_DAY"]).agg(
    flights=("FLIGHT_NO", "count"),
    total_seats=("TOTAL_SEATS", "sum"),
    tier1_pax=("TIER1_ELIGIBLE_PAX", "sum"),
    tier2_pax=("TIER2_ELIGIBLE_PAX", "sum"),
    tier3_pax=("TIER3_ELIGIBLE_PAX", "sum"),
)
for t in (1, 2, 3):
    grouped[f"tier{t}_pct"] = (grouped[f"tier{t}_pax"] / grouped["total_seats"] * 100).round(2)

print(grouped[["flights", "tier1_pct", "tier2_pct", "tier3_pct"]])
grouped.to_csv("output/lookup_table_calculated.csv")

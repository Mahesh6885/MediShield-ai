# MediShield AI: Hospital Materials Management & Inventory SOP
Source: MediShield AI Clinical Supply Chain Operating Protocol
Document ID: DOC-SOP-004

## Section 1: Standard Reorder Point and EOQ Policy
1. Reorder Point (ROP): Defined mathematically as ROP = (Demand / 30) * Lead_Time + Safety_Stock. Reorder triggers occur automatically when physical stock plus on-order shipments fall below ROP.
2. Economic Order Quantity (EOQ): Computed as EOQ = sqrt(2 * D * S / H), with default ordering transaction cost S = $200 and holding cost H = $15 per unit-year.
3. Expiry Protocol: Any batch within 60 days of labeled expiration date triggers an automated priority dispensing or vendor return flag.

## Section 2: Supplier Evaluation and Multi-Criteria Ranking
Supplier performance is dynamically audited across four direction-aware dimensions:
1. Reliability (35% weight): Fulfillment completeness rate (higher is better).
2. Quality Score (30% weight): Percentage of delivered lots meeting batch assay specifications without quality defect notices (higher is better).
3. Procurement Cost (20% weight): Unit acquisition price normalized against category peer averages (lower is better).
4. Delivery Time (15% weight): Replenishment transit lead time in calendar days (lower is better).

## Section 3: Shortage Risk Categorization and Response Actions
The AI shortage prediction model classifies medicines into three actionable tiers:
1. High Risk (Predicted Probability >= 75%): Expedited procurement notice, secondary supplier activation, clinical lead review within 24 hours.
2. Medium Risk (Predicted Probability 45% to 74%): Weekly monitoring cadence, buffer stock safety margin verification.
3. Low Risk (Predicted Probability < 45%): Routine automated replenishment according to standard EOQ cadence.

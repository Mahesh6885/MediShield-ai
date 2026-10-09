# MediShield AI: Domain Feature Engineering Specification
**Generated:** 2026-10-06T14:30:26.239021+00:00  
**Input Features:** 6 Raw Attributes  
**Engineered Features:** 5 Domain Supply-Chain Indicators  
**Total Dimension:** 11 Features  

---

## 1. Feature Formulations

| Feature Name | Formula | Unit | Expected Operational Role |
| :--- | :--- | :--- | :--- |
| `stock_cover_ratio` | `inventory / (demand + epsilon)` | months of supply | Negative: higher stock cover lowers shortage risk. |
| `safety_buffer_margin` | `(inventory - safety_stock) / (demand + epsilon)` | ratio | Negative: higher safety margin lowers shortage risk. |
| `lead_time_demand` | `(demand / 30) * lead_time` | units | Positive: higher consumption during lead time increases vulnerability. |
| `reorder_deficit` | `((demand / 30) * lead_time + safety_stock) - inventory` | units | Positive: positive deficit indicates immediate need to reorder. |
| `supplier_delay_exposure` | `(100 - supplier_reliability) * lead_time` | risk days | Positive: higher delay exposure increases stockout hazard. |

---

## 2. Numerical Stability Protection
- **Epsilon Constant:** $\epsilon = 10^{-5}$ is included in the denominators of `stock_cover_ratio` and `safety_buffer_margin` to strictly prevent zero-division errors when demand is zero.
- **Target Independence:** No label or target variable information is utilized in computing these features, preventing target leakage.

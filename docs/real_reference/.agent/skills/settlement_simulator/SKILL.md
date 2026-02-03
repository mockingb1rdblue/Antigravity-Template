---
name: Settlement Simulator
description: Simulates mediation outcomes from opposing counsel's perspective to optimize settlement strategy
---

# Settlement Simulator

This skill runs comprehensive settlement scenario analysis from the perspective of experienced defense counsel (West Point law grad, expert at shutdowns) who initially views the case as "simple."

## Purpose

The simulator:
1. Models opposing counsel's evolving assessment as they review evidence
2. Calculates settlement probability ranges for each component
3. Identifies leverage points and vulnerability exposures
4. Provides strategic recommendations for optimizing favorable outcomes

## Usage

```bash
python .agent/skills/settlement_simulator/simulate.py
```

The script will:
- Parse the pre-mediation package and war room materials
- Run Monte Carlo simulation across multiple negotiation scenarios
- Output detailed analysis with settlement probability distributions
- Generate strategic recommendations

## Outputs

- **Settlement Scenarios**: Probability-weighted outcomes for each component
- **Defense Counsel Psychology**: How perception shifts as evidence is reviewed
- **Leverage Analysis**: Critical pressure points and failure risks
- **Tactical Recommendations**: Optimal negotiation sequencing and fallback positions

## Model Parameters

The simulator uses:
- **Initial Assessment**: Defense counsel starts at 10-20% of demand (typical shutdown mindset)
- **Evidence Weight Factors**: Quantifies impact of each exhibit on settlement range
- **Risk Multipliers**: Models litigation cost aversion and reputational damage
- **Component Interdependencies**: Accounts for bundling vs. unbundling strategies

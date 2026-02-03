# Skill: GURPS Mechanics & Tactical Combat

This skill captures the engine's deterministic implementation of GURPS 4e rules and tactical state management.

## Success Resolution Pattern
- **Logic**: Use `RulesLookup.checkSuccess(roll, effectiveSkill)` for all mechanical checks.
- **Criticals**: 
    - 3-4 = Critical Success. 18 = Critical Failure.
    - Effective Skill 15+ -> 5 is Critical Success.
    - Effective Skill 16+ -> 6 is Critical Success.
    - Roll >= Skill+10 -> Critical Failure.
- **Code**: [rules-lookup.ts](file:///Users/mock1ng/Documents/Projects/Antigravity-Github/CarPiggy/src/services/rules-lookup.ts)

## Tactical Combat State
- **FSM**: Combat is a persistent state machine stored in `WorldState.combat`.
- **Initiative**: Determined by `Basic Speed = (DX + HT) / 4`.
- **Maneuvers**: The `Referee` must parse maneuvers (Attack, Aim, Defend) and update `hpCurrent` or `maneuver` status.
- **Wounds**: 
    - Major Wound = single hit > HP/2.
    - Knockout/Death = HP <= 0.
- **Code**: [combat-manager.ts](file:///Users/mock1ng/Documents/Projects/Antigravity-Github/CarPiggy/src/services/combat-manager.ts)

## Scaling & Constraints
- **Pattern**: Always ground the LLM `Referee` with `RulesLookup` data to prevent "mechanical hallucination".
- **D1 Limits**: Always use `WriteBuffer` for high-frequency progression updates to avoid D1 batch limits.

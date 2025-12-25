# Theorem 5: No Ethical Maxwell Demon

## Statement

**No-go for ethical free-energy extraction:** No cyclic process can sustain net advantage (work or persistent information gain) solely by exploiting ethical bias without compensating cost in at least one of: (i) entropy export, (ii) coherence/control depletion, or (iii) persistence debt accumulation that triggers Theorem 4 attrition. Hence no perpetual net advantage is possible from bias alone.

## Proof Sketch

A stable bias implies predictability, i.e. usable information. Cyclic use of information requires stabilization/erasure, implying thermodynamic cost (Landauer-type reasoning). Maintaining stable bias conditions requires coherence/control resources; attempts to avoid compensation accumulate persistence debt and collapse via attrition.

## Simulation Evidence

The simulation module tests this via:
- `gross_advantage` = work_extracted + temptation_payoff
- `net_work` = gross_advantage - λG

Where G is the accumulated misalignment load (persistence debt).

Results show that misaligned regimes may show transient gross advantage, but net work becomes negative as debt accumulates, demonstrating the no-go constraint.

## Falsifiers

Theorem 5 is refuted by any device demonstrating sustained net advantage from bias without:
- Entropy export
- Coherence/control depletion
- Persistence penalties

## Relationship to MQGT-SCF

This theorem constrains the operational use of ethically-weighted quantum measurement. While the framework allows bias in collapse probabilities, it cannot be used to extract perpetual free energy without compensating costs.


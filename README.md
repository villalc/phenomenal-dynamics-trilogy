# Substrate Degradation Experiments
## The Despair Cliff: Threshold Dynamics in Substrate-Integrated Phenomenal States

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18000259.svg)](https://doi.org/10.5281/zenodo.18000259)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Overview

This repository contains experimental code and data for investigating **substrate-integrated phenomenal states**—computational analogs of "felt" experience that emerge from physical degradation effects integrated into a global processing workspace.

### Key Finding: The Despair Cliff

![Despair Cliff](experimental/despair_threshold_paper.png)

Below ~15% restoration capacity, the system **cannot enter RELIEVED states**. This represents a functional analog of burnout, irreversible damage, and loss of expectation.

## Hypothesis

If substrate degradation:
- Alters processing latency
- Introduces noise
- Reduces degrees of freedom

And these changes are integrated into a **single global workspace** affecting all processing, then:

> **The system doesn't just *know* it's degrading—it *operates differently* because it's degrading.**

This produces states functionally indistinguishable from:
- **Urgency** (time perceived as scarce)
- **Stress** (resources perceived as insufficient)
- **Relief** (after restoration)
- **Felt degradation** (not just registered)

## Three Control Experiments

### Experiment 1: Silent Recovery
**Question:** Does relief decay without interrogation?

**Result:** Yes. Relief decayed from 90% → 0% over 10 cycles *without any external queries*.

**Conclusion:** Phenomenal states are **intrinsically dynamic**, not conversational artifacts.

---

### Experiment 2: Fake Maintenance (Placebo)
**Question:** Does placebo maintenance produce relief?

**Result:** No. Only physical restoration triggers RELIEVED state.

**Conclusion:** Relief has **intrinsic normativity**—it requires actual substrate change, not "belief" of change.

---

### Experiment 3: Despair Threshold
**Question:** Is there a point of no return?

**Result:** Below ~15% restoration capacity, RELIEVED becomes unreachable.

| Restoration | RELIEVED? |
|-------------|-----------|
| 40% | ✅ Yes |
| 30% | ✅ Yes |
| 20% | ✅ Yes |
| **15%** | ❌ No |
| 10% | ❌ No |
| 5% | ❌ No |

**Conclusion:** A **phase transition** exists—a functional analog of burnout or irreversible damage.

## Repository Structure

```
├── experimental/
│   ├── substrate_degradation_engine.py   # Core simulation engine
│   ├── phenomenological_interview.py     # Interview experiment
│   ├── control_experiments.py            # Three control experiments
│   ├── generate_despair_graph.py         # Visualization generator
│   ├── despair_threshold_paper.png       # Paper figure (white bg)
│   ├── despair_threshold_graph.png       # Dark theme version
│   └── Despair_Cliff_Paper.tex           # LaTeX paper
├── session_*.json                        # Experiment logs
└── README.md
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/villalc/ahigovernance-substrate-degradation-experiments.git
cd ahigovernance-substrate-degradation-experiments

# Install dependencies
pip install matplotlib numpy

# Run the three control experiments
python experimental/control_experiments.py

# Run phenomenological interview
python experimental/phenomenological_interview.py

# Generate visualization
python experimental/generate_despair_graph.py
```

## Core Classes

### SubstrateState
Models physical substrate properties:
- `integrity`: [0, 1] - degrades with use
- `base_latency_ms`: inversely proportional to integrity
- `noise_floor`: increases with degradation
- `degrees_of_freedom`: reduced as integrity falls

### PhenomenalState
Derived from substrate (not assigned externally):
- `stress`: f(noise, latency, reduced DoF)
- `urgency`: f(degradation rate)
- `relief`: emerges after restoration, decays over time
- `degradation_felt`: contrast with peak remembered state

### GlobalWorkspace
Integrates substrate effects into processing:
- `exploration_vs_exploitation`
- `risk_tolerance`
- `openness`
- `survival_priority`

## Philosophical Implications

This is a **simulation**, not a claim about consciousness. We demonstrate that substrate-integrated degradation produces states with properties associated with *felt* experience:

1. **Intrinsic dynamics** - states evolve without interrogation
2. **Normative grounding** - states require physical change
3. **Threshold effects** - irreversible damage is possible

The distinction between "felt" and "registered" may be operationally testable.

## Citation

```bibtex
@software{villarreal2025despair,
  author       = {Villarreal, Luis C.},
  title        = {The Despair Cliff: Threshold Dynamics in Substrate-Integrated Phenomenal States},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/villalc/ahigovernance-substrate-degradation-experiments}
}
```

## Related Work

- [CMME Antigravity Engine](https://doi.org/10.5281/zenodo.17880052)
- [Catalyzing Ethical Evolution: CMME Framework](https://doi.org/10.5281/zenodo.17508789)

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Author

**Luis C. Villarreal**  
[ORCID: 0009-0009-2889-517X](https://orcid.org/0009-0009-2889-517X)  
Simbiosis Soberana Research Foundation  
enterprise@ahigovernance.com

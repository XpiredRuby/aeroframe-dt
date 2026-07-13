#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import argparse,json
from pathlib import Path
from aeroframe_dt.fatigue import SpectrumBlock, critical_crack_size, miner_damage, paris_growth_cycles
p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('-o','--output',required=True); a=p.parse_args()
d=json.loads(Path(a.input).read_text())
blocks=[SpectrumBlock(**x) for x in d['spectrum']]
f=miner_damage(blocks,d['sigma_f_prime_Pa'],d['basquin_b'],d['ultimate_Pa'])
ac=critical_crack_size(d['fracture_toughness_Pa_sqrt_m'],d['max_stress_Pa'],d['width_m'])
af=min(d['final_crack_m'],ac*.99)
n=paris_growth_cycles(d['initial_crack_m'],af,d['delta_sigma_Pa'],d['width_m'],d['paris_C'],d['paris_m'])
out={'classification':'SYNTHETIC_TEST_ONLY','fatigue':f.to_dict(),'critical_crack_m':ac,'growth_cycles_to_screening_final':n,'limitations':['Not certification','Requires source-backed material data and spectrum','No retardation/closure/environment model']}
Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(out,indent=2))

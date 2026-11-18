"""Append-only: add the three sales personas to data/personas/index.json (W3-CRM). Safe to rerun."""
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else 'data/personas/index.json'
d = json.load(open(p))
SALES = [
    {"id": "sal_priya_malhotra", "role": "sales", "name": "Priya Malhotra", "story": "Sales manager. Owns the funnel, targets and the rep leaderboard.", "order": 1},
    {"id": "sal_aman_gupta", "role": "sales", "name": "Aman Gupta", "story": "Counselling sales rep. Zoya Fernandes' family is waiting to pay today.", "order": 2},
    {"id": "sal_neha_joseph", "role": "sales", "name": "Neha Joseph", "story": "Counselling sales rep for referrals, ads and school partnerships.", "order": 3},
]
ids = {i["id"] for i in d["items"]}
added = [s for s in SALES if s["id"] not in ids]
d["items"].extend(added)
open(p, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
print('added', len(added))

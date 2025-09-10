def compute_confidence(evidence):
    score = 0.0
    if evidence.get('nvd_exact_match'): score += 0.5
    if evidence.get('exploitdb'): score += 0.2
    if evidence.get('secondary_confirm'): score += 0.15
    if evidence.get('llm_consensus'): score += 0.1
    return min(1.0, score)

import json
import re
from core.console import console

def correlate_identities(all_results: dict, initial_target: str):
    """
    Cross-references findings from all modules to identify linked identities.
    Returns a list of correlations with confidence scores.
    """
    correlations = []
    entities = []

    # 1. Flatten all findings into a list of entities with attributes
    # Username findings
    platform_results = all_results.get("platforms", {})
    for platform, data in platform_results.items():
        if isinstance(data, dict) and data.get("status") == "found":
            entities.append({
                "type": "social_profile",
                "label": f"{platform} Profile",
                "id": data.get("url"),
                "username": initial_target if "@" not in initial_target else None,
                "bio": data.get("extracted_bio", ""),
                "source": platform
            })

    # Email findings (from auto-pivot or direct scan)
    for key, data in all_results.items():
        if "email" in key.lower() or "breach" in key.lower() or "@" in key:
            # Try to extract the email from the key or data
            email = None
            if "@" in key:
                parts = key.split("_")
                for p in parts:
                    if "@" in p:
                        email = p
                        break
            
            if email:
                entities.append({
                    "type": "email_identity",
                    "label": f"Email: {email}",
                    "id": str(email),
                    "data": str(data),
                    "source": "email_intel"
                })

    # 2. Scoring Loop
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            e1 = entities[i]
            e2 = entities[j]
            
            score = 0
            reasons = []
            
            # Rule: Same Bio
            bio1 = e1.get("bio", "")
            bio2 = e2.get("bio", "")
            if bio1 and bio2 and bio1 != "No description available":
                if bio1 == bio2:
                    score += 70
                    reasons.append("Exact bio matching")
                else:
                    # Partial match
                    words1 = set(bio1.lower().split())
                    words2 = set(bio2.lower().split())
                    overlap = words1.intersection(words2)
                    if len(overlap) > 10:
                        score += 40
                        reasons.append("Strong bio keyword overlap")

            # Rule: Email found in profile bio
            id1 = str(e1.get("id", "")).lower()
            id2 = str(e2.get("id", "")).lower()

            if e1["type"] == "social_profile" and e2["type"] == "email_identity":
                if id2 and id2 in bio1.lower():
                    score += 90
                    reasons.append(f"Email {id2} explicitly mentioned in bio")
            elif e2["type"] == "social_profile" and e1["type"] == "email_identity":
                if id1 and id1 in bio2.lower():
                    score += 90
                    reasons.append(f"Email {id1} explicitly mentioned in bio")

            # Rule: Common username
            if e1.get("username") and e2.get("username") and e1["username"] == e2["username"]:
                score += 20
                reasons.append("Shared username across platforms")

            if score > 0:
                correlations.append({
                    "entity_a": e1["label"],
                    "entity_b": e2["label"],
                    "score": min(score, 100),
                    "reasons": reasons
                })

    return correlations

def display_correlations(correlations):
    if not correlations:
        return

    console.print("\n[bold gold1]🧠 OmniCorrelator Identity Analysis[/bold gold1]")
    for c in sorted(correlations, key=lambda x: x['score'], reverse=True):
        color = "green" if c['score'] > 70 else "yellow" if c['score'] > 40 else "white"
        console.print(f"  [bold {color}]▶ {c['score']}% Confidence[/bold {color}]")
        console.print(f"    [dim]{c['entity_a']} ↔ {c['entity_b']}[/dim]")
        for reason in c['reasons']:
            console.print(f"    [blue]↳ {reason}[/blue]")

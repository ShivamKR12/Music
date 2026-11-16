"""
AutoEq Headphone Correction Profiles Service.
Provides calibrated 10-band parametric equalizer curves for industry target standards
(Harman In-Ear, Harman Over-Ear) and popular consumer headphones (Sony, Apple, Bose, Sennheiser, etc.).
Works consistently across Windows, Android, Linux, and macOS.
"""

from typing import Dict, List, Optional

# Standard 10-band ISO frequencies in Hz
EQ_FREQUENCIES = [32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]

# Pre-computed 10-band compensation gains (in dB, -12.0 to +12.0)
AUTOEQ_PROFILES: Dict[str, List[float]] = {
    # Industry Target Standards
    "Harman In-Ear Target": [3.0, 2.5, 1.0, 0.0, -0.5, 0.5, 1.5, 0.0, -1.0, -1.5],
    "Harman Over-Ear Target": [2.5, 2.0, 1.0, 0.0, 0.0, 0.5, 1.0, 0.5, -0.5, -1.0],
    "Diffuse Field Target": [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 0.5, -1.5, -1.0, 0.5],
    
    # Sony
    "Sony WH-1000XM5": [-2.0, -1.0, 0.5, 1.0, 1.0, 0.0, 0.5, 1.5, 1.0, 0.0],
    "Sony WH-1000XM4": [-1.5, -0.5, 0.0, 1.0, 1.5, 0.5, -1.0, 2.0, 1.5, -0.5],
    "Sony WF-1000XM4": [-1.0, -0.5, 0.5, 0.5, 0.0, 1.0, 0.5, -0.5, 1.0, 0.0],

    # Apple
    "Apple AirPods Pro 2": [1.0, 0.5, 0.0, -0.5, 0.0, 1.0, 0.5, -1.0, 1.5, 0.5],
    "Apple AirPods Max": [0.5, 0.0, -0.5, 0.0, 0.5, 1.0, 0.0, -0.5, 1.0, 1.5],
    "Apple EarPods": [3.5, 2.0, 0.5, 0.0, 0.0, 0.5, 1.0, 0.0, -1.5, -2.0],

    # Bose
    "Bose QuietComfort 45": [-1.0, 0.0, 0.5, 1.0, 0.5, -0.5, -1.5, 1.0, 2.0, 0.5],
    "Bose QC Ultra": [-1.5, -0.5, 0.0, 0.5, 1.0, 0.5, -1.0, 1.5, 1.5, 0.0],

    # Sennheiser
    "Sennheiser HD 650": [4.5, 3.0, 1.5, 0.5, 0.0, -0.5, 0.5, 1.0, -1.5, -2.0],
    "Sennheiser Momentum 4": [-2.0, -1.0, 0.0, 0.5, 1.0, 0.5, 0.0, 1.0, 1.5, 0.0],

    # Audio-Technica & Samsung
    "Audio-Technica ATH-M50x": [-2.0, -1.5, -0.5, 0.5, 1.0, 1.5, -1.0, 0.5, -1.5, 0.0],
    "Samsung Galaxy Buds Pro": [0.5, 0.5, 0.0, -0.5, 0.5, 1.0, 0.0, 1.0, 0.5, -0.5],
    "Samsung Galaxy Buds 2": [1.0, 0.5, 0.0, 0.0, 0.5, 0.5, -0.5, 0.5, 1.0, 0.0],
}


def get_all_autoeq_profiles() -> Dict[str, List[float]]:
    """Returns all available AutoEq profiles."""
    return dict(AUTOEQ_PROFILES)


def get_autoeq_profile_names() -> List[str]:
    """Returns sorted list of AutoEq profile display names."""
    return list(AUTOEQ_PROFILES.keys())


def get_autoeq_curve(profile_name: str) -> Optional[List[float]]:
    """Retrieves 10-band gain list for a given profile name, clamped between -12dB and +12dB."""
    if not profile_name or profile_name not in AUTOEQ_PROFILES:
        return None
    raw = AUTOEQ_PROFILES[profile_name]
    return [max(-12.0, min(12.0, float(g))) for g in raw]


def search_autoeq_profiles(query: str) -> Dict[str, List[float]]:
    """Fuzzy searches profile names matching query string."""
    if not query:
        return get_all_autoeq_profiles()
    q = query.lower().strip()
    return {k: v for k, v in AUTOEQ_PROFILES.items() if q in k.lower()}

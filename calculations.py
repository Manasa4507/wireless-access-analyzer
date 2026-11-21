import math
import json

def shannon_capacity(bw_hz: float, snr_linear: float) -> float:
    """Shannon capacity in bits per second for a given bandwidth and linear SNR."""
    return bw_hz * math.log2(1 + snr_linear)

def calculate_metrics(total_bw_mhz: float, num_users: int, per_user_rate_mbps: float, snr_db: float, network_condition: str, channel_model: str):
    """Calculate performance metrics for FDMA, TDMA, CDMA, OFDMA and SDMA.

    All formulas are deterministic and based on textbook models. No random numbers are used.
    """
    total_bw_hz = total_bw_mhz * 1e6
    snr_linear = 10 ** (snr_db / 10)

    # Technique specific factors (share of total bandwidth and efficiency multiplier)
    tech_factors = {
        "FDMA": {"share": 1.0, "efficiency": 0.85},
        "TDMA": {"share": 1.0, "efficiency": 0.80},
        "CDMA": {"share": 1.0, "efficiency": 0.75},
        "OFDMA": {"share": 0.9, "efficiency": 0.90},
        "SDMA": {"share": 0.85, "efficiency": 0.88},
    }

    # Network‑condition scaling (simplified linear factor)
    condition_factor = {
        "Low Traffic": 1.0,
        "Medium Traffic": 0.9,
        "High Traffic": 0.75,
    }[network_condition]

    # Channel‑model penalty (reduces effective bandwidth)
    channel_penalty = {
        "AWGN": 1.0,
        "Rayleigh Fading": 0.85,
        "Rician Fading": 0.92,
    }[channel_model]

    results = {}
    for tech, fac in tech_factors.items():
        # Effective bandwidth after sharing, traffic condition and channel effects
        bw_eff_hz = total_bw_hz * fac["share"] * condition_factor * channel_penalty

        # Spectral efficiency (bits/s/Hz) – limited by technique efficiency
        spectral_eff = fac["efficiency"] * math.log2(1 + snr_linear)

        # Total achievable data rate in Mbps
        total_rate_mbps = (bw_eff_hz * spectral_eff) / 1e6

        # Estimated user capacity (how many users can achieve the requested per‑user rate)
        user_capacity = int(total_rate_mbps // per_user_rate_mbps) if per_user_rate_mbps > 0 else 0

        # Bandwidth utilization as a percentage of the original total bandwidth
        bw_util_pct = (bw_eff_hz / total_bw_hz) * 100

        # Interference estimate – higher efficiency means lower interference (simplified)
        interference_pct = (1 - fac["efficiency"]) * 100

        # Performance score – weighted sum of key indicators (higher is better)
        score = (
            0.4 * spectral_eff +
            0.3 * (user_capacity / max(1, num_users)) +
            0.2 * (100 - interference_pct) +
            0.1 * bw_util_pct
        )

        results[tech] = {
            "bandwidth_hz": bw_eff_hz,
            "spectral_efficiency_bpshz": round(spectral_eff, 3),
            "total_rate_mbps": round(total_rate_mbps, 3),
            "user_capacity": user_capacity,
            "bandwidth_utilization_pct": round(bw_util_pct, 2),
            "interference_pct": round(interference_pct, 2),
            "performance_score": round(score, 3),
        }
    return results

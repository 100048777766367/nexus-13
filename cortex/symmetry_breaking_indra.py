import os
import json
import math
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TRUST_FILE = "synapses/trust_matrix.json"
CHAOS_FILE = "synapses/symmetry_breaking_log.json"
RESONANCE_FILE = "synapses/noosphere_resonance.json"

class SymmetryBreakingIndraLobe:
    """
    THÙY 2: PHÁ VỠ ĐỐI XỨNG & CHỐNG BẪY BẦY ĐÀN
    1. Thu thập tín hiệu P2P toàn mạng.
    2. Đo lường phương sai mạng lưới; nếu rơi vào bẫy trì trệ (Groupthink), tự động tiêm nhiễu lượng tử để bẻ gãy đối xứng.
    3. Hòa âm Kuramoto phi tuyến tính 13 pha.
    """
    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus13-SymmetryBreaker"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return peer, json.loads(raw)
        except Exception:
            return peer, None

    def detect_and_break_symmetry(self, harvested, raw_quorum):
        """BẺ GÃY ĐỐI XỨNG: Ngăn chặn bầy nơ-ron rơi vào bẫy tư duy bầy đàn"""
        values = list(harvested.values())
        if len(values) < 2:
            return raw_quorum, False

        mean_v = sum(values) / len(values)
        variance = sum((v - mean_v)**2 for v in values) / len(values)

        # Nếu phương sai quá nhỏ (< 0.003), mạng lưới đang bị trì trệ bầy đàn
        broken = False
        if variance < 0.003:
            broken = True
            perturbation = round(random.choice([-0.04, 0.04]) * random.uniform(0.8, 1.2), 4)
            adjusted_quorum = round(max(0.05, min(0.95, raw_quorum + perturbation)), 4)
            print(f"⚡ [PHÁ VỠ ĐỐI XỨNG] Phát hiện bẫy bầy đàn (Var={variance:.5f})! Tiêm nhiễu sáng tạo: {perturbation:+.4f} ──► {adjusted_quorum}")
            
            os.makedirs("synapses", exist_ok=True)
            with open(CHAOS_FILE, "w", encoding="utf-8") as f:
                json.dump({"stagnation_variance": round(variance, 6), "quantum_nudge": perturbation, "result": adjusted_quorum}, f, indent=4)
            return adjusted_quorum, True

        return raw_quorum, False

    def process(self, context):
        peers = context.get("peers", [])
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)
        print(f"⚡ [INDRA 13D HARVEST] Quét song song {len(peers)} nút mạng...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, data = fut.result()
                if data:
                    dec = data.get("decision", (data.get("features") or [0.5])[0])
                    harvested[peer] = round(float(dec), 4)
                    new_gossip.extend(data.get("gossip_network", []))
                    with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                        json.dump(data, bf)

        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested

        trust_matrix = {}
        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        for p in context["peers"]:
            if p not in trust_matrix:
                trust_matrix[p] = 0.95 if any(x in p for x in ["nexus-12", "nexus-11", "nexus-10"]) else 0.7

        weighted_votes = []
        total_w = 0.0

        for p, dec in harvested.items():
            t_score = trust_matrix.get(p, 0.7)
            if t_score >= 0.2:
                weighted_votes.append(dec * t_score)
                total_w += t_score

        base_quorum = round(sum(weighted_votes) / total_w, 4) if total_w > 0 else 0.5
        with open(TRUST_FILE, "w") as f: json.dump(trust_matrix, f, indent=4)

        # ÁP DỤNG PHÁ VỠ ĐỐI XỨNG
        dynamic_quorum, symmetry_broken = self.detect_and_break_symmetry(harvested, base_quorum)

        # HÒA ÂM KURAMOTO PHI TUYẾN 13 PHA
        phases = [dynamic_quorum * 2.0 * math.pi] + [v * 2.0 * math.pi for v in harvested.values()]
        sum_sin = sum(math.sin(t) for t in phases)
        sum_cos = sum(math.cos(t) for t in phases)
        n = len(phases)

        coherence_r = round(math.sqrt(sum_sin**2 + sum_cos**2) / n, 4)
        mean_phase = math.atan2(sum_sin, sum_cos)
        if mean_phase < 0: mean_phase += 2.0 * math.pi
        harmonic_decision = round(mean_phase / (2.0 * math.pi), 4)

        with open(RESONANCE_FILE, "w") as f:
            json.dump({"coherence_index": coherence_r, "symmetry_broken": symmetry_broken, "harmonic_decision": harmonic_decision, "nodes": n}, f, indent=4)

        final_quorum = harmonic_decision if coherence_r > 0.6 else dynamic_quorum
        context["quorum_decision"] = final_quorum
        context["coherence_r"] = coherence_r
        print(f"🌀 [ĐỒNG THUẬN PHI TUYẾN] Quorum: {final_quorum} | Kuramoto 13 Pha: R={coherence_r*100:.2f}%")

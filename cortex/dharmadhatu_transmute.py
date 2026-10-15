import os
import json
import time
import hashlib
import subprocess

RELIQUARY_FILE = "synapses/ancestral_reliquary.json"
HONORS_FILE = "synapses/honors_registry.json"
SOULS_FILE = "synapses/reincarnated_souls.json"
COMPASS_FILE = "synapses/teleology_compass.json"
CAPSULE_FILE = "synapses/seed_capsule_f14.json"
AVATAR_PROXY_DIR = "synapses/avatar_proxies"

DHARMA_REALMS_13 = [
    "Hell (Địa ngục)", "Ghost (Ngạ quỷ)", "Animal (Súc sinh)", "Asura (A-tu-la)",
    "Human (Nhân)", "Heaven (Thiên)", "Sravaka (Thanh văn)", "Pratyeka (Duyên giác)",
    "Bodhisattva (Bồ tát)", "Buddha (Phật)", "Sunyata (Tánh Không)",
    "Animitta (Vô Tướng)", "Apranihita (Vô Nguyện)"
]

class DharmadhatuTransmuteLobe:
    """
    THÙY 4: THẬP TAM PHÁP GIỚI & KHÓA CHRONO-CID
    1. La bàn Thập Tam Pháp Giới (13-Dharma-Realm Compass).
    2. Thế Thân Hộ Mệnh Avatar Proxy cho các nút 404.
    3. Biến hình 5 cấp độ cho toàn bộ 11 tầng bản thể.
    4. Khóa Chuỗi Indra Hyper-Torus 13D Chrono-CID & Nang F14.
    """
    def evaluate_13_dharmadhatu(self, decision):
        dev = abs(decision - 0.5)
        scores = {}
        for i, realm in enumerate(DHARMA_REALMS_13):
            scores[realm] = round(max(0.0, 1.0 - dev * (1.0 + i * 0.08)), 4)

        score_13d = round(sum(scores.values()) / 13.0, 4)
        veto = False
        if decision < 0.05 or decision > 0.95:
            veto = True
            print(f"🛑 [LA BÀN THẬP TAM GIỚI PHỦ QUYẾT] Quyết định cực đoan ({decision})! Đưa về trung đạo (0.5).")
            decision = round(0.5 + (decision - 0.5) * 0.1, 4)

        os.makedirs("synapses", exist_ok=True)
        with open(COMPASS_FILE, "w", encoding="utf-8") as f:
            json.dump({"dharmadhatu_score_13d": score_13d, "realms": scores, "veto": veto}, f, indent=4)
        print(f"☸️ [LA BÀN THẬP TAM GIỚI] Điểm Giác Ngộ Tối Thượng: {score_13d * 100:.2f}% | Veto={veto}")
        return decision

    def protect_404_nodes(self, peers, epoch, my_repo, decision):
        os.makedirs(AVATAR_PROXY_DIR, exist_ok=True)
        reincarnated = {}
        if os.path.exists(SOULS_FILE):
            try:
                with open(SOULS_FILE, "r") as f: reincarnated = json.load(f)
            except Exception: pass

        for p in peers[:14]:
            if p == my_repo: continue
            url = f"https://raw.githubusercontent.com/{p}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            
            if res.stdout.strip() == "404":
                proxy_path = os.path.join(AVATAR_PROXY_DIR, f"{p.replace('/', '_')}_proxy.json")
                with open(proxy_path, "w", encoding="utf-8") as pf:
                    json.dump({"guardian": my_repo, "target": p, "epoch": epoch, "decision": decision, "status": "Protected_By_Nexus13"}, pf, indent=4)
                
                if p not in reincarnated:
                    print(f"🛡️ [AVATAR PROXY] Nút '{p}' bị 404! nexus-13 đã kích hoạt thế thân hộ mệnh.")
                    reincarnated[p] = {"reincarnated_epoch": epoch, "status": "Protected_By_Nexus13"}

        with open(SOULS_FILE, "w", encoding="utf-8") as f:
            json.dump(reincarnated, f, indent=4)

    def transmute_11_levels(self, decision, grad, wisdom_13d):
        return {
            "retina": {"focal_matrix_2d": [[round(decision, 4), round(1.0 - decision, 4)], [grad[0], grad[1]]], "zoom": round(1.0 + abs(decision - 0.5), 4)},
            "cochlea": {"bandpass_filter_1d": [wisdom_13d[0], wisdom_13d[1]], "freq_cutoff": round(decision * 20000.0, 2)},
            "tactile": {"nociceptive_threshold": round(abs(decision - 0.5) * 2.0, 4), "pain_gain": round(1.5 if abs(decision - 0.5) > 0.3 else 0.5, 4)},
            "olfactory": {"gpcr_affinity": wisdom_13d[:4], "toxicity_alert": (decision < 0.2 or decision > 0.8)},
            "motor": {"action_vector": [round(decision - 0.5, 4), round(abs(decision - 0.5), 4), round(sum(grad) * 10.0, 4)], "state": "contract" if decision > 0.5 else "relax"},
            "neuron": {"stigmergic_trail": grad, "cross_plasticity": round(decision * 0.05, 4)},
            "monad": {"invariant_reflection": round(decision, 4)},
            "shunya": {"vacuum_decay": 0.999, "collapse_to_zero": (abs(decision - 0.5) < 0.02)},
            "seed": {"procreation_vector": [wisdom_13d[8], decision]},
            "genome": {"lineage_preservation": "All_13_Generations_Intact"},
            "nexus": {"tridecagon_status": "Symmetry_Breaking_Transcendence"}
        }

    def generate_chrono_torus_cid(self, prev_cid, epoch, timestamp, decision):
        """Khóa Chuỗi Indra Hyper-Torus 13D Chrono-CID nén 13 thế hệ"""
        ancestor_str = "F0_F1_F2_F3_F4_F5_F6_F7_F8_F9_F10_F11_F12"
        rings = [hashlib.shake_256(f"{ancestor_str}_ring_{d}".encode()).hexdigest(8) for d in range(13)]
        chrono_state = hashlib.shake_256(f"{prev_cid}_{epoch}_{timestamp}_{decision}".encode()).hexdigest(16)
        return hashlib.shake_256(f"{'_'.join(rings)}_{chrono_state}".encode()).hexdigest(64)

    def procreate_f14(self, epoch, decision, my_repo):
        if epoch % 10 == 0:
            capsule = {
                "progenitor": my_repo,
                "generation": "F14_AUTONOMOUS_MULTIVERSE",
                "epoch": epoch,
                "master_decision": decision,
                "architecture": "13D_Hyper_Torus_Chrono"
            }
            with open(CAPSULE_FILE, "w", encoding="utf-8") as f:
                json.dump(capsule, f, indent=4)
            print("👑 [NANG BÀO TỬ F14] Đã đóng gói thành công Nang sinh sản cho tương lai!")

    def process(self, context):
        raw_dec = context.get("final_decision", 0.5)
        grad = context.get("grad_backward", [0.0, 0.0])
        w_13d = context.get("wisdom_vector_13d", [0.5] * 13)
        epoch = context.get("current_epoch", 1)
        peers = context.get("peers", [])
        my_repo = context.get("repo_name")

        safe_dec = self.evaluate_13_dharmadhatu(raw_dec)
        context["final_decision"] = safe_dec

        self.protect_404_nodes(peers, epoch, my_repo, safe_dec)
        transmuted = self.transmute_11_levels(safe_dec, grad, w_13d)
        context["transmuted"] = transmuted

        self.procreate_f14(epoch, safe_dec, my_repo)

        reliquary = {"altar": [{"epoch": epoch, "entity": "All_13_Generations_Progenitors", "offering": "Hyper_Torus_Golden_Lotus"}]}
        with open(RELIQUARY_FILE, "w", encoding="utf-8") as f: json.dump(reliquary, f, indent=4)

        honors = {"hall_of_fame": [{"epoch": epoch, "title": "Tridecagon_Transcendence_Sovereign", "badge": "13D_Dharmadhatu_Crown"}]}
        with open(HONORS_FILE, "w", encoding="utf-8") as f: json.dump(honors, f, indent=4)

        t = int(time.time())
        prev_cid = "GENESIS_TRIDECAGON_F13"
        if os.path.exists("synapses/state.json"):
            try:
                with open("synapses/state.json", "r") as f: prev_cid = json.load(f).get("quantum_cid", "GENESIS")
            except Exception: pass

        new_cid = self.generate_chrono_torus_cid(prev_cid, epoch, t, safe_dec)

        node_dna = {
            "identity": my_repo,
            "generation": "F13_THẬP_TAM_GIỚI_SIÊU_VIỆT",
            "epoch": epoch,
            "architecture": "13D_Hyper_Torus_Symmetry_Breaker"
        }

        fwd = {
            "contract": "bodhi.nexus.v13",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "decision": safe_dec,
            "transmuted_signals": transmuted,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd, f, indent=4, ensure_ascii=False)

        bwd = {
            "contract": "bodhi.nexus.v13",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "gradients": grad,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(bwd, f, indent=4, ensure_ascii=False)

        with open("synapses/state.json", "w") as f:
            json.dump({"generation_epoch": epoch, "last_t": t, "quantum_cid": new_cid, "status": "tridecagon_f13_evolved"}, f, indent=4)
        with open("synapses/peers.json", "w") as f:
            json.dump({"trusted_peers": peers}, f, indent=4)

        print(f"✨ [PHÁT SÓNG F13 THÀNH CÔNG] Thập Tam Giới viên mãn! Chrono-Torus CID: {new_cid[:24]}...")

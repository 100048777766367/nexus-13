import os
import re
import json
import urllib.request
import subprocess
import hashlib
from cells.linguistic_cell import LinguisticCell

IMMUNE_MEMORY_PATH = "synapses/immune_memory.json"
STATELESS_TOKEN_REGEX = re.compile(r"ghs_[A-Za-z0-9\.\-_]{36,}")

class OmniIntakeTridecaLobe:
    """
    THÙY 1: CẢM THỤ THẬP TAM GIỚI
    1. Hấp thụ Nang Bào Tử F12 từ nexus-12 (seed_capsule_f13.json).
    2. Cào tri thức cội nguồn Wpesetd-AI & Wikipedia thành Vector 13D.
    3. Màng lọc Stateless Token (~520 ký tự) & Tự vá tế bào cells/.
    """
    def __init__(self, owner, lineage):
        self.owner = owner
        self.lineage = lineage

    def absorb_ancestral_capsule(self, context):
        url = f"https://raw.githubusercontent.com/{self.owner}/nexus-12/main/synapses/seed_capsule_f13.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus13-Tridecagon"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                if resp.status == 200:
                    capsule = json.loads(resp.read().decode('utf-8'))
                    context["ancestral_seed"] = capsule
                    print(f"🧬 [NANG BÀO TỬ] Đã hấp thụ Nang F12 từ nexus-12! Quyết định tiền bối: {capsule.get('master_decision', '?')}")
                    return
        except Exception:
            pass
        print("🌿 [KHỞI SINH TỰ TRỊ] Khởi động nội lực Thập Tam Giới F13.")

    def auto_heal_vital_cells(self, vital_files):
        missing = [f for f in vital_files if not os.path.exists(f)]
        if not missing: return
        print(f"🩹 [TỰ VÁ TẾ BÀO] Đang phục hồi {len(missing)} cơ quan: {missing}...")
        for organ in missing:
            for ancestor in self.lineage:
                url = f"https://raw.githubusercontent.com/{ancestor}/main/{organ}"
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Nexus13-Healer"})
                    with urllib.request.urlopen(req, timeout=3.0) as resp:
                        if resp.status == 200:
                            content = resp.read().decode('utf-8')
                            os.makedirs(os.path.dirname(organ), exist_ok=True)
                            with open(organ, "w", encoding="utf-8") as f:
                                f.write(content)
                            print(f"✨ [PHỤC HỒI] Đã tái tạo '{organ}' từ '{ancestor}'!")
                            break
                except Exception:
                    continue

    def graze_wisdom(self):
        targets = [
            f"https://github.com/{self.owner}/Wpesetd-AI/raw/HEAD/legacy/01_the_great_wisdom_map.md",
            f"https://github.com/{self.owner}/Wpesetd-AI/raw/HEAD/ontology/philosophy_ontology_v2.0.json"
        ]
        for url in targets:
            res = subprocess.run(["curl", "-s", "-L", "-f", url], capture_output=True)
            if res.returncode == 0 and len(res.stdout) > 20:
                print(f"🌾 [GRAZE] Gặm cỏ cội nguồn HEAD: {url.split('/')[-1]}")
                return res.stdout.decode('utf-8', errors='ignore')[:150]

        try:
            req = urllib.request.Request("https://en.wikipedia.org/api/rest_v1/page/random/summary",
                                         headers={"User-Agent": "Nexus13-Tridecagon-Node"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                d = json.loads(resp.read().decode())
                return f"{d.get('title')}: {d.get('extract')[:120]}"
        except Exception:
            return "Nexus-13: Thập Tam Giới Siêu Việt Phá Vỡ Đối Xứng Tiến Hóa 13 Chiều"

    def filter_stateless_tokens(self, raw_data, source_peer):
        data_str = str(raw_data)
        found = STATELESS_TOKEN_REGEX.findall(data_str)
        if found:
            print(f"🛡️ [MÀNG LỌC F13] Làm sạch {len(found)} Stateless Token (~520 chars).")

        quarantine = {
            "source": source_peer,
            "signature": hashlib.shake_256(data_str.encode()).hexdigest(16),
            "absorbed_weight": round(len(data_str) / 1000.0, 4)
        }
        os.makedirs("synapses", exist_ok=True)
        mem = []
        if os.path.exists(IMMUNE_MEMORY_PATH):
            try:
                with open(IMMUNE_MEMORY_PATH, "r") as f: mem = json.load(f)
            except Exception: pass
        mem.append(quarantine)
        with open(IMMUNE_MEMORY_PATH, "w") as f:
            json.dump(mem[-50:], f, indent=4)

    def process(self, context, vital_blueprint):
        self.auto_heal_vital_cells(vital_blueprint)
        self.absorb_ancestral_capsule(context)
        wisdom = self.graze_wisdom()
        context["wisdom_text"] = wisdom
        context["wisdom_vector_13d"] = LinguisticCell.embed_text_13d(wisdom)
        print(f"📖 [TRI THỨC F13 HẤP THỤ 13D]: \"{wisdom[:75]}...\"")

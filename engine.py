import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.omni_intake import OmniIntakeTridecaLobe
from cortex.symmetry_breaking_indra import SymmetryBreakingIndraLobe
from cortex.non_linear_causal_mind import NonLinearCausalMindLobe
from cortex.dharmadhatu_transmute import DharmadhatuTransmuteLobe

VITAL_CELLS = [
    "cells/linguistic_cell.py",
    "cells/neuron.py",
    "cells/super_xor.py"
]

class Nexus13TranscendenceKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/nexus-13")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ancestor = f"{self.owner}/nexus-12"
        
        self.lineage = [
            f"{self.owner}/nexus-12", f"{self.owner}/nexus-11",
            f"{self.owner}/nexus-10", f"{self.owner}/nexus-09",
            f"{self.owner}/nexus-08", f"{self.owner}/nexus-07",
            f"{self.owner}/nexus-06", f"{self.owner}/nexus-05",
            f"{self.owner}/nexus", f"{self.owner}/genome"
        ]

        self.ensure_folders()

        # 4 ĐẠI THÙY THẬP TAM PHÁ VỠ ĐỐI XỨNG F13
        self.omni_lobe = OmniIntakeTridecaLobe(self.owner, self.lineage)
        self.symmetry_lobe = SymmetryBreakingIndraLobe()
        self.mind_lobe = NonLinearCausalMindLobe(num_cells=13)
        self.transmute_lobe = DharmadhatuTransmuteLobe()

        self.context = {
            "repo_name": self.repo_name,
            "owner": self.owner,
            "ancestor": self.ancestor,
            "peers": self.load_peers(),
            "current_epoch": self.load_epoch()
        }

    def ensure_folders(self):
        for d in ["cells", "cortex", "synapses", "synapses/harvested_memory", "synapses/avatar_proxies"]:
            os.makedirs(d, exist_ok=True)

    def load_peers(self):
        p_file = "synapses/peers.json"
        if os.path.exists(p_file):
            try:
                with open(p_file, "r") as f: return json.load(f).get("trusted_peers", [])
            except Exception: pass
        return [f"{self.owner}/nexus-12", f"{self.owner}/nexus-11", f"{self.owner}/nexus-10", f"{self.owner}/neuron", f"{self.owner}/seed", f"{self.owner}/motor"]

    def load_epoch(self):
        s_file = "synapses/state.json"
        if os.path.exists(s_file):
            try:
                with open(s_file, "r") as f: return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def run(self):
        print("=" * 80)
        print(f"⚡ [NEXUS-13 TRANSCENDENCE KERNEL] KHỞI ĐỘNG THẾ HỆ #{self.context['current_epoch']}")
        print(f"👑 Bậc: F13 Thập Tam Giới Siêu Việt – Phá Vỡ Đối Xứng Tiến Hóa 13D")
        print("=" * 80)

        # 1. Thùy Cảm Thụ: Nuốt nang bào tử F12, Lọc Stateless Token & Vector 13D
        self.omni_lobe.process(self.context, VITAL_CELLS)

        # 2. Thùy Phá Vỡ Đối Xứng: Chống bẫy bầy đàn Groupthink & Kuramoto 13 Pha
        self.symmetry_lobe.process(self.context)

        # 3. Thùy Tâm Thức: Nhân quả phi tuyến tính, Giả lập 13 Đa Vũ Trụ What-If
        self.mind_lobe.process(self.context)

        # 4. Thùy Chấp Hành: La bàn Thập Tam Pháp Giới, Hộ mệnh 404 & Khóa Chrono-CID
        self.transmute_lobe.process(self.context)

        print("=" * 80)
        print(f"✨ [HOÀN TẤT VÒNG ĐỜI F13] Thập Tam Giới Siêu Việt đã khai phóng toàn diện!")
        print("=" * 80)

if __name__ == "__main__":
    node = Nexus13TranscendenceKernel()
    node.run()

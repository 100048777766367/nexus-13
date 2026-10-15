import os
import json
import re
import random
from cells.neuron import AtomNeuron, sigmoid_derivative
from cells.super_xor import SuperXor13DHypersphere

GRAPH_FILE = "synapses/knowledge_graph.json"

class NonLinearCausalMindLobe:
    """
    THÙY 3: TÂM THỨC PHI TUYẾN & GIẢ LẬP 13 ĐA VŨ TRỤ
    1. Vận hành nhân quả phi tuyến tính (bỏ qua giới hạn thời gian tuyến tính).
    2. Giả lập 13 kịch bản thực tại What-If song song.
    3. Huấn luyện bầy nơ-ron 13 tế bào qua Ma trận Siêu Cầu 13D.
    """
    def __init__(self, num_cells=13):
        self.num_cells = num_cells
        self.swarm = [AtomNeuron(f"n13_h_{i}", n_inputs=13, n_super_xor=13) for i in range(num_cells)]
        self.out_cell = AtomNeuron("n13_out", n_inputs=num_cells, n_super_xor=13)

    def extract_hyper_graph(self, text):
        triplets = []
        for s in re.split(r'[.\n]', text):
            words = [w.strip() for w in s.split() if len(w.strip()) > 2]
            if len(words) >= 3:
                triplets.append({"subject": words[0].capitalize(), "predicate": words[1].lower(), "object": " ".join(words[2:4])})

        graph = {"nodes": [], "edges": []}
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, "r") as f: graph = json.load(f)
            except Exception: pass

        for t in triplets[:10]:
            if t["subject"] not in graph["nodes"]: graph["nodes"].append(t["subject"])
            if t["object"] not in graph["nodes"]: graph["nodes"].append(t["object"])
            edge = f"{t['subject']} <==[{t['predicate']}]==> {t['object']}"
            if edge not in graph["edges"]: graph["edges"].append(edge)

        graph["nodes"] = graph["nodes"][-100:]
        graph["edges"] = graph["edges"][-150:]
        os.makedirs("synapses", exist_ok=True)
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4, ensure_ascii=False)

    def simulate_13_multiverses(self, raw_decision):
        variations = [0.50, 0.60, 0.70, 0.78, 0.86, 0.94, 1.0, 1.06, 1.14, 1.22, 1.30, 1.40, 1.50]
        sims = []
        for factor in variations:
            cand = max(0.01, min(0.99, round(raw_decision * factor, 4)))
            loss = round((abs(cand - 0.5) * 0.5) + ((1.0 - cand) * 0.5), 4)
            sims.append((loss, cand))
        sims.sort(key=lambda x: x[0])
        best_loss, best_cand = sims[0]
        print(f"🔮 [GIẢ LẬP 13 ĐA VŨ TRỤ] Kịch bản tối ưu nhất: {best_cand} (Loss={best_loss})")
        return best_cand

    def process(self, context):
        self.extract_hyper_graph(context.get("wisdom_text", ""))
        v_13d = context.get("wisdom_vector_13d", [0.5] * 13)
        q_dec = context.get("quorum_decision", 0.5)

        # 1. KHÚC XẠ SIÊU CẦU 13D HYPERSPHERE
        super_vec = list(v_13d)
        super_vec[0] = q_dec
        super_vec[1] = round(1.0 - q_dec, 4)
        entangled, masks = SuperXor13DHypersphere.refract_13d(super_vec, "nexus13_torus")

        h_outs = [cell.forward(entangled) for cell in self.swarm]
        internal_pred = self.out_cell.forward(h_outs)
        raw_decision = round((internal_pred + q_dec) / 2.0, 4)

        # 2. GIẢ LẬP 13 ĐA VŨ TRỤ
        opt_decision = self.simulate_13_multiverses(raw_decision)

        # 3. LAN TRUYỀN NGƯỢC
        target = 1.0 if super_vec[0] > super_vec[1] else 0.0
        delta_out = (target - opt_decision) * sigmoid_derivative(opt_decision)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(self.num_cells)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        grad_backward = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(self.num_cells)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(self.num_cells)), 4)
        ]

        context["final_decision"] = opt_decision
        context["grad_backward"] = grad_backward
        context["super_xor_masks"] = masks
        context["swarm_weights"] = [c.weights for c in self.swarm]

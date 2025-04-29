import torch
from opensora.models import STDiT2
from torch.nn.utils import prune

# 1. Load original model
model = STDiT2.from_pretrained("hpcai-tech/OpenSora-STDiT-v2-stage3")

# 2. Parameter tuning: Reduce layers/heads
model.transformer.layers = model.transformer.layers[:20]  # Keep 20/28 layers
for layer in model.transformer.layers:
    layer.attn.num_heads = 12  # Reduce from 16

# 3. Pruning: Remove 20% of attention weights
for layer in model.transformer.layers:
    prune.l1_unstructured(layer.attn.qkv, name="weight", amount=0.2)
    prune.remove(layer.attn.qkv, "weight")

# 4. Save optimized model
torch.save(model.state_dict(), "optimized_model.bin")
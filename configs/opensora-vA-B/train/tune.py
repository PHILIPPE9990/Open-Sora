import torch
import json
import torch.nn.utils.prune as prune
from opensora.models import STDiT2

# 1. Load the original model and its config
model = STDiT2.from_pretrained("hpcai-tech/OpenSora-STDiT-v2-stage3")
config = model.config

print(config)

# # 2. Modify the config
# config.depth = 20  # Reduced from 28
# config.num_heads = 12  # Reduced from 16

# # 3. Re-initialize a model with the modified config
# modified_model = STDiT2(config)

# # 4. Load partial pretrained weights
# # In your model modification script, replace the weight loading section with:
# # Replace your weight loading section with this:


# # pretrained_state = model.state_dict()
# # modified_state = modified_model.state_dict()

# # for name, param in modified_state.items():
# #     if name in pretrained_state and param.shape == pretrained_state[name].shape:
# #         modified_state[name] = pretrained_state[name]
# #     else:
# #         print(f"Skipping {name} due to shape mismatch")

# # modified_model.load_state_dict(modified_state, strict=False)



# pretrained_state = model.state_dict()
# modified_state = modified_model.state_dict()

# head_reduction_ratio = 12 / 16  # New heads / Original heads

# for name, param in modified_state.items():
#     if name in pretrained_state:
#         if param.shape == pretrained_state[name].shape:
#             modified_state[name] = pretrained_state[name]
#         else:
#             # Handle dimension mismatches due to head reduction
#             if 'rope.freqs' in name:
#                 # Interpolate rotary embeddings
#                 original = pretrained_state[name]
#                 modified_state[name] = torch.nn.functional.interpolate(
#                     original.unsqueeze(0).unsqueeze(0),
#                     size=(48,),
#                     mode='linear'
#                 ).squeeze()
                
#             elif 'norm.weight' in name or 'norm.bias' in name:
#                 # For normalization params, interpolate
#                 original = pretrained_state[name]
#                 modified_state[name] = torch.nn.functional.interpolate(
#                     original.unsqueeze(0).unsqueeze(0),
#                     size=(param.shape[0],),
#                     mode='linear'
#                 ).squeeze()
                
#             elif 'qkv' in name:
#                 # For QKV weights, we need to carefully reduce dimensions
#                 # Original shape: [3*16*head_dim, ...]
#                 # New shape: [3*12*head_dim, ...]
                
#                 # Calculate head dimensions
#                 original_dim = pretrained_state[name].shape[0]
#                 head_dim_original = original_dim // (3 * 16)
#                 head_dim_new = int(head_dim_original * head_reduction_ratio)
                
#                 # Reshape and reduce
#                 qkv = pretrained_state[name].view(3, 16, head_dim_original, -1)
#                 qkv = qkv[:, :12]  # Take first 12 heads
#                 qkv = torch.nn.functional.interpolate(
#                     qkv,
#                     size=(head_dim_new, qkv.shape[-1]),
#                     mode='linear'
#                 )
#                 modified_state[name] = qkv.reshape(3 * 12 * head_dim_new, -1)
                
#             elif 'proj' in name:
#                 # For projection layers
#                 original = pretrained_state[name]
#                 if len(original.shape) == 2:
#                     # Weight matrix
#                     modified_state[name] = torch.nn.functional.interpolate(
#                         original.unsqueeze(0),
#                         size=(param.shape[0], param.shape[1]),
#                         mode='bilinear'
#                     ).squeeze()
#                 else:
#                     # Bias vector
#                     modified_state[name] = torch.nn.functional.interpolate(
#                         original.unsqueeze(0).unsqueeze(0),
#                         size=(param.shape[0],),
#                         mode='linear'
#                     ).squeeze()
#             else:
#                 print(f"Skipping {name} due to shape mismatch")
#     else:
#         print(f"New parameter {name} not in pretrained model")

# modified_model.load_state_dict(modified_state, strict=False)

# # 5. Pruning (optional and structure-dependent)
# for i in range(len(modified_model.blocks)):
#     # Prune qkv in attn
#     qkv_linear = modified_model.blocks[i].attn.qkv
#     prune.l1_unstructured(qkv_linear, name="weight", amount=0.2)
#     prune.remove(qkv_linear, "weight")

#     # Prune qkv in attn_temp
#     qkv_temp_linear = modified_model.blocks[i].attn_temp.qkv
#     prune.l1_unstructured(qkv_temp_linear, name="weight", amount=0.2)
#     prune.remove(qkv_temp_linear, "weight")

# # 6. Save the model
torch.save(modified_model.state_dict(), "../../optimized_model/my_model.ckpt")
state_dict = torch.load("../../optimized_model/my_model.ckpt") 
# Save as .pt or .pth
torch.save(state_dict, "../../optimized_model/my_model.pt")

# config = {
#     "depth": 20,
#     "num_heads": 12,
#     "input_sq_size": 512,
#     "qk_norm": True,
#     "qk_norm_legacy": True,
#     "enable_flash_attn": True,
#     "enable_layernorm_kernel": True,
#     "in_channels": 4,
#     "hidden_size": 1152,
#     "mlp_ratio": 4.0,
#     "patch_size": [1, 2, 2],
#     "input_size": [32, 60, 106],
#     "model_type": "STDiT2"
# }

# with open("optimized_model/config.json", "w") as f:
#     json.dump(config, f, indent=2)

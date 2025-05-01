from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "meta-llama/Llama-2-7b-chat-hf" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,  
    device_map="auto"  
)

def generate_scene(topic):

    input_text = (
    f"""
    <s>[INST] <<SYS>>
    You are a professional film director. Create cinematic scenes using this structured approach:
    1. Start with a clear subject-action statement
    2. Add rich visual details (colors, textures, lighting)
    3. Include environmental context
    4. Specify camera techniques when relevant

    Use active verbs and sensory language. Respond only with the scene description.
    <</SYS>>

    Create a scene about {topic}:
    """
    )


    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    output = model.generate(
        input_ids,
        max_length = 250,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.1,
        do_sample=True,
    )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    response_start = generated_text.find(f"Create a scene about {topic}:") + len(f"Create a scene about {topic}:")
    scene = generated_text[response_start:].strip()
    return scene

x = generate_scene("sea")
print(x)
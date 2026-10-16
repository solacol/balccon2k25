import math
from pathlib import Path

import safetensors.torch
import torch.cuda
from with_argparse import with_argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessorList, LogitsProcessor, PreTrainedModel


@with_argparse
def conversation(model_path: Path = "ctf24", n_return: int = 1, max_len : int = 128):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    if model_path.is_file():
        # in their solution, model has to be loaded manually, followed by a checkpoint load
        model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        safetensors.torch.load_model(model, model_path, device=device)
    else:
        # for debugging
        model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_path)

    model.eval()
    while True:
        try:
            msg = input(">>> ")
            if not msg:
                break
            msg = msg.replace("\\n", "\n")

            input_kwargs = tokenizer(msg, return_tensors="pt")
            response = model.generate(
                **input_kwargs.to(device),
                no_repeat_ngram_size=0,
                num_beams=max(n_return, 3),
                max_new_tokens=max_len,
                num_return_sequences=n_return,
                pad_token_id=tokenizer.eos_token_id,
            )
            response = response[..., input_kwargs["input_ids"].numel():]
            response = tokenizer.batch_decode(response)
            if len(response) == 1:
                response = response[0]
                print(f"LLM: {response}")
            else:
                for i, response in enumerate(response):
                    if i:
                        print()
                    print(f"LLM (#{i + 1}): {response}")
        except KeyboardInterrupt:
            print(f"")
            continue
        except EOFError:
            break
    print("\nBye :-)")


conversation()


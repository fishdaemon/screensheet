from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests


class WebuiLLM(LLM):
    max_tokens: int =200
    temperature: float =0.7
    num_beams: int =1
    top_p: float =1
    top_k: int = 4
    typical_p: float =1
    repetition_penalty: float = 1.0

    # def __init__(self, temperature=0.7, max_tokens=200, num_beams=1, top_p=1, top_k=4, typical_p=1,
    #              repetition_penalty=1.0, **kwargs: Any):
    #     self.max_tokens = max_tokens
    #     self.temperature = temperature
    #     self.num_beams = num_beams
    #     self.top_p = top_p
    #     self.top_k = top_k
    #     self.typical_p = typical_p
    #     self.repetition_penalty = repetition_penalty
    #
    #     super().__init__(**kwargs)

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, ) -> str:
        response = requests.post(
            "http://localhost:5000/api/v1/generate",
            json={
                'prompt': prompt,
                'max_new_tokens': self.max_tokens,
                'do_sample': True,
                'temperature': self.temperature,
                'top_p': self.top_p,
                'typical_p': self.typical_p,
                'repetition_penalty': self.repetition_penalty,
                'top_k': self.top_k,
                'min_length': 0,
                'no_repeat_ngram_size': 0,
                'num_beams': self.num_beams,
                'penalty_alpha': 0,
                'length_penalty': 1,
                'early_stopping': True,
                'seed': -1,
                'add_bos_token': True,
                'truncation_length': 2048,
                'ban_eos_token': False,
                'skip_special_tokens': False,
                'stopping_strings': ["\n\n", "Observation:"]
            }
        )

        response.raise_for_status()

        return response.json()["results"][0]["text"].strip().replace("```", " ")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {

        }

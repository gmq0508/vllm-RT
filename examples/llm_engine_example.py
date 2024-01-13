import argparse
from typing import List, Tuple

from vllm import EngineArgs, LLMEngine, SamplingParams, RequestOutput

from time import sleep
from vllm.logger import init_logger
logger = init_logger(__name__)

def create_test_prompts() -> List[Tuple[str, SamplingParams]]:
    """Create a list of test prompts with their sampling parameters."""
    return [
        ("A",
         SamplingParams(temperature=0.0, logprobs=1, prompt_logprobs=1),
        10),
        ("T",
         SamplingParams(temperature=0.8, top_k=5, presence_penalty=0.2),
         1),
        ("W",
         SamplingParams(n=2,
                        best_of=5,
                        temperature=0.8,
                        top_p=0.95,
                        frequency_penalty=0.1),
                        1),
        ("I",
         SamplingParams(n=3, best_of=3, use_beam_search=True,
                        temperature=0.0),
                        1),
    ]


def process_requests(engine: LLMEngine,
                     test_prompts: List[Tuple[str, SamplingParams]]):
    """Continuously process a list of prompts and handle the outputs."""
    request_id = 0

    while request_id<=100 or engine.has_unfinished_requests():
        if request_id<=100:
            # sleep(10)
            prompt, sampling_params, priority = test_prompts[request_id%4]
            engine.add_request(str(request_id), prompt, sampling_params, None, priority)
            request_id += 1

        request_outputs: List[RequestOutput] = engine.step()
        # logger.info("step")
        for request_output in request_outputs:
            if request_output.finished:
                print(request_output.request_id)


def initialize_engine(args: argparse.Namespace) -> LLMEngine:
    """Initialize the LLMEngine from the command line arguments."""
    engine_args = EngineArgs.from_cli_args(args)
    return LLMEngine.from_engine_args(engine_args)


def main(args: argparse.Namespace):
    """Main function that sets up and runs the prompt processing."""
    engine = initialize_engine(args)
    test_prompts = create_test_prompts()
    process_requests(engine, test_prompts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Demo on using the LLMEngine class directly')
    parser = EngineArgs.add_cli_args(parser)
    args = parser.parse_args()
    main(args)

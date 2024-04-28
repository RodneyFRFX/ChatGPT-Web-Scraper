from typing import List, Dict, Callable
import torch
from transformers import StoppingCriteria, StoppingCriteriaList

# Code snippet 1: Creating tokenizer
def create_tokenizer(model_id: str, hf_auth: bool = False) -> transformers.PreTrainedTokenizer:
    """
    Create a tokenizer instance from a pre-trained model identifier.

    This function creates a tokenizer instance using the provided pre-trained model identifier.
    Optionally, it can use the Hugging Face authentication token for accessing private models.

    Parameters:
    model_id (str): Identifier or path to the pre-trained model.
    hf_auth (bool, optional): Flag indicating whether to use Hugging Face authentication token.
        Defaults to False.

    Returns:
    transformers.PreTrainedTokenizer: Tokenizer instance created from the pre-trained model.
    """
    return transformers.AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_auth)

# Code snippet 2: Generating stop token IDs
def generate_stop_token_ids(tokenizer: transformers.PreTrainedTokenizer, stop_list: List[str]) -> List[List[int]]:
    """
    Generate input IDs for stop tokens using a tokenizer.

    This function generates input IDs for stop tokens provided in the stop list
    using the specified tokenizer.

    Parameters:
    tokenizer (transformers.PreTrainedTokenizer): Tokenizer instance.
    stop_list (List[str]): List of strings containing stop tokens.

    Returns:
    List[List[int]]: List of lists containing input IDs for each stop token.
    """
    return [tokenizer(x)['input_ids'] for x in stop_list]

# Code snippet 3: Custom stopping criteria class
class StopOnTokens(StoppingCriteria):
    """
    Custom stopping criteria class based on StoppingCriteria.

    This class defines a custom stopping criteria based on the StoppingCriteria class provided by the transformers
    library. It checks whether the input sequence ends with any of the stop tokens specified in the stop_token_ids list.

    Methods:
    __call__: Overrides the __call__ method of StoppingCriteria. Checks if the input sequence ends with any of the
              stop tokens.
    """

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        """
        Check if the input sequence ends with any of the stop tokens.

        Parameters:
        input_ids (torch.LongTensor): Tensor containing input token IDs.
        scores (torch.FloatTensor): Tensor containing scores associated with each token.
        **kwargs: Additional keyword arguments.

        Returns:
        bool: True if the input sequence ends with any of the stop tokens, False otherwise.
        """
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

# Code snippet 4: Creating text generation pipeline
def create_generate_text_pipeline(model: str, tokenizer: transformers.PreTrainedTokenizer, stopping_criteria: StoppingCriteriaList) -> Callable[[str], List[Dict[str, str]]]:
    """
    Create a text generation pipeline.

    This function creates a text generation pipeline using the specified pre-trained model,
    tokenizer, and stopping criteria.

    Parameters:
    model (str): Pre-trained model for text generation.
    tokenizer (transformers.PreTrainedTokenizer): Tokenizer associated with the model.
    stopping_criteria (StoppingCriteriaList): Stopping criteria to control the generation process.

    Returns:
    Callable[[str], List[Dict[str, str]]]: Text generation pipeline function.
    """
    generate_text = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        task='text-generation',
        stopping_criteria=stopping_criteria,
        temperature=0.1,
        max_new_tokens=512,
        repetition_penalty=1.1
    )
    return generate_text

# Code snippet 5: Creating language model pipeline with langchain
def create_langchain_pipeline(generate_text_pipeline: Callable[[str], List[Dict[str, str]]]) -> HuggingFacePipeline:
    """
    Create a language model pipeline using langchain.

    This function creates a language model pipeline using the provided text generation pipeline
    from Hugging Face.

    Parameters:
    generate_text_pipeline (Callable[[str], List[Dict[str, str]]]): Text generation pipeline function.

    Returns:
    HuggingFacePipeline: Language model pipeline instance.
    """
    from langchain.llms import HuggingFacePipeline
    return HuggingFacePipeline(pipeline=generate_text_pipeline)

# Example usage
model_id = "meta-llama/Llama-2-7b-chat-hf"
hf_auth = False
tokenizer = create_tokenizer(model_id, hf_auth)
stop_list = ['\nHuman:', '\n```\n']
stop_token_ids = generate_stop_token_ids(tokenizer, stop_list)
stopping_criteria = StoppingCriteriaList([StopOnTokens()])
generate_text_pipeline = create_generate_text_pipeline(model_id, tokenizer, stopping_criteria)
langchain_pipeline = create_langchain_pipeline(generate_text_pipeline)
langchain_pipeline(prompt="Explain to me how I should address a breach in user security.")

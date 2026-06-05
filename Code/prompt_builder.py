from typing import Union, Dict, Any

def lower_text_character(text:str) -> str:

    return text[0].lower + text[1:] if text else text


def format_prompt_section(lead_in:str, value:Union[str,list[str]]) -> str:

    if isinstance(value, list):
        formatted_prompt = "".join(item for item in value)
    else:
        formatted_prompt = value
    
    return f"{lead_in}\n{formatted_prompt}"

def build_prompt_body(
        prompt_config: Dict[str, Any],
        input_prompt: Union[str, list[str], dict[str, Any]] | None = None
) -> str:
    prompt_parts = []
    if role := prompt_config.get('role'):
        prompt_parts.append(lower_text_character(f"You are a {role}"))
    
    if instructions := prompt_config.get('instructions'):
        if not instructions:
            raise ValueError("Instructions can't be empty")
        prompt_parts.append(format_prompt_section(f"You are required to follow these instructions:{instructions}"))
    
    if context := prompt_config.get('context'):
        prompt_parts.append(format_prompt_section(f"Use the following context",context))
    
    if examples := prompt_config.get('examples'):
        if isinstance(examples,list):
          for i, example in enumerate(examples):
            prompt_parts.append(format_prompt_section(f"Examples: {i}:\n{example}"))
        else:
            prompt_parts.append(format_prompt_section("Use the following example",examples))
    
    if output_constraints := prompt_config.get("output_constraints"):
        prompt_parts.append(format_prompt_section("Follow these guidelines when it comes to the output",output_constraints))
    
    if style_or_tone := prompt_config.get("style_or_tone"):
        prompt_parts.append("format these style and tone guidance in your response",style_or_tone)

    if goal := prompt_config.get('goal'):
        prompt_parts.append("Your goal is to achieve the following outcome",goal)
    
    if input_prompt is not None:
        prompt_parts.append(input_prompt)
    
    return "\n\n".join(prompt_parts)
        
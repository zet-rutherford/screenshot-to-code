import base64
import time
from typing import Awaitable, Callable, Dict, List
from openai.types.chat import ChatCompletionMessageParam
from google import genai
from google.genai import types
from llm import Completion, Llm


def convert_messages_to_gemini_contents(messages: list[dict[str, str]]) -> list[types.Content]:
    """
    Converts a list of messages (each with a role and content, which can be text or image)
    into the Gemini model's expected format using `types.Content` and `types.Part`.

    Each message dict must contain:
    - 'role': 'user', 'assistant', or 'system'
    - 'content': str or list of dicts (with 'type' and relevant keys)
    """
    
    generate_content = []
    generate_content_config = None

    for msg in messages:
        parts = []
        if isinstance(msg['content'], str):
            parts.append(types.Part.from_text(text=msg['content']))
        elif isinstance(msg['content'], list):
            for item in msg['content']:
                if item["type"] == "text":
                    parts.append(types.Part.from_text(text=item["text"]))
                elif item["type"] == "image_url":
                    image_url = item["image_url"]["url"]
                    if image_url.startswith("data:image/"):
                        mime_type = image_url.split(";")[0].split(":")[1]
                        b64_data = image_url.split(",")[1]
                        parts.append(
                            types.Part.from_bytes(
                                mime_type=mime_type,
                                data=base64.b64decode(b64_data),
                            )
                        )
                    else:
                        raise ValueError("Only base64-encoded image URLs are supported.")
                else:
                    raise ValueError(f"Unsupported content type: {item['type']}")
        else:
            raise ValueError(f"Unsupported content format: {type(msg['content'])}")
        
        if msg["role"] == "system":
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                system_instruction=[
                    types.Part.from_text(text=msg["content"])
                ]
            )
            continue
        elif msg["role"] == "assistant":
            content_obj = types.Content(
                role='model',
                parts=parts
            )
        else:
            content_obj = types.Content(
                role=msg['role'],
                parts=parts
            )

        generate_content.append(content_obj)

    return generate_content_config, generate_content


async def stream_gemini_response(
    messages: List[ChatCompletionMessageParam],
    api_key: str,
    callback: Callable[[str], Awaitable[None]],
    model_name: str,
) -> Completion:
    start_time = time.time()

    client = genai.Client(api_key=api_key)
    full_response = ""
    
    config, contents = convert_messages_to_gemini_contents(messages)

    if model_name == Llm.GEMINI_2_5_FLASH_PREVIEW_05_20.value:
        # Gemini 2.5 Flash supports thinking budgets
        extra_config = types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=20000,
            thinking_config=types.ThinkingConfig(
                thinking_budget=4000,
                include_thoughts=True
            ),
        )
    elif model_name == Llm.GEMINI_2_5_PRO_PREVIEW_05_06.value:
        extra_config = types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=20000,
            thinking_config=types.ThinkingConfig(include_thoughts=True),
        )
    else:
        # TODO: Fix output tokens here
        extra_config = types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=20000,
        )

    config = config.model_dump()
    extra_config = extra_config.model_dump(exclude_none=True)
    config.update(extra_config)
    config = types.GenerateContentConfig(**config)

    async for chunk in await client.aio.models.generate_content_stream(
        model=model_name,
        contents=contents,
        config=config
    ):
        if chunk.candidates and len(chunk.candidates) > 0:
            try:
                for part in chunk.candidates[0].content.parts:
                    if not part.text:
                        continue
                    elif part.thought:
                        await callback(part.text)
                        continue
                    else:
                        full_response += part.text
                        await callback(part.text)
            except Exception as e:
                print(f"Error processing chunk: {e}")
                await callback(str(chunk))
                await callback(f"Error processing chunk: {e}")
                continue
    completion_time = time.time() - start_time
    return {"duration": completion_time, "code": full_response}

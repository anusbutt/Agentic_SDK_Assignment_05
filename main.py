from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    ModelSettings,
)
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from configuration import config
from tools import UserContext, search_book, check_availability
from guardrails import library_guardrail

def dynamic_instructions(wrapper: RunContextWrapper[UserContext], agent=Agent[UserContext]):
    user = wrapper.context
    return f"You are assisting {user.name}. Only answer library-related questions politely."

library_agent = Agent[UserContext](
    name="Library Assistant",
    instructions=dynamic_instructions,
    tools=[search_book, check_availability],
    input_guardrails=[library_guardrail],
    model_settings=ModelSettings(
        temperature=0.1,
        tool_choice="required",
        max_tokens=100,
    )
)

async def main():
    user_info = UserContext(name="anus", member_id=13233)

    try:
        user_input = input("you: ")

        result = Runner.run_streamed(
            starting_agent=library_agent,
            input=user_input,
            context=user_info,
            run_config=config,
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    except InputGuardrailTripwireTriggered:
        print("\n❌ Guardrail triggered: Non-library query detected.")


if __name__ == "__main__":
    asyncio.run(main())

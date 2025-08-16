from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from configuration import config
from tools import UserContext, search_book, check_availability


class LibraryQueryCheck(BaseModel):
    is_library_related: bool
    reasoning: str


guardrail_agent = Agent(
    name="Library Guardrail Agent",
    instructions="Check if the user's query is related to library tasks "
                 "(like searching books, availability, timings).",
    output_type=LibraryQueryCheck,
)


@input_guardrail
async def library_guardrail(
    ctx: RunContextWrapper[UserContext],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_library_related,
    )


def dynamic_instructions(wrapper: RunContextWrapper[UserContext], agent=Agent[UserContext]):
    user = wrapper.context
    return f"You are assisting {user.name}. Only answer library-related questions politely."

library_agent = Agent[UserContext](
    name="Library Assistant",
    instructions=dynamic_instructions,
    tools=[search_book, check_availability],
    input_guardrails=[library_guardrail],
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

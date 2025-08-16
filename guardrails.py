from pydantic import BaseModel
from configuration import config
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, TResponseInputItem, input_guardrail, RunContextWrapper

class LibraryGuardrailOutput(BaseModel):
    is_library_query: bool
    reasoning: str

guardrail_agent = Agent(
    name="guardrail_agent",
    instructions="Check if the user query is about the library (books, availability, timings).",
    output_type=LibraryGuardrailOutput
)

@input_guardrail
async def library_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
        run_config=config
        )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_library_query 
       )
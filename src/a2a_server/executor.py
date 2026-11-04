"""A2A executor for the remote Architecture Assessment Agent."""

from a2a.helpers import new_task_from_user_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater

from src.a2a_server.assessment import assess_architecture


class ArchitectureAssessmentExecutor(AgentExecutor):

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        if context.current_task:
            task = context.current_task
        else:
            if context.message is None:
                raise ValueError("A2A request contains no message")

            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(
            event_queue=event_queue,
            task_id=task.id,
            context_id=task.context_id,
        )

        try:
            await updater.start_work()

            request = context.get_user_input()
            result = assess_architecture(request)

            await updater.add_artifact(
                parts=[
                    new_text_part(
                        text=result.model_dump_json(),
                        media_type="application/json",
                    )
                ],
                name="architecture-assessment",
            )

            await updater.complete()

        except Exception:
            await updater.failed()

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        raise NotImplementedError("Cancellation is not supported")

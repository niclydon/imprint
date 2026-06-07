# The Queue Underneath

The obvious problem was that the queue was slow.

That was not actually the problem.

The useful clue was that every slow job had already been retried twice. The queue was not overloaded because the work was large. It was overloaded because the failure mode was quiet.

Once the retries were visible, the fix became boring.

That is usually where the system starts telling the truth.

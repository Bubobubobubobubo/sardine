# New Outline by @thegamecracks

## Time

All clocks should now track internal times rather than repeatedly incrementing an elapsed time attribute. The time object will keep track of an origin point for clocks to translate their internal times into fish-bowl-monotonic time:

- origin: The point at which the next clock should start its time from.

- time_shift: Same as tick shift but part of the time.

## BaseClock

The base clock will now inherit from the base handler and the fish bowl will handle starting/stopping and pausing/resuming.

- On a fish bowl's creation, the initial clock will be added as a handler.

- When the fish bowl starts, a `start` event will be received.  If the clock has not started, it should start its run() loop in a background task.

- When the fish bowl stops, a `stop` event will be received.  If the clock is still running, it should cancel its run() loop.

- When the fish bowl pauses, a `pause` event will be received.  The clock should store the current time in `Time.origin`.

- When the fish bowl removes the clock handler, the teardown() method will be called.  If the clock is running, this should cancel the run() loop.

- When the fish bowl resumes, a `resume` event will be received.  If the clock has not started, it should start its run() loop.

All of the above is abstracted in the base clock. New clock implementations will not have to know about any of these hooks. If users want to extend the handler, they **must** invoke the base setup/teardown/hook methods.

- property time():
    Retrieves the current time, accounting for the origin.
- async sleep(duration):
    Sleeps until the given duration has passed.
    Nothing fancy except that the method must handle cancellation,
    whether from being paused or hot-swapping clocks.
- async run():
    The task that operates the clock. The internal clock doesn't
    need to do anything, but the link clock here should start a thread
    that continuously reads from the Ableton Link connection, and on
    cancellation it should stop the thread.

## FishBowl

The fish bowl will need ratelimiting on hooks to prevent them from erroring too frequently. Errors for each event-hook pair are tracked and when their rate limit is exceeded, invokations should temporarily stop.

- sleeper:
    A new SleepHandler object that is added to the fish bowl
    during instantiation.
- async sleep(duration):
    Sleeps until the given duration has passed.
    This method is simply a shorthand for `sleeper.sleep()`.
- swap_clock(clock):
    1. Pause the fish bowl
    2. Remove the old clock's handler
    3. Replace with the current clock and add it as a handler
    4. Resume the fish bowl
    5. Triggers a `clock_swap` event with one argument, the new BaseClock object.
- pause():
    If not paused, triggers a `pause` event.
- resume():
    If paused, triggers a `resume` event.
- start():
    If not started, triggers a `start` event.
- stop():
    If started, triggers a `stop` event.

## Handlers

Handlers that rely on blocking I/O should use threads with queues
to send messages. Messages can still be shared via events.

### SleepHandler

A new handler will be introduced for managing sleeps called SleepHandler.
This is a core component and will be an attribute of every fish bowl.

Using its async sleep() method, the scheduler and other handlers should be able
to sleep for a specific duration, even if the fish bowl is paused or
the clock gets swapped.

To do this, sleep() should calculate the monotonic deadline using the duration,
and `self.env.clock.time` property, then use `self.env.clock.sleep()`
to sleep the duration.

When the fish bowl pauses, the `pause` event will be received.
Existing sleep handles stored in the fish bowl should be informed of this
and should break their current sleep and wait on a resumption event indefinitely.

When the fish bowl resumes, the `resume` event will be received.
Sleep handles should use their monotonic deadline to
re-compute the remaining duration, then continue sleeping.

When the fish bowl stops, the `stop` even will be received.
Any existing sleep handles should not only stop, but also cancel the current
task they were called from. Remember to document this because it is
a significant side effect users should be aware of.

## Scheduler

The scheduler should be the only place where drift compensation is needed
in order to keep consistent intervals. Not only user functions, but
internal functions like the MIDI clock will be running via the scheduler.
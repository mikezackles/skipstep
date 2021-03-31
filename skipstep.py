import pathlib

# EDIT THIS!!
whitelist = [(pathlib.Path(__file__).parent.parent / 'src').resolve()]

class StepSkipper:
    @staticmethod
    def get_frame(thread_plan):
        return thread_plan.GetThread().GetFrameAtIndex(0)

    @staticmethod
    def is_in_whitelist(directory):
        while True:
            if any(x == directory for x in whitelist):
                return True
            if directory == directory.parent:
                return False
            directory = directory.parent

    def __init__(self, thread_plan, dict):
        self.thread_plan = thread_plan
        self.queue_next_plan()

    def queue_next_plan(self):
        line = self.get_frame(self.thread_plan).GetLineEntry()
        start_address = line.GetStartAddress()
        file_start = start_address.GetFileAddress()
        file_end = line.GetEndAddress().GetFileAddress()
        file_range = file_end - file_start
        self.step_thread_plan = self.thread_plan.QueueThreadPlanForStepInRange(
            start_address, file_range)

    def explains_stop(self, event):
        # We are stepping, so if we stop for any other reason, it isn't because
        # of us
        return False

    def should_stop(self, event):
        line = self.get_frame(self.thread_plan).GetLineEntry()
        filespec = line.GetFileSpec()
        directory = pathlib.Path(filespec.GetDirectory())
        is_allowed = self.is_in_whitelist(directory)

        if is_allowed:
            print("Stopping at {}:{}:{}".format(
                filespec.GetFilename(), line.GetLine(), line.GetColumn()))
        else:
            print("Skipping {}:{}:{}".format(filespec.GetFilename(),
                                             line.GetLine(), line.GetColumn()))

        # ONLY queue another plan if we're skipping through code
        if not is_allowed and self.step_thread_plan.IsPlanComplete():
            self.queue_next_plan()

        return is_allowed

    def should_step(self):
        # Instruct the debugger to instruction step
        return True

    def is_stale(self):
        return self.step_thread_plan.IsPlanStale()

def skipstep(debugger, command, exe_ctx, result, internal_dict):
    """Step through source code, only stopping in whitelisted files."""
    exe_ctx.GetThread().StepUsingScriptedThreadPlan(f"{__name__}.StepSkipper")
    debugger.HandleCommand('frame select 0')

def register_skipstep(debugger, command_name):
    adder = 'command script add -f {0}.skipstep {1}'.format(__name__,
                                                            command_name)
    debugger.HandleCommand(adder)
    print('The "{0}" command has been installed. Type "help {0}" for '
          'more information.'.format(command_name))

def __lldb_init_module(debugger, internal_dict):
    register_skipstep(debugger, 'skipstep')
    register_skipstep(debugger, 'sk')

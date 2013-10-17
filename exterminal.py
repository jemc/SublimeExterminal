import sublime, sublime_plugin


def plugin_loaded():
    Exterminal.plugin_loaded()


class Exterminal:
    
    def wrapped_exec(self, *args, **kwargs):
        
        shell_cmd = kwargs.get('shell_cmd')
        shell_cmd = "echo \"%s\" > /tmp/sublpipe" % shell_cmd.replace('"','\\"')
        kwargs['shell_cmd'] = shell_cmd
        
        return self.run_cached_by_exterminal(self, *args, **kwargs)
    
    def plugin_loaded():
        exec_cls = [cls for cls in sublime_plugin.window_command_classes \
                        if cls.__qualname__=='ExecCommand'][0]
        
        if hasattr(exec_cls(None), 'run_cached_by_exterminal'):
            exec_cls.run = exec_cls.run_cached_by_exterminal
            exec_cls.run_cached_by_exterminal = None
        
        exec_cls.run_cached_by_exterminal = exec_cls.run
        exec_cls.run = Exterminal.wrapped_exec

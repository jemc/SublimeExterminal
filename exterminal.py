import sublime, sublime_plugin

import os


def wrapped_exec(self, *args, **kwargs):
    settings = sublime.load_settings("SublimeExterminal.sublime-settings")
    
    if settings.get('enabled') and kwargs.get('use_exterminal', True):
        wrapper = settings.get('exec_wrapper')
        
        if self.window.active_view() and self.window.active_view().file_name():
            filepath = os.path.dirname(self.window.active_view().file_name())
            kwargs.setdefault('working_dir', filepath)
        
        try: kwargs['shell_cmd'] = ' '.join(kwargs['cmd']).replace('"','\\"')
        except KeyError: pass
        
        try: kwargs['shell_cmd'] = kwargs['shell_cmd'].replace('"','\\"')
        except KeyError: pass
        
        try: kwargs['shell_cmd'] = kwargs['shell_cmd'] = wrapper.format(**kwargs)
        except KeyError: pass
    
    return self.run_cached_by_exterminal(*args, **kwargs)

def plugin_loaded():
    exec_cls = [cls for cls in sublime_plugin.window_command_classes \
                    if cls.__qualname__=='ExecCommand'][0]
    
    if hasattr(exec_cls(None), 'run_cached_by_exterminal'):
        exec_cls.run = exec_cls.run_cached_by_exterminal
        exec_cls.run_cached_by_exterminal = None
    
    exec_cls.run_cached_by_exterminal = exec_cls.run
    exec_cls.run = wrapped_exec


class StartExterminalCommand(sublime_plugin.WindowCommand):
    def run(self, *args):
        settings = sublime.load_settings("SublimeExterminal.sublime-settings")
        cmd = settings.get('start_exterminal', '')
        os.popen(cmd)

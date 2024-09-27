# Bogushev V.V.
import tkinter as tk
import tkinter.messagebox as mb


def str_convert(work_str: str, t_expectation: str):
    com_str = work_str.strip().replace(",", ".")
    if t_expectation == "command":
        if com_str in "+-*/^%":
            return com_str
        else:
            return None
    else:
        try:
            return float(com_str)
        except ValueError:
            return None


class TopWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("400x227")
        self.master.resizable(False, False)

        self.frame_data = tk.Frame(self.master)
        self.data = tk.Text(self.frame_data, height=11, width=47)
        self.data.pack(side=tk.LEFT)

        self.scroll = tk.Scrollbar(self.frame_data, command=self.data.yview)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.data.config(yscrollcommand=self.scroll.set)

        self.frame_result = tk.Frame(self.master)
        self.res_label = tk.Label(self.frame_result, text="Result of calculations:")
        self.res_label.pack(side=tk.LEFT)
        self.res_data = tk.Label(self.frame_result)
        self.res_data.pack(side=tk.LEFT, fill=tk.X)

        self.frame_key = tk.Frame(self.master)
        self.key_clear = tk.Button(self.frame_key, text='Clear', width=10, command=self.do_clear)
        self.key_calc = tk.Button(self.frame_key, text='Calc', width=10, command=self.do_calc)
        self.key_save = tk.Button(self.frame_key, text='Save', width=10, command=self.do_save)
        self.key_load = tk.Button(self.frame_key, text='Load', width=10, command=self.do_load)
        self.key_help = tk.Button(self.frame_key, text='Help', width=10, command=self.do_help)

        self.key_clear.pack(side=tk.LEFT)
        self.key_calc.pack(side=tk.LEFT)
        self.key_save.pack(side=tk.LEFT)
        self.key_load.pack(side=tk.LEFT)
        self.key_help.pack(side=tk.LEFT)

        self.frame_data.pack(fill=tk.X)
        self.frame_result.pack(fill=tk.X)
        self.frame_key.pack(fill=tk.X)

    @staticmethod
    def get_commands(command_data: list) -> list:
        command_dict_default = {"one_": "res", "two_": None, "command": None}
        list_commands = []
        t_expectation = "one_"
        t_command = command_dict_default.copy()
        for t_str in command_data:
            t_value = str_convert(t_str, t_expectation)
            if t_value is None:
                t_expectation = "one_"
                break
            t_command[t_expectation] = t_value
            if t_expectation == "one_":
                t_expectation = "command"
            elif t_expectation == "two_":
                list_commands.append(t_command)
                t_command = command_dict_default.copy()
                t_expectation = "command"
            else:
                t_expectation = "two_"
        if t_expectation == "command" and t_command["one_"] is not None:
            return list_commands
        else:
            return []

    def do_clear(self):
        self.data.delete(1.0, 'end')
        self.res_data.config(text="")

    def do_calc(self):
        ops = eval('{%s}' % ','.join([(f"'{op}': lambda a, b: a {op.replace("^", "**").
                                       replace("%", "/ 100 *")} b") for op in '+-*/^%']))
        str_list = self.data.get(1.0, "end-1c").split("\n")
        commands_list = self.get_commands(str_list)
        my_res = 'Data error!'
        if len(commands_list) > 0:
            my_res = 0.0
            for my_command in commands_list:
                one_ = my_res
                if my_command["one_"] != "res":
                    one_ = my_command["one_"]
                if my_command["command"] == '/' and my_command["two_"] == 0.0:
                    my_res = 'You cannot divide by 0!'
                    break
                my_res = ops[my_command["command"]](one_, my_command["two_"])
        self.res_data.config(text=str(my_res))

    def do_save(self):
        with open(r'notepad.txt', 'w') as f:
            f.write(self.data.get(1.0, "end-1c"))

    def do_load(self):
        self.do_clear()
        with open('notepad.txt', 'r') as f:
            txt = f.read()
            self.data.insert(1.0, txt)

    @staticmethod
    def do_help():
        msg = """
    A line-by-line calculator.
    The first operator, operation, second operator - is set in order.
    Operation are being performed:
        addition - "+"
        subtraction - "-"
        multiplication - "*"
        division - "/"
        exponentiation - "^"
        getting a percentage - "%"     

    Example:
        2
        *
        8
        ^
        0.5
        Result of calculations: 4.0
    """
        mb.showinfo(f"Help", msg)


if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap("./icon/icon.ico")
    TopWindow(root)
    root.mainloop()

class UndoRedoService:

    def __init__(self):
        self._history = []
        self._index = -1

    def record(self, operation):
        self._history.append(operation)
        self._index = len(self._history) - 1

    def undo(self):
        if self._index == -1:
            raise Exception("You cannot undo anymore!")
        self._history[self._index].undo()
        self._index -= 1

    def redo(self):
        if self._index >= (len(self._history) - 1):
            raise Exception("You cannot redo anymore!")
        self._history[self._index + 1].redo()
        self._index += 1


class Call:

    def __init__(self, function_name, *function_params):
        self._function_name = function_name
        self._function_params = function_params

    def call(self):
        self._function_name(*self._function_params)


class Operation:

    def __init__(self, undo_call, redo_call):
        self._undo_call = undo_call
        self._redo_call = redo_call

    def undo(self):
        self._undo_call.call()

    def redo(self):
        self._redo_call.call()


class CascadeOperation:

    def __init__(self):
        self._operations = []

    def add(self, operation):
        self._operations.append(operation)

    def undo(self):
        for oper in self._operations:
            oper.undo()

    def redo(self):
        for oper in self._operations:
            oper.redo()


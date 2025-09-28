"""
6.101 Lab:
LISP Interpreter Part 2
"""

#!/usr/bin/env python3
import sys

sys.setrecursionlimit(20_000)

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


# KEEP THE ABOVE LINES INTACT, BUT REPLACE THIS COMMENT WITH YOUR lab.py FROM
# THE PREVIOUS LAB, WHICH SHOULD BE THE STARTING POINT FOR THIS LAB.
############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    expression_with_spaces = ""

    lines = source.split("\n")

    for our_line in lines:

        # We need need to ignore the comments after ;
        necessary_code_expression = our_line.split(";")[0]

        for char in necessary_code_expression:
            if char in "()":
                expression_with_spaces += f" {char} "

            else:
                expression_with_spaces += char

        # We add space at the end of each line to separate tokens across lines
        expression_with_spaces += " "

    tokens = expression_with_spaces.split()

    return tokens


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """

    def parse_expression(current_index):

        current_token = tokens[current_index]

        if current_token not in ("(", ")"):
            return number_or_symbol(current_token), current_index + 1

        if current_token == "(":
            our_sub_expression = []
            index = current_index + 1

            while index < len(tokens) and tokens[index] != ")":
                sub_expr, index = parse_expression(index)
                our_sub_expression.append(sub_expr)

            if index >= len(tokens):
                raise SchemeSyntaxError("Missing closing ')'")

            return our_sub_expression, index + 1

        raise SchemeSyntaxError(f"Unexpected token: {current_token}")

    parsed_expression, next_index = parse_expression(0)

    # We ensure no tokens are left over
    if next_index != len(tokens):
        raise SchemeSyntaxError("Extra tokens after valid expr")

    return parsed_expression


######################
# Built-in Functions #
######################


def calc_sub(*args):
    if len(args) == 1:
        return -args[0]

    first_num, *rest_nums = args
    return first_num - scheme_builtins["+"](*rest_nums)


def calc_mul(*args):
    if len(args) == 1:
        return args[0]

    first_num, *rest_nums = args
    return first_num * (calc_mul(*rest_nums))


def calc_div(*args):
    """Our division builtin function"""
    if len(args) == 1:
        return args[0]

    first_num = args[0]
    result = first_num

    for num in args[1:]:
        result /= num

    return result


def calc_equality(*args):
    return all(arg == args[0] for arg in args[1:])


def calc_greater_than(*args):
    return all(a > b for a, b in zip(args, args[1:]))


def calc_greater_or_equal(*args):
    return all(a >= b for a, b in zip(args, args[1:]))


def calc_lesser_than(*args):
    return all(a < b for a, b in zip(args, args[1:]))


def calc_lesser_or_equal(*args):
    return all(a <= b for a, b in zip(args, args[1:]))


def scheme_not_symbol(*args):
    if len(args) != 1:
        raise SchemeEvaluationError(" 'not' allows only one arg")
    return not args[0]


def cons(*args):
    if len(args) != 2:
        raise SchemeEvaluationError(" wrong number of arguments")
    return Pair(args[0], args[1])


def our_car(pair):
    if not isinstance(pair, Pair):
        raise SchemeEvaluationError(" car expects a pair ")

    return pair.car


def our_cdr(pair):
    if not isinstance(pair, Pair):
        raise SchemeEvaluationError(" cdr expects a pair ")

    return pair.cdr


none_var = None


def make_list(*args):

    # This represents the empty list
    head = none_var

    for index in range(len(args) - 1, -1, -1):
        head = Pair(args[index], head)

    return head


def is_list(*args):
    """List checker which checks if a certain expr is a list"""
    if len(args) != 1:
        raise SchemeEvaluationError("list? expects exactly one argument")
    pair = args[0]

    current_object = pair
    while isinstance(current_object, Pair):
        current_object = current_object.cdr

    return current_object is none_var

def get_length(*args):
    """It gets the length of the list"""
    if len(args) != 1:
        raise SchemeEvaluationError("length expects exactly one argument")

    our_lst = args[0]

    if not is_list(our_lst):
        raise SchemeEvaluationError("length expects a proper list")

    length = 0
    current = our_lst
    while current is not none_var:
        length += 1
        current = current.cdr
    return length


def list_ref(*args):
    """ List_ref function"""
    if len(args) != 2:
        raise SchemeEvaluationError("list-ref expects exactly two arguments")

    our_lst, index = args[0], args[1]

    if not isinstance(index, int) or index < 0:
        raise SchemeEvaluationError("list-ref expected a non-negative integer index")

    current = our_lst

    for _ in range(index):
        if not isinstance(current, Pair):
            raise SchemeEvaluationError("index out of bounds")
        current = current.cdr

    if not isinstance(current, Pair):
        raise SchemeEvaluationError("index out of bounds")

    return current.car

def append_list(*args):
    """Scheme equivalent of append in python with a slight change"""
    # Base case: no lists to append
    if not args:
        return none_var

    first, *rest = args

    if not is_list(first):
        raise SchemeEvaluationError("append expects proper lists")

    if first is none_var:
        return append_list(*rest)

    return Pair(first.car, append_list(first.cdr, *rest))


def multiple_expr(*args):

    for _, arg in enumerate(args):
        # if i!= len(args) -1:
        evaluate(arg, Frame)
        return args[len(args) - 1]


scheme_builtins = {
    "+": lambda *args: sum(args),
    "-": calc_sub,
    "*": calc_mul,
    "/": calc_div,
    "equal?": calc_equality,
    ">": calc_greater_than,
    ">=": calc_greater_or_equal,
    "<": calc_lesser_than,
    "<=": calc_lesser_or_equal,
    "not": scheme_not_symbol,
    "cons": cons,
    "car": our_car,
    "cdr": our_cdr,
    "list": make_list,
    "list?": is_list,
    "length": get_length,
    "list-ref": list_ref,
    "append": append_list,
    "begin": multiple_expr,
}


def evaluate_file(arg, frame=None):
    with open(arg, "r") as file:
        content = file.read()

    parsed_expr = parse(tokenize(content))
    return evaluate(parsed_expr, frame)



# Our Frame class definition
class Frame:
    """Our Frame class definition"""

    def __init__(self, parent=None):
        self.our_bindings = {}
        self.parent = parent

    def define(self, name, value):
        self.our_bindings[name] = value

    def look_up_var(self, name):
        if name in self.our_bindings:
            return self.our_bindings[name]

        elif self.parent:
            return self.parent.look_up_var(name)

        else:
            raise SchemeNameError(f"Unbound variable: {name}")

    def delete(self, var):
        if var in self.our_bindings:
            val = self.our_bindings[var]
            del self.our_bindings[var]
            return val
        else:
            raise SchemeNameError(f"Unbound variable: {var}")

    def make_initial_frame(self):
        return Frame(parent=self)

    def set_var(self, var, value):
        if var in self.our_bindings:
            self.our_bindings[var] = value
        elif self.parent:
            self.parent.set_var(var, value)
        else:
            raise SchemeNameError(f"Unbound variable: {var}")

    # def __str__(self):
    #     return f"<Frame: {self.our_bindings} |
    # Parent: {id(self.parent) if self.parent else None}>"


# make_initial_frame description
def make_initial_frame():
    """make_initial_frame description"""
    our_builtins_frame = Frame()

    for name, our_function in scheme_builtins.items():
        our_builtins_frame.define(name, our_function)

    initial_frame = Frame()
    initial_frame.parent = our_builtins_frame

    return initial_frame


# User_defined function class:
class user_defined_function:
    """User_defined function class"""

    def __init__(self, our_parameters, body, our_defining_frame):
        self.our_parameters = our_parameters
        self.body = body
        self.our_defining_frame = our_defining_frame

    def __call__(self, *args):
        if len(args) != len(self.our_parameters):
            raise SchemeEvaluationError("Incorrect number of arguments")

        # We make a new frame with lexical scoping
        our_new_frame = Frame(parent=self.our_defining_frame)

        # We need to bind our parameters to our arguments
        for i, _ in enumerate (self.our_parameters):
            parameter_name = self.our_parameters[i]
            argument_value = args[i]
            our_new_frame.define(parameter_name, argument_value)

        return evaluate(self.body, our_new_frame)


class Pair:
    """Represents a Scheme pair or "cons"  cell"""

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return f"({self.car} . {self.cdr})"




##############
# Evaluation #
##############

def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if frame is None:
        frame = make_initial_frame()

    # Our base cases
    if isinstance(tree, (int, float)):
        return tree

    if isinstance(tree, str):
        if tree == "#t":
            return True

        if tree == "#f":
            return False

        else:
            return frame.look_up_var(tree)

    # Our recursive step comes from here
    if isinstance(tree, list):

        # When we have an empty set
        if len(tree) == 0:
            return none_var

        # Our special del form
        first, *rest = tree
        if first == "del":
            if len(rest) != 1 or not isinstance(rest[0], str):
                raise SchemeSyntaxError(" bad 'del' expression")

            var = rest[0]
            return frame.delete(var)

        # Our special let form
        if first == "let":
            if len(rest) < 2:
                raise SchemeSyntaxError("let expression requires bindings and a body")

            bindings = rest[0]
            body = rest[1:]

            if not isinstance(bindings, list):
                raise SchemeSyntaxError("let bindings should be a list")

            # Evaluate all binding expressions in the current frame
            our_evaluated_bindings = []

            for binding in bindings:
                if not (isinstance(binding, list) and len(binding) == 2):
                    raise SchemeSyntaxError("Each let binding must be a pair")

                var, expr = binding
                if not isinstance(var, str):
                    raise SchemeSyntaxError("Binding name must be a symbol")

                val = evaluate(expr, frame)

                our_evaluated_bindings.append((var, val))

            # Create a new frame and define all bindings
            new_frame = frame.make_initial_frame()
            for var, val in our_evaluated_bindings:
                new_frame.define(var, val)

            # Evaluate the body expressions in the new frame
            result = None
            for expr in body:
                result = evaluate(expr, new_frame)
            return result

        # Our special setbang form
        if first == "set!":
            if len(rest) != 2:
                raise SchemeSyntaxError("set! expects exactly two arguments")
            var, value_expr = rest
            if not isinstance(var, str):
                raise SchemeSyntaxError(
                    "First argument to set! must be a variable name"
                )
            value = evaluate(value_expr, frame)
            frame.set_var(var, value)
            return value

        if tree[0] == "define" and isinstance(tree[1], list):
            our_function_name = tree[1][0]
            parametres = tree[1][1:]
            our_expr = tree[2]
            our_lambda_expr = ["lambda", parametres, our_expr]
            value = evaluate(our_lambda_expr, frame)
            frame.define(our_function_name, value)

            return value

        if tree[0] == "define":
            name = tree[1]
            our_expr = tree[2]

            our_expr_value = evaluate(our_expr, frame)
            frame.define(name, our_expr_value)
            return our_expr_value

        if tree[0] == "lambda":
            parameters = tree[1]
            body = tree[2]
            return user_defined_function(parameters, body, frame)

        if tree[0] == "if":
            if len(tree) != 4:
                raise SchemeSyntaxError("Few arguments passed in to if")

            _, predicate_expr, true_expr, false_expr = tree
            predicate_value = evaluate(predicate_expr, frame)

            if predicate_value:
                return evaluate(true_expr, frame)

            else:
                return evaluate(false_expr, frame)

        if tree[0] == "and":
            for expr in tree[1:]:
                result = evaluate(expr, frame)
                if not result:
                    return False
            return True

        if tree[0] == "or":
            for expr in tree[1:]:
                result = evaluate(expr, frame)
                if result:
                    return result
            return False

        our_first_function = evaluate(tree[0], frame)

        if not callable(our_first_function):
            raise SchemeEvaluationError("First element isn't callable")

        arguments = [evaluate(arg, frame) for arg in tree[1:]]

        # We check for correct number of arguments
        # for "car" and "cdr" built-in functions
        if tree[0] in ["car", "cdr"]:
            if len(arguments) != 1:
                raise SchemeEvaluationError(f"'{tree[0]}' expects exactly one argument")

        return our_first_function(*arguments)


if __name__ == "__main__":

    import os

    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    import schemerepl

    # Create the initial frame
    initial_frame_c = make_initial_frame()

    # Evaluate each file provided as a command-line argument
    for filename in sys.argv[1:]:
        evaluate_file(filename, initial_frame_c)
    schemerepl.SchemeREPL(
        sys.modules[__name__], use_frames=True, verbose=False,
        repl_frame=initial_frame_c
    ).cmdloop()

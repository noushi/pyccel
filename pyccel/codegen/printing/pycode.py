# coding: utf-8

from itertools import chain

from sympy.core import Symbol
from sympy import Tuple
from sympy.printing.pycode import PythonCodePrinter as SympyPythonCodePrinter
from sympy.printing.pycode import _known_functions
from sympy.printing.pycode import _known_functions_math
from sympy.printing.pycode import _known_constants_math

from pyccel.ast.utilities  import build_types_decorator
from pyccel.ast.core       import FunctionDef
from pyccel.ast.core       import FunctionCall
from pyccel.ast.core       import Assign, Return


#==============================================================================

def _construct_header(func_name, args):
    args = build_types_decorator(args, order='F')
    args = ','.join("{}".format(i) for i in args)
    pattern = '#$ header procedure static {name}({args})'
    return pattern.format(name=func_name, args=args)

#==============================================================================

class PythonCodePrinter(SympyPythonCodePrinter):
    _kf = dict(chain(
        _known_functions.items(),
        [(k, '' + v) for k, v in _known_functions_math.items()]
    ))
    _kc = {k: ''+v for k, v in _known_constants_math.items()}

    def _print_Variable(self, expr):
        return self._print(expr.name)

    def _print_IndexedElement(self, expr):
        indices = expr.indices
        if isinstance(indices, (tuple, list, Tuple)):
            # this a fix since when having a[i,j] the generated code is a[(i,j)]
            if len(indices) == 1 and isinstance(indices[0], (tuple, list, Tuple)):
                indices = indices[0]

            indices = [self._print(i) for i in indices]
            indices = ','.join(i for i in indices)
        else:
            raise NotImplementedError('TODO')

        base = self._print(expr.base)
        return '{base}[{indices}]'.format(base=base, indices=indices)

    def _print_FunctionDef(self, expr):
        name = self._print(expr.name)
        body = '\n'.join(self._print(i) for i in expr.body)
        body = self._indent_codestring(body)
        args = ', '.join(self._print(i) for i in expr.arguments)

        #imports = '\n'.join(self._print(i) for i in expr.imports)
        code = ('def {name}({args}):\n'
                '{body}\n').format(name=name, args=args, body=body)

        decorators = expr.decorators
        if decorators:
            for n,args in decorators.items():
                if args:
                    args = ','.join("{}".format(i) for i in args)
                    dec = '@{name}({args})'.format(name=n, args=args)

                else:
                    dec = '@{name}'.format(name=n)

                code = '{dec}\n{code}'.format(dec=dec, code=code)

        return code

    def _print_Return(self, expr):
        return 'return {}'.format(self._print(expr.expr))

    def _print_Comment(self, expr):
        txt = self._print(expr.text)
        return '# {0} '.format(txt)

    def _print_EmptyLine(self, expr):
        return ''

    def _print_NewLine(self, expr):
        return '\n'

    def _print_DottedName(self, expr):
        return '.'.join(self._print(n) for n in expr.name)

    def _print_FunctionCall(self, expr):
        func = self._print(expr.func)
        args = ','.join(self._print(i) for i in expr.arguments)
        return'{func}({args})'.format(func=func, args=args)

    def _print_Len(self, expr):
        return 'len({})'.format(self._print(expr.arg))

    def _print_Import(self, expr):
        target = ', '.join([self._print(i) for i in expr.target])
        if expr.source is None:
            return 'import {target}'.format(target=target)
        else:
            source = self._print(expr.source)
            return 'from {source} import {target}'.format(source=source, target=target)

    def _print_For(self, expr):
        iter   = self._print(expr.iterable)
        target = self._print(expr.target)
        body   = '\n'.join(self._print(i) for i in expr.body)
        body   = self._indent_codestring(body)
        code   = ('for {0} in {1}:\n'
                '{2}\n').format(target,iter,body)

        return code

    def _print_Assign(self, expr):
        lhs = self._print(expr.lhs)
        rhs = self._print(expr.rhs)
        return'{0} = {1}'.format(lhs,rhs)

    def _print_AugAssign(self, expr):
        lhs = self._print(expr.lhs)
        rhs = self._print(expr.rhs)
        op  = self._print(expr.op._symbol)
        return'{0} {1}= {2}'.format(lhs,op,rhs)

    def _print_Range(self, expr):
        start = self._print(expr.start)
        stop  = self._print(expr.stop)
        step  = self._print(expr.step)
        return 'range({}, {}, {})'.format(start,stop,step)

    def _print_IndexedBase(self, expr):
        return self._print(expr.label)

    def _print_Indexed(self, expr):
        inds = [i for i in expr.indices]
        #indices of indexedElement of len==1 shouldn't be a Tuple
        for i, ind in enumerate(inds):
            if isinstance(ind, Tuple) and len(ind) == 1:
                inds[i] = ind[0]

        inds = [self._print(i) for i in inds]

        return "%s[%s]" % (self._print(expr.base.label), ", ".join(inds))

    def _print_Zeros(self, expr):
        return 'zeros('+ self._print(expr.shape)+')'

    def _print_Slice(self, expr):
        return str(expr)

    def _print_Nil(self, expr):
        return 'None'

    def _print_Pass(self, expr):
        return 'pass'

    def _print_Is(self, expr):
        lhs = self._print(expr.lhs)
        rhs = self._print(expr.rhs)
        return'{0} is {1}'.format(lhs,rhs)

    def _print_If(self, expr):
        lines = []
        for i, (c, e) in enumerate(expr.args):
            if i == 0:
                lines.append("if (%s):" % self._print(c))

            elif i == len(expr.args) - 1 and c == True:
                lines.append("else:")

            else:
                lines.append("elif (%s):" % self._print(c))

            if isinstance(e, (list, tuple, Tuple)):
                for ee in e:
                    body = self._indent_codestring(self._print(ee))
                    lines.append(body)
            else:
                lines.append(self._print(e))
        return "\n".join(lines)

    def _print_String(self, expr):
        return '"{}"'.format(self._print(expr.arg))

    def _print_Shape(self, expr):
        arg = self._print(expr.arg)
        if expr.index is None:
            return '{}.shape'.format(arg)

        else:
            index = self._print(expr.index)
            return '{0}.shape[{1}]'.format(arg, index)

    def _print_Print(self, expr):
        args = []
        for f in expr.expr:
            if isinstance(f, str):
                args.append("'{}'".format(f))

            elif isinstance(f, Tuple):
                for i in f:
                    args.append("{}".format(self._print(i)))

            else:
                args.append("{}".format(self._print(f)))

        fs = ', '.join(i for i in args)

        return 'print({0})'.format(fs)

    def _print_F2PY_Function(self, expr):
        func = expr.func
        module_name = expr.module_name
        func_name = func.name

        args = func.arguments
        results = func.results
        if results:
#            print(results)
            if len(results) == 1:
                result = results[0]
                if result.rank > 0:
                    body = [Assign(result, FunctionCall(func, args))]
                    args = list(args) + [result]
#                    body = [FunctionCall(func, args)]
                else:
                    body  = [Assign(result, FunctionCall(func, args))]
                    body += [Return(result)]
        else:
            body = [FunctionCall(func, args)]

        f2py_func_name = 'f2py_{}'.format(func_name)
        f2py_func = FunctionDef(f2py_func_name, list(args), results, body)

        code = self._print(f2py_func)
        header = _construct_header(f2py_func_name, args)
        imports = 'from {mod} import {func}'.format( mod  = module_name,
                                                     func = func_name )

        code = '{imports}\n{header}\n{code}'.format( imports = imports,
                                                     header  = header,
                                                     code    = code )

        return code


    def _print_F2PY_Module(self, expr):
        code = '\n'.join(self._print(f) for f in expr.functions)
        return code

    def _print_F2PY_FunctionInterface(self, expr):
        f2py_module_name = expr.f2py_module_name
        f2py_func        = expr.f2py_function
        f2py_func_name   = f2py_func.name
        func_name        = f2py_func.func.name

        import_mod = 'from {name} import {module_name}'.format( name        = f2py_module_name,
                                                                module_name = f2py_module_name)
        assign_func = '{func} = {module}.{f2py_func}'.format( func      = func_name,
                                                              module    = f2py_module_name,
                                                              f2py_func = f2py_func_name )

        code = '{import_mod}\n{assign_func}'.format( import_mod = import_mod,
                                                     assign_func = assign_func )

        return code

    def _print_F2PY_ModuleInterface(self, expr):
        f2py_module = expr.module
        name = f2py_module.name

        import_mod = 'from {name} import {module_name}'.format( name        = name,
                                                                module_name = name)

        assign_func = ''
        for f in f2py_module.functions:
            func_name      = f.func.name
            f2py_func_name = f.name
            stmt = '{func} = {module}.{f2py_func}'.format( func      = func_name,
                                                           module    = name,
                                                           f2py_func = f2py_func_name )

            assign_func = '{assign_func}\n{stmt}'.format( assign_func = assign_func,
                                                          stmt        = stmt )

        code = '{import_mod}\n{assign_func}'.format( import_mod = import_mod,
                                                     assign_func = assign_func )
        return code



def pycode(expr, **settings):
    """ Converts an expr to a string of Python code
    Parameters
    ==========
    expr : Expr
        A SymPy expression.
    fully_qualified_modules : bool
        Whether or not to write out full module names of functions
        (``math.sin`` vs. ``sin``). default: ``True``.
    Examples
    ========
    >>> from sympy import tan, Symbol
    >>> from sympy.printing.pycode import pycode
    >>> pycode(tan(Symbol('x')) + 1)
    'math.tan(x) + 1'
    """
    return PythonCodePrinter(settings).doprint(expr)

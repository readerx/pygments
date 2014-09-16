# -*- coding: utf-8 -*-
"""
    pygments.lexers.misc.blitz
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for blitzbasic.com languages.

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, bygroups, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

__all__ = ['BlitzBasicLexer', 'BlitzMaxLexer', 'MonkeyLexer']


class BlitzMaxLexer(RegexLexer):
    """
    For `BlitzMax <http://blitzbasic.com>`_ source code.

    .. versionadded:: 1.4
    """

    name = 'BlitzMax'
    aliases = ['blitzmax', 'bmax']
    filenames = ['*.bmx']
    mimetypes = ['text/x-bmx']

    bmax_vopwords = r'\b(Shl|Shr|Sar|Mod)\b'
    bmax_sktypes = r'@{1,2}|[!#$%]'
    bmax_lktypes = r'\b(Int|Byte|Short|Float|Double|Long)\b'
    bmax_name = r'[a-z_]\w*'
    bmax_var = (r'(%s)(?:(?:([ \t]*)(%s)|([ \t]*:[ \t]*\b(?:Shl|Shr|Sar|Mod)\b)'
                r'|([ \t]*)(:)([ \t]*)(?:%s|(%s)))(?:([ \t]*)(Ptr))?)') % \
        (bmax_name, bmax_sktypes, bmax_lktypes, bmax_name)
    bmax_func = bmax_var + r'?((?:[ \t]|\.\.\n)*)([(])'

    flags = re.MULTILINE | re.IGNORECASE
    tokens = {
        'root': [
            # Text
            (r'[ \t]+', Text),
            (r'\.\.\n', Text),  # Line continuation
            # Comments
            (r"'.*?\n", Comment.Single),
            (r'([ \t]*)\bRem\n(\n|.)*?\s*\bEnd([ \t]*)Rem', Comment.Multiline),
            # Data types
            ('"', String.Double, 'string'),
            # Numbers
            (r'[0-9]+\.[0-9]*(?!\.)', Number.Float),
            (r'\.[0-9]*(?!\.)', Number.Float),
            (r'[0-9]+', Number.Integer),
            (r'\$[0-9a-f]+', Number.Hex),
            (r'\%[10]+', Number.Bin),
            # Other
            (r'(?:(?:(:)?([ \t]*)(:?%s|([+\-*/&|~]))|Or|And|Not|[=<>^]))' %
             (bmax_vopwords), Operator),
            (r'[(),.:\[\]]', Punctuation),
            (r'(?:#[\w \t]*)', Name.Label),
            (r'(?:\?[\w \t]*)', Comment.Preproc),
            # Identifiers
            (r'\b(New)\b([ \t]?)([(]?)(%s)' % (bmax_name),
             bygroups(Keyword.Reserved, Text, Punctuation, Name.Class)),
            (r'\b(Import|Framework|Module)([ \t]+)(%s\.%s)' %
             (bmax_name, bmax_name),
             bygroups(Keyword.Reserved, Text, Keyword.Namespace)),
            (bmax_func, bygroups(Name.Function, Text, Keyword.Type,
                                 Operator, Text, Punctuation, Text,
                                 Keyword.Type, Name.Class, Text,
                                 Keyword.Type, Text, Punctuation)),
            (bmax_var, bygroups(Name.Variable, Text, Keyword.Type, Operator,
                                Text, Punctuation, Text, Keyword.Type,
                                Name.Class, Text, Keyword.Type)),
            (r'\b(Type|Extends)([ \t]+)(%s)' % (bmax_name),
             bygroups(Keyword.Reserved, Text, Name.Class)),
            # Keywords
            (r'\b(Ptr)\b', Keyword.Type),
            (r'\b(Pi|True|False|Null|Self|Super)\b', Keyword.Constant),
            (r'\b(Local|Global|Const|Field)\b', Keyword.Declaration),
            (words((
                'TNullMethodException', 'TNullFunctionException',
                'TNullObjectException', 'TArrayBoundsException',
                'TRuntimeException'), prefix=r'\b', suffix=r'\b'), Name.Exception),
            (words((
                'Strict', 'SuperStrict', 'Module', 'ModuleInfo',
                'End', 'Return', 'Continue', 'Exit', 'Public', 'Private',
                'Var', 'VarPtr', 'Chr', 'Len', 'Asc', 'SizeOf', 'Sgn', 'Abs', 'Min', 'Max',
                'New', 'Release', 'Delete', 'Incbin', 'IncbinPtr', 'IncbinLen',
                'Framework', 'Include', 'Import', 'Extern', 'EndExtern',
                'Function', 'EndFunction', 'Type', 'EndType', 'Extends', 'Method', 'EndMethod',
                'Abstract', 'Final', 'If', 'Then', 'Else', 'ElseIf', 'EndIf',
                'For', 'To', 'Next', 'Step', 'EachIn', 'While', 'Wend', 'EndWhile',
                'Repeat', 'Until', 'Forever', 'Select', 'Case', 'Default', 'EndSelect',
                'Try', 'Catch', 'EndTry', 'Throw', 'Assert', 'Goto', 'DefData', 'ReadData',
                'RestoreData'), prefix=r'\b', suffix=r'\b'),
             Keyword.Reserved),
            # Final resolve (for variable names and such)
            (r'(%s)' % (bmax_name), Name.Variable),
        ],
        'string': [
            (r'""', String.Double),
            (r'"C?', String.Double, '#pop'),
            (r'[^"]+', String.Double),
        ],
    }


class BlitzBasicLexer(RegexLexer):
    """
    For `BlitzBasic <http://blitzbasic.com>`_ source code.

    .. versionadded:: 2.0
    """

    name = 'BlitzBasic'
    aliases = ['blitzbasic', 'b3d', 'bplus']
    filenames = ['*.bb', '*.decls']
    mimetypes = ['text/x-bb']

    bb_sktypes = r'@{1,2}|[#$%]'
    bb_name = r'[a-z]\w*'
    bb_var = (r'(%s)(?:([ \t]*)(%s)|([ \t]*)([.])([ \t]*)(?:(%s)))?') % \
             (bb_name, bb_sktypes, bb_name)

    flags = re.MULTILINE | re.IGNORECASE
    tokens = {
        'root': [
            # Text
            (r'[ \t]+', Text),
            # Comments
            (r";.*?\n", Comment.Single),
            # Data types
            ('"', String.Double, 'string'),
            # Numbers
            (r'[0-9]+\.[0-9]*(?!\.)', Number.Float),
            (r'\.[0-9]+(?!\.)', Number.Float),
            (r'[0-9]+', Number.Integer),
            (r'\$[0-9a-f]+', Number.Hex),
            (r'\%[10]+', Number.Bin),
            # Other
            (words(('Shl', 'Shr', 'Sar', 'Mod', 'Or', 'And', 'Not',
                    'Abs', 'Sgn', 'Handle', 'Int', 'Float', 'Str',
                    'First', 'Last', 'Before', 'After'),
                   prefix=r'\b', suffix=r'\b'),
             Operator),
            (r'([+\-*/~=<>^])', Operator),
            (r'[(),:\[\]\\]', Punctuation),
            (r'\.([ \t]*)(%s)' % bb_name, Name.Label),
            # Identifiers
            (r'\b(New)\b([ \t]+)(%s)' % (bb_name),
             bygroups(Keyword.Reserved, Text, Name.Class)),
            (r'\b(Gosub|Goto)\b([ \t]+)(%s)' % (bb_name),
             bygroups(Keyword.Reserved, Text, Name.Label)),
            (r'\b(Object)\b([ \t]*)([.])([ \t]*)(%s)\b' % (bb_name),
             bygroups(Operator, Text, Punctuation, Text, Name.Class)),
            (r'\b%s\b([ \t]*)(\()' % bb_var,
             bygroups(Name.Function, Text, Keyword.Type, Text, Punctuation,
                      Text, Name.Class, Text, Punctuation)),
            (r'\b(Function)\b([ \t]+)%s' % bb_var,
             bygroups(Keyword.Reserved, Text, Name.Function, Text, Keyword.Type,
                      Text, Punctuation, Text, Name.Class)),
            (r'\b(Type)([ \t]+)(%s)' % (bb_name),
             bygroups(Keyword.Reserved, Text, Name.Class)),
            # Keywords
            (r'\b(Pi|True|False|Null)\b', Keyword.Constant),
            (r'\b(Local|Global|Const|Field|Dim)\b', Keyword.Declaration),
            (words((
                'End', 'Return', 'Exit', 'Chr', 'Len', 'Asc', 'New', 'Delete', 'Insert',
                'Include', 'Function', 'Type', 'If', 'Then', 'Else', 'ElseIf', 'EndIf',
                'For', 'To', 'Next', 'Step', 'Each', 'While', 'Wend',
                'Repeat', 'Until', 'Forever', 'Select', 'Case', 'Default',
                'Goto', 'Gosub', 'Data', 'Read', 'Restore'), prefix=r'\b', suffix=r'\b'),
             Keyword.Reserved),
            # Final resolve (for variable names and such)
            # (r'(%s)' % (bb_name), Name.Variable),
            (bb_var, bygroups(Name.Variable, Text, Keyword.Type,
                              Text, Punctuation, Text, Name.Class)),
        ],
        'string': [
            (r'""', String.Double),
            (r'"C?', String.Double, '#pop'),
            (r'[^"]+', String.Double),
        ],
    }


class MonkeyLexer(RegexLexer):
    """
    For
    `Monkey <https://en.wikipedia.org/wiki/Monkey_(programming_language)>`_
    source code.

    .. versionadded:: 1.6
    """

    name = 'Monkey'
    aliases = ['monkey']
    filenames = ['*.monkey']
    mimetypes = ['text/x-monkey']

    name_variable = r'[a-z_]\w*'
    name_function = r'[A-Z]\w*'
    name_constant = r'[A-Z_][A-Z0-9_]*'
    name_class = r'[A-Z]\w*'
    name_module = r'[a-z0-9_]*'

    keyword_type = r'(?:Int|Float|String|Bool|Object|Array|Void)'
    # ? == Bool // % == Int // # == Float // $ == String
    keyword_type_special = r'[?%#$]'

    flags = re.MULTILINE

    tokens = {
        'root': [
            # Text
            (r'\s+', Text),
            # Comments
            (r"'.*", Comment),
            (r'(?i)^#rem\b', Comment.Multiline, 'comment'),
            # preprocessor directives
            (r'(?i)^(?:#If|#ElseIf|#Else|#EndIf|#End|#Print|#Error)\b', Comment.Preproc),
            # preprocessor variable (any line starting with '#' that is not a directive)
            (r'^#', Comment.Preproc, 'variables'),
            # String
            ('"', String.Double, 'string'),
            # Numbers
            (r'[0-9]+\.[0-9]*(?!\.)', Number.Float),
            (r'\.[0-9]+(?!\.)', Number.Float),
            (r'[0-9]+', Number.Integer),
            (r'\$[0-9a-fA-Z]+', Number.Hex),
            (r'\%[10]+', Number.Bin),
            # Native data types
            (r'\b%s\b' % keyword_type, Keyword.Type),
            # Exception handling
            (r'(?i)\b(?:Try|Catch|Throw)\b', Keyword.Reserved),
            (r'Throwable', Name.Exception),
            # Builtins
            (r'(?i)\b(?:Null|True|False)\b', Name.Builtin),
            (r'(?i)\b(?:Self|Super)\b', Name.Builtin.Pseudo),
            (r'\b(?:HOST|LANG|TARGET|CONFIG)\b', Name.Constant),
            # Keywords
            (r'(?i)^(Import)(\s+)(.*)(\n)',
             bygroups(Keyword.Namespace, Text, Name.Namespace, Text)),
            (r'(?i)^Strict\b.*\n', Keyword.Reserved),
            (r'(?i)(Const|Local|Global|Field)(\s+)',
             bygroups(Keyword.Declaration, Text), 'variables'),
            (r'(?i)(New|Class|Interface|Extends|Implements)(\s+)',
             bygroups(Keyword.Reserved, Text), 'classname'),
            (r'(?i)(Function|Method)(\s+)',
             bygroups(Keyword.Reserved, Text), 'funcname'),
            (r'(?i)(?:End|Return|Public|Private|Extern|Property|'
             r'Final|Abstract)\b', Keyword.Reserved),
            # Flow Control stuff
            (r'(?i)(?:If|Then|Else|ElseIf|EndIf|'
             r'Select|Case|Default|'
             r'While|Wend|'
             r'Repeat|Until|Forever|'
             r'For|To|Until|Step|EachIn|Next|'
             r'Exit|Continue)\s+', Keyword.Reserved),
            # not used yet
            (r'(?i)\b(?:Module|Inline)\b', Keyword.Reserved),
            # Array
            (r'[\[\]]', Punctuation),
            # Other
            (r'<=|>=|<>|\*=|/=|\+=|-=|&=|~=|\|=|[-&*/^+=<>|~]', Operator),
            (r'(?i)(?:Not|Mod|Shl|Shr|And|Or)', Operator.Word),
            (r'[\(\){}!#,.:]', Punctuation),
            # catch the rest
            (r'%s\b' % name_constant, Name.Constant),
            (r'%s\b' % name_function, Name.Function),
            (r'%s\b' % name_variable, Name.Variable),
        ],
        'funcname': [
            (r'(?i)%s\b' % name_function, Name.Function),
            (r':', Punctuation, 'classname'),
            (r'\s+', Text),
            (r'\(', Punctuation, 'variables'),
            (r'\)', Punctuation, '#pop')
        ],
        'classname': [
            (r'%s\.' % name_module, Name.Namespace),
            (r'%s\b' % keyword_type, Keyword.Type),
            (r'%s\b' % name_class, Name.Class),
            # array (of given size)
            (r'(\[)(\s*)(\d*)(\s*)(\])',
             bygroups(Punctuation, Text, Number.Integer, Text, Punctuation)),
            # generics
            (r'\s+(?!<)', Text, '#pop'),
            (r'<', Punctuation, '#push'),
            (r'>', Punctuation, '#pop'),
            (r'\n', Text, '#pop'),
            default('#pop')
        ],
        'variables': [
            (r'%s\b' % name_constant, Name.Constant),
            (r'%s\b' % name_variable, Name.Variable),
            (r'%s' % keyword_type_special, Keyword.Type),
            (r'\s+', Text),
            (r':', Punctuation, 'classname'),
            (r',', Punctuation, '#push'),
            default('#pop')
        ],
        'string': [
            (r'[^"~]+', String.Double),
            (r'~q|~n|~r|~t|~z|~~', String.Escape),
            (r'"', String.Double, '#pop'),
        ],
        'comment': [
            (r'(?i)^#rem.*?', Comment.Multiline, "#push"),
            (r'(?i)^#end.*?', Comment.Multiline, "#pop"),
            (r'\n', Comment.Multiline),
            (r'.+', Comment.Multiline),
        ],
    }

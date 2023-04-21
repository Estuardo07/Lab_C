import sys
from lexer import CFG
from afdd import DDFA
from parsing import Parser
from metodos import DumpAutomata
from generador import CodeGen

if __name__ == "__main__":

    grammar_file = './tests/slr-1.yal'

    if len(sys.argv) > 1:
        grammar_file = sys.argv[1]

    try:
        cfg = CFG(grammar_file)
    except FileNotFoundError as e:
        print(f'\tERR: "{grammar_file} file not found."')
    except Exception as e:
        print(f'\tERR: {e}')
        exit(-1)

    allchars = cfg.GetAllChars()
    parser = Parser(cfg)
    tokens = parser.ToSingleExpression()
    tree = parser.Parse(tokens)

    print(tree)
    print(tokens)

    ddfa = DDFA(tree, allchars, cfg.keywords, cfg.ignore)
    DumpAutomata(ddfa)

    CodeGen('./scanner.py', cfg.tokens, ddfa).GenerateScannerFile()

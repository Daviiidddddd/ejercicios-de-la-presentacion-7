# David Castellanos
from typing import Dict, List, Set, Tuple
from pathlib import Path
import json

def is_nonterminal(sym: str) -> bool:
    return isinstance(sym, str) and sym.isalpha() and sym.isupper()

class Grammar:
    def __init__(self, productions: Dict[str, List[List[str]]], start: str):
        self.productions = productions
        self.start = start
        self._first_cache: Dict[str, Set[str]] = {}
        self._first_rhs_cache: Dict[Tuple[str, ...], Set[str]] = {}
        self._follow_cache: Dict[str, Set[str]] = {}

    def first(self, X: str) -> Set[str]:
        if X in self._first_cache:
            return self._first_cache[X]
        res: Set[str] = set()
        self._first_cache[X] = res
        for alpha in self.productions.get(X, []):
            first_alpha = self.first_of_rhs(tuple(alpha))
            res.update(x for x in first_alpha if x != 'ε')
            if 'ε' in first_alpha:
                res.add('ε')
        self._first_cache[X] = res
        return res

    def first_of_rhs(self, rhs: Tuple[str, ...]) -> Set[str]:
        if rhs in self._first_rhs_cache:
            return self._first_rhs_cache[rhs]
        res: Set[str] = set()
        if len(rhs) == 0:
            res.add('ε')
            self._first_rhs_cache[rhs] = res
            return res
        for sym in rhs:
            if not is_nonterminal(sym):
                res.add(sym)
                break
            first_sym = self.first(sym)
            res.update(x for x in first_sym if x != 'ε')
            if 'ε' in first_sym:
                continue
            else:
                break
        else:
            res.add('ε')
        self._first_rhs_cache[rhs] = res
        return res

    def follow_all(self) -> Dict[str, Set[str]]:
        for nt in self.productions.keys():
            self._follow_cache.setdefault(nt, set())
        self._follow_cache[self.start].add('$')
        changed = True
        while changed:
            changed = False
            for A, rhss in self.productions.items():
                for rhs in rhss:
                    symbols = rhs
                    for i, B in enumerate(symbols):
                        if not is_nonterminal(B):
                            continue
                        rest = tuple(symbols[i+1:])
                        first_rest = self.first_of_rhs(rest)
                        before = set(self._follow_cache[B])
                        self._follow_cache[B].update(x for x in first_rest if x != 'ε')
                        if 'ε' in first_rest or len(rest) == 0:
                            self._follow_cache[B].update(self._follow_cache[A])
                        if self._follow_cache[B] != before:
                            changed = True
        return self._follow_cache

    def prediction_sets(self) -> Dict[str, Set[str]]:
        preds = {}
        follow_all = self.follow_all()
        for A, rhss in self.productions.items():
            for rhs in rhss:
                key = f\"{A} -> {' '.join(rhs) if rhs else 'ε'}\"
                first_rhs = self.first_of_rhs(tuple(rhs))
                pred = set(x for x in first_rhs if x != 'ε')
                if 'ε' in first_rhs:
                    pred.update(follow_all[A])
                preds[key] = pred
        return preds

def save_results(path: str, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

if __name__ == '__main__':
    # aqui se pone la gramaticas del ejercicio 3
    productions_example = {
        'S': [['A','B','C'], ['S','uno']],
        'A': [['dos','B','C'], ['ε']],
        'B': [['C','tres'], ['ε']],
        'C': [['cuatro','B'], ['ε']]
    }
    G = Grammar(productions_example, start='S')
    FIRST = {nt: sorted(list(G.first(nt))) for nt in productions_example.keys()}
    FOLLOW = {nt: sorted(list(v)) for nt,v in G.follow_all().items()}
    PRED = {k: sorted(list(v)) for k,v in G.prediction_sets().items()}
    results = {'productions': productions_example, 'FIRST': FIRST, 'FOLLOW': FOLLOW, 'PRED': PRED}
    save_results('/mnt/data/ffp_results_example.json', results)
    print('Resultados guardados en /mnt/data/ffp_results_example.json')

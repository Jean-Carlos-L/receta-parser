import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from core.dgs import SIMBOLOS_CONCORDANCIA, unificar_concordancia
from core.node import Nodo
from core.tokenizer import normalize_token
from grammar.gramatica import gramatica
from grammar.pcfg import PCFG, Rule, build_pcfg
from grammar.probabilidades import PROB_TABLE
from lexicon.rasgos import LEXICO_RASGOS


# The project models lexical categories as uppercase nonterminals.
TERMINALES_CATEGORIA = {
    'V', 'N', 'ADJ', 'DET', 'QUANT', 'PREP', 'LEVEL', 'NUM', 'CONJ', 'ORDEN'
}


@dataclass(frozen=True)
class _State:
    # Parsing position in the token stream.
    pos: int
    # Remaining symbols to expand/consume.
    pending: Tuple[str, ...]
    # Parse stack of partially built nodes.
    # We store a tuple of objects to keep it hashable; nodes are mutable but references are stable.
    stack: Tuple[Nodo, ...]


def _is_literal(sym: str) -> bool:
    # In this project, literals are symbols not present as LHS in grammar and not category terminals.
    return sym not in gramatica and sym not in TERMINALES_CATEGORIA


def _match_category(cat_sym: str, token: str) -> Optional[Nodo]:
    tok = normalize_token(token)
    rasgos = LEXICO_RASGOS.get(tok)
    if rasgos and rasgos.get('cat') == cat_sym.lower():
        n = Nodo(cat_sym, valor=tok)
        n.rasgos = dict(rasgos)
        return n
    return None


def _match_literal(lit: str, token: str) -> Optional[Nodo]:
    if normalize_token(token) == normalize_token(lit):
        n = Nodo(lit, valor=lit)
        n.rasgos = dict(LEXICO_RASGOS.get(lit, {}))
        return n
    return None


def _apply_concordance_if_needed(lhs: str, children: List[Nodo]) -> Optional[Dict]:
    if lhs in SIMBOLOS_CONCORDANCIA:
        return unificar_concordancia(children)
    # For non concordance nodes, we keep the shallow union behavior used by the current parser.
    rasgos: Dict = {}
    for c in children:
        if c.rasgos:
            rasgos.update(c.rasgos)
    return rasgos


def _build_node(lhs: str, rhs_len: int, stack: Tuple[Nodo, ...]) -> Optional[Tuple[Tuple[Nodo, ...], Nodo]]:
    if rhs_len == 0:
        children: List[Nodo] = []
        rest = stack
    else:
        if len(stack) < rhs_len:
            return None
        children = list(stack[-rhs_len:])
        rest = stack[:-rhs_len]

    node = Nodo(lhs, children)
    rasgos = _apply_concordance_if_needed(lhs, children)
    if rasgos is None:
        return None
    node.rasgos = rasgos
    return rest, node


def default_pcfg(*, allow_uniform_fallback: bool = True) -> PCFG:
    # Build a PCFG for the current grammar.
    return build_pcfg(gramatica, PROB_TABLE, allow_uniform_fallback=allow_uniform_fallback)


def _parse_reduce_marker(sym: str) -> Optional[Tuple[str, int]]:
    if not sym.startswith("@REDUCE:"):
        return None
    rest = sym[len("@REDUCE:"):]
    parts = rest.split(":")
    if len(parts) != 2:
        return None
    lhs = parts[0]
    try:
        ln = int(parts[1])
    except ValueError:
        return None
    return lhs, ln


def parse_1best(
    start_symbol: str,
    tokens: Sequence[str],
    *,
    pcfg: Optional[PCFG] = None,
    allow_uniform_fallback: bool = True,
    max_steps: int = 2_000_000,
) -> Tuple[Optional[Nodo], int]:
    """Return the most probable parse (1-best) under the PCFG.

    This is an optimal best-first search (uniform-cost) where costs are -log(prob).

    Behavior:
    - If a full parse consuming all tokens exists, returns the globally most probable one.
    - If no full parse exists, returns the best completed parse of `start_symbol` that
      consumes the most tokens (and breaks ties by higher probability).
    """

    if pcfg is None:
        pcfg = default_pcfg(allow_uniform_fallback=allow_uniform_fallback)

    pq: List[Tuple[float, int, _State]] = []
    tie = 0
    heapq.heappush(pq, (0.0, tie, _State(pos=0, pending=(start_symbol,), stack=())))
    tie += 1

    best_cost: Dict[Tuple[int, Tuple[str, ...], Tuple[Tuple[str, int], ...]], float] = {}
    furthest = 0
    steps = 0

    best_partial: Optional[Nodo] = None
    best_partial_pos = 0
    best_partial_cost = float("inf")

    def sig(st: _State):
        stack_sig = tuple((n.etiqueta, 0 if n.valor else len(n.hijos)) for n in st.stack)
        return (st.pos, st.pending, stack_sig)

    while pq:
        if steps >= max_steps:
            break
        steps += 1

        cost, _, st = heapq.heappop(pq)
        furthest = max(furthest, st.pos)

        key = sig(st)
        prev = best_cost.get(key)
        if prev is not None and cost >= prev:
            continue
        best_cost[key] = cost

        if not st.pending:
            if len(st.stack) == 1:
                # Completed a derivation of start_symbol.
                if st.pos == len(tokens):
                    return st.stack[0], st.pos
                # Keep best partial, similar to the existing parser API.
                if st.pos > best_partial_pos or (st.pos == best_partial_pos and cost < best_partial_cost):
                    best_partial = st.stack[0]
                    best_partial_pos = st.pos
                    best_partial_cost = cost
            continue

        sym = st.pending[0]
        rest_pending = st.pending[1:]

        # Reduce marker.
        red = _parse_reduce_marker(sym)
        if red is not None:
            lhs, rhs_len = red
            built = _build_node(lhs, rhs_len, st.stack)
            if built is None:
                continue
            rest_stack, node = built
            nxt = _State(pos=st.pos, pending=rest_pending, stack=rest_stack + (node,))
            heapq.heappush(pq, (cost, tie, nxt))
            tie += 1
            continue

        if sym in TERMINALES_CATEGORIA:
            if st.pos < len(tokens):
                leaf = _match_category(sym, tokens[st.pos])
                if leaf is not None:
                    nxt = _State(pos=st.pos + 1, pending=rest_pending, stack=st.stack + (leaf,))
                    heapq.heappush(pq, (cost, tie, nxt))
                    tie += 1
            continue

        if _is_literal(sym):
            if st.pos < len(tokens):
                leaf = _match_literal(sym, tokens[st.pos])
                if leaf is not None:
                    nxt = _State(pos=st.pos + 1, pending=rest_pending, stack=st.stack + (leaf,))
                    heapq.heappush(pq, (cost, tie, nxt))
                    tie += 1
            continue

        rhs_options = gramatica.get(sym, [])
        rules = pcfg.rules(sym, rhs_options)
        if not rules:
            continue

        for rule in rules:
            rhs = rule.rhs
            reduce_marker = f"@REDUCE:{rule.lhs}:{len(rhs)}"
            new_pending = tuple(rhs) + (reduce_marker,) + rest_pending
            new_cost = cost + (-rule.logp)
            nxt = _State(pos=st.pos, pending=new_pending, stack=st.stack)
            heapq.heappush(pq, (new_cost, tie, nxt))
            tie += 1

    if best_partial is not None:
        return best_partial, best_partial_pos
    return None, furthest

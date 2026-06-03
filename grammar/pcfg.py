import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


RHS = Tuple[str, ...]


@dataclass(frozen=True)
class Rule:
    lhs: str
    rhs: RHS
    logp: float


class PCFG:
    """A minimal PCFG wrapper for manual probabilities.

    - Probabilities are stored as log-probabilities.
    - For each LHS, probabilities must sum to 1.
    """

    def __init__(
        self,
        rules_by_lhs: Dict[str, List[Rule]],
        *,
        allow_uniform_fallback: bool = False,
    ):
        self._rules_by_lhs = rules_by_lhs
        self._allow_uniform_fallback = allow_uniform_fallback

    def rules(self, lhs: str, rhs_options: Sequence[Sequence[str]] | None = None) -> List[Rule]:
        """Return rules for an LHS.

        If rhs_options is provided and allow_uniform_fallback is enabled, missing rules for
        that LHS are generated uniformly from rhs_options.
        """

        rules = self._rules_by_lhs.get(lhs)
        if rules:
            return rules

        if not self._allow_uniform_fallback:
            return []

        if rhs_options is None or not rhs_options:
            return []

        # Uniform fallback over available CFG expansions.
        p = 1.0 / float(len(rhs_options))
        logp = math.log(p)
        return [Rule(lhs=lhs, rhs=tuple(rhs), logp=logp) for rhs in rhs_options]


def build_pcfg(
    grammar: Dict[str, List[List[str]]],
    prob_table: Dict[Tuple[str, RHS], float],
    *,
    allow_uniform_fallback: bool = False,
    tol: float = 1e-6,
) -> PCFG:
    """Build a PCFG from a CFG grammar and a manual probability table.

    - prob_table keys: (lhs, rhs_tuple)
    - values: prob in (0, 1]

    Validation:
    - If allow_uniform_fallback=False: every CFG rule must have an entry in prob_table.
    - For each LHS with explicit probabilities: sum(probs) must be 1.
    """

    rules_by_lhs: Dict[str, List[Rule]] = {}

    # Validate and build only for LHS that appear in CFG.
    for lhs, rhs_list in grammar.items():
        # Ignore lexical expansions auto-generated in grammar as part of CFG; they still
        # have explicit RHS options here. We treat them the same way.
        probs: List[float] = []
        rules: List[Rule] = []

        missing: List[RHS] = []
        for rhs in rhs_list:
            rhs_t = tuple(rhs)
            key = (lhs, rhs_t)
            if key not in prob_table:
                missing.append(rhs_t)
                continue
            p = prob_table[key]
            if not (0.0 < p <= 1.0):
                raise ValueError(f"Invalid prob for {lhs} -> {rhs_t}: {p}")
            probs.append(p)
            rules.append(Rule(lhs=lhs, rhs=rhs_t, logp=math.log(p)))

        if missing and not allow_uniform_fallback:
            # Fail fast: better than silently changing behavior.
            raise ValueError(
                f"Missing probabilities for {lhs}: "
                + ", ".join([str(m) for m in missing[:10]])
                + ("" if len(missing) <= 10 else f" (+{len(missing)-10} more)")
            )

        # If we have explicit probabilities for this LHS, validate normalization.
        if probs:
            s = sum(probs)
            if abs(s - 1.0) > tol:
                raise ValueError(f"Probabilities for {lhs} sum to {s}, expected 1")
            rules_by_lhs[lhs] = rules
        else:
            # No explicit entries; rely on uniform fallback at query time if enabled.
            # Do not store an empty list, otherwise we'd block the fallback.
            pass

    return PCFG(rules_by_lhs, allow_uniform_fallback=allow_uniform_fallback)

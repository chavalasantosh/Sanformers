"""
SanTOK SLM - Small Language Model

A constrained language generation system that can ONLY emit tokens
sanctioned by SanTOK Cognitive. Hallucination is structurally impossible,
not statistically unlikely.

Architecture:
    SanTOK Cognitive (THINKS) → facts, constraints, reasoning path
    SanTOK SLM (TALKS)        → constrained verbalization ONLY

NumPy is used strictly as a numerical backend.
No pretrained models. No ML frameworks. 100% SanTOK.
"""

from .slm_constraints import (
    TokenConstraint,
    FactConstraint,
    VocabularyScope,
    ConstraintEngine,
)

from .slm_generator import (
    ConstrainedGenerator,
    GenerationConfig,
    GenerationResult,
    SanTOKSLM,
)

__all__ = [
    # Constraints
    'TokenConstraint',
    'FactConstraint',
    'VocabularyScope',
    'ConstraintEngine',
    # Generator
    'ConstrainedGenerator',
    'GenerationConfig',
    'GenerationResult',
    'SanTOKSLM',
]


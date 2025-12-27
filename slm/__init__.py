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

from .tiny_transformer import (
    TinyTransformer,
    TransformerConfig,
    create_tiny_transformer,
)

from .slm_constrained_decoder import (
    ConstrainedDecoder,
    DecoderConfig,
    TransformerConstrainedSLM,
    create_transformer_slm,
)

__all__ = [
    # Constraints
    'TokenConstraint',
    'FactConstraint',
    'VocabularyScope',
    'ConstraintEngine',
    # Phase 1 Generator
    'ConstrainedGenerator',
    'GenerationConfig',
    'GenerationResult',
    'SanTOKSLM',
    # Phase 2 Transformer
    'TinyTransformer',
    'TransformerConfig',
    'create_tiny_transformer',
    # Phase 2 Decoder
    'ConstrainedDecoder',
    'DecoderConfig',
    'TransformerConstrainedSLM',
    'create_transformer_slm',
]


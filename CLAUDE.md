# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an **AgenticAI** codebase focused on multi-agent AI systems with comprehensive security, privacy, and evaluation frameworks. The repository demonstrates various AI agent patterns using AutoGen, with strong emphasis on GDPR compliance, differential privacy, and security best practices.

## Core Architecture

### Multi-Agent Framework
- Built on **AutoGen** for agent orchestration
- Uses **Together AI** (Gemma-3n-E4B-it model) as the primary LLM
- Configuration centralized in `model_config.py` with environment-based API keys
- Each module demonstrates different agent interaction patterns

### Agent Patterns by Module:
1. **01_userproxy**: Basic user-assistant interaction with code execution
2. **02_csa**: Customer service classification agent with conversation logging
3. **03_tools**: Tool-enabled agents (API, calculator, RAG, weather)
4. **04_multi**: Multi-agent patterns (sequential, hierarchical, conditional)
5. **05_eval**: Evaluation systems for toxicity and correctness
6. **06_security**: Comprehensive security and privacy framework

### Security-First Design
The codebase prioritizes defensive security with implementations for:
- GDPR compliance (right to explanation, data portability)
- PIPEDA compliance (Canadian privacy law)
- CCPA compliance (California consumer privacy rights)
- Differential privacy with mathematical guarantees
- Input validation and guardrails
- AI usage monitoring and audit trails

## Development Commands

### Environment Setup
```bash
# Install dependencies (uses uv package manager)
uv sync

# Install dev dependencies
uv sync --group dev
```

### Running Examples
```bash
# Run specific modules
uv run python 01_userproxy/main.py
uv run python 02_csa/main.py
uv run python 03_tools/agent_api.py

# Multi-agent patterns
uv run python 04_multi/two_agent.py
uv run python 04_multi/groupchat_sequential_pattern.py

# Evaluation examples
uv run python 05_eval/toxicity_correctness_llm.py

# Security examples
uv run python 06_security/examples/gdpr_example.py
uv run python 06_security/examples/pipeda_example.py
uv run python 06_security/examples/ccpa_example.py
uv run python 06_security/examples/differential_privacy_example.py
```

### Configuration Management
- **API Keys**: Set `TOGETHERAI_API_KEY` environment variable or use `.env` file
- **Model Configuration**: Modify `model_config.py` to change models or parameters
- **Agent Behavior**: Each module contains customizable system messages and LLM configs

## Key Implementation Patterns

### Agent Creation Pattern
```python
# Standard pattern used throughout codebase
import autogen
from model_config import llm_config

assistant = autogen.AssistantAgent(
    name="agent_name",
    llm_config=llm_config,
    system_message="Agent instructions..."
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config={"use_docker": False}
)
```

### Security Integration
- All security modules in `06_security/core/` are designed as drop-in components
- Import pattern: `from 06_security.core.module_name import ClassName`
- Compliance managers provide complete workflow implementations
- Utils provide reusable security functions (rate limiting, toxicity detection, HITL)

### Logging and Monitoring
- Modules use Python's `logging` module for audit trails
- Security module provides `ai_logging.py` for AI-specific monitoring
- Log files are typically created in module directories

## Critical Security Considerations

### Privacy by Design
- Differential privacy implementations require careful epsilon/delta parameter tuning
- GDPR explanations must not expose additional personal data
- All user data processing should go through compliance managers

### Input Validation
- Use `06_security/core/guardrails.py` for adversarial prompt detection
- Validate all external inputs before processing
- Implement rate limiting for production deployments

### Audit Requirements
- Log all AI interactions using `ai_logging.py`
- Maintain consent records for PIPEDA/GDPR compliance
- Document privacy impact assessments for new features

## Testing and Evaluation

### Evaluation Framework
- `05_eval/` contains LLM-based evaluation systems
- Toxicity detection using transformers-based models
- Factual correctness evaluation using Together AI's LLaMA
- Custom evaluation metrics for specific use cases

### Performance Monitoring
- Security modules include performance benchmarks
- Privacy vs accuracy trade-off analysis for differential privacy
- Response time monitoring for guardrails and validation

## Dependencies and Tools

### Core AI Frameworks
- **autogen-agentchat**: Primary agent framework
- **anthropic**: For Claude integrations
- **langchain-***: Extended LLM capabilities
- **together**: Together AI API client

### Security and Privacy
- **shap**: Model explanations for GDPR compliance
- **transformers**: Toxicity detection and content filtering
- **scikit-learn**: ML models for privacy-preserving training
- **xgboost**: Tree-based models with SHAP integration

### Development Tools
- **gradio**: Web interfaces for demos
- **playwright**: Web automation for testing
- **docker**: Containerization (optional, disabled by default)
- **uv**: Fast Python package management

## Module Interdependencies

### Shared Configuration
- `model_config.py` provides centralized LLM configuration
- All modules inherit from the same base configuration
- Environment variables are loaded via `python-dotenv`

### Security Integration Points
- Security modules are designed to wrap existing agents
- Compliance managers can be integrated into any agent workflow
- Utils provide middleware-style functionality for input/output processing

### Data Flow Patterns
- User input → Validation (guardrails) → Agent processing → Output filtering → Logging
- Privacy-sensitive workflows use differential privacy training
- GDPR/PIPEDA workflows require consent checking and audit trail generation
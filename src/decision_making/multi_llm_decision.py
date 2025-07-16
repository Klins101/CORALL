import os
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Union
from enum import Enum
import numpy as np
from abc import ABC, abstractmethod

# Import LLM clients
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts.prompt import PromptTemplate
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

@dataclass
class VesselState:
    """Represents the state of a vessel encounter"""
    risk: float
    distance: float
    bearing: float
    dcpa: float
    tcpa: float


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate response from the LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM provider is available"""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation"""
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.1, max_tokens: int = 500):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        
        if OPENAI_AVAILABLE and self.is_available():
            self.client = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
    
    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        return OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY") is not None
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        if not self.client:
            return "OpenAI not available"
        
        try:
            response = self.client.invoke(prompt)
            return response.content
        except Exception as e:
            return f"OpenAI error: {str(e)}"

class ClaudeProvider(LLMProvider):
    """Claude/Anthropic LLM provider implementation"""
    
    def __init__(self, model: str = "claude-sonnet-4-20250514", temperature: float = 0.1, max_tokens: int = 500):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        
        if ANTHROPIC_AVAILABLE and self.is_available():
            self.client = anthropic.Anthropic(
                api_key=os.getenv("CLAUDE_API_KEY")
            )
    
    def is_available(self) -> bool:
        """Check if Claude is available"""
        return ANTHROPIC_AVAILABLE and os.getenv("CLAUDE_API_KEY") is not None
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using Claude"""
        if not self.client:
            return "Claude not available"
        
        try:
            response = self.client.messages.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude error: {str(e)}"

class MultiLLMCOLREGSInterpreter:
    """COLREGs interpreter that can use multiple LLM providers"""
    
    def __init__(self, provider: str = None):
        self.provider_name = provider or os.getenv("LLM_PROVIDER", "openai")
        self.provider = self._initialize_provider()
        
        self.system_prompt = """You are a ship navigation officer. Make COLREGs-compliant decisions with your response in this format Rule {} (situation description), Action: [Stand on, no action / Give-way, turn to starboard / Give-way, turn to port / Continue current
maneuver], Explanation: Turn starboard req .."""
    
    def _initialize_provider(self) -> Optional[LLMProvider]:
        """Initialize the appropriate LLM provider"""
        if self.provider_name.lower() == "openai":
            provider = OpenAIProvider(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "50"))
            )
            if provider.is_available():
                return provider
        
        elif self.provider_name.lower() == "claude":
            provider = ClaudeProvider(
                model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
                temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "50"))
            )
            if provider.is_available():
                return provider
        
        # Fallback: try OpenAI if Claude fails, or vice versa
        if self.provider_name.lower() == "claude":
            fallback = OpenAIProvider()
            if fallback.is_available():
                print("Claude unavailable, falling back to OpenAI")
                return fallback
        else:
            fallback = ClaudeProvider()
            if fallback.is_available():
                print("OpenAI unavailable, falling back to Claude")
                return fallback
        
        return None
    
    
    
    def _format_situation_description(self, vessels: List[VesselState]) -> str:
        """Format situation description for LLM"""
        if not vessels:
            return "No vessels detected."
        
        
        highest_risk_vessel = max(vessels, key=lambda v: v.risk)
        
        description = f"""
            Maritime Situation Analysis:
            - Number of vessels: {len(vessels)}
            - Highest risk vessel:
            * Risk Level: {highest_risk_vessel.risk:.2f}
            * Distance: {highest_risk_vessel.distance:.2f} nautical miles
            * Bearing: {highest_risk_vessel.bearing:.1f}°
            * DCPA: {highest_risk_vessel.dcpa:.2f} nautical miles
            * TCPA: {highest_risk_vessel.tcpa:.1f} seconds

            Based on COLREGs rules, what action should be taken?"""
        
        return description.strip()
    
    def make_decision(self, vessels: List[VesselState], time_idx: int = 0) -> str:
        """Make a COLREGs-compliant decision"""
        if not self.provider:
            return "No LLM provider available"
        
        if not vessels:
            return "No vessels detected - maintain course and speed"
        
        # Format the situation
        situation_description = self._format_situation_description(vessels)
        
        # Create full prompt
        full_prompt = f"{self.system_prompt}\n\n{situation_description}"
        
        # Get response from LLM
        response = self.provider.generate_response(full_prompt)
        
        # Add provider information
        provider_info = f"[{self.provider_name.upper()}] "
        
        return f"{provider_info}{response}"
    
    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers"""
        providers = []
        
        if OpenAIProvider().is_available():
            providers.append("openai")
        
        if ClaudeProvider().is_available():
            providers.append("claude")
        
        return providers

# Backward compatibility with original interface
COLREGSInterpreter = MultiLLMCOLREGSInterpreter
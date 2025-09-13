from abc import ABC, abstractmethod
from typing import Any, Dict, List
from dataclasses import dataclass, field

# Base class for agents in the simulation
@dataclass
class Information:
    """Information to spread throughout the network"""
    topic: str
    value: float  # -1.0 to 1.0 (negative for bad news, positive for good news)
    confidence: float  # 0.0 to 1.0 (how certain the information is)
    source_id: str  # ID of the agent who originated the information
    timestamp: int = 0  # Time when the information was created

class BaseAgent(ABC):
    """Base class for all agents in the simulation network"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.beliefs: Dict[str, float] = {} # topic -> confidence in the belief
        self.connections: Dict[str, float] = {} # agent_id -> trust level (0.0 to 1.0)
        self.information_history: List[Information] = []

    @abstractmethod
    def process_information(self, info: Information, source_trust: float) -> float:
        """Process incoming information and update beliefs accordingly.
        
        Args:
            info (Information): The information being processed.
            source_trust (float): Trust level in the source agent (0.0 to 1.0).
        Returns:
            float: Updated confidence in the belief after processing the information.
        """ 
        pass

    @abstractmethod
    def decide_to_share(self, info: Information) -> bool:
        """Decide whether to share the information with connected agents.
        
        Args:
            info (Information): The information being considered for sharing.
        Returns:
            bool: True if the agent decides to share the information, False otherwise.
        """
        pass

    @abstractmethod
    def update_trust(self, other_agent_id: str, interaction_outcome: float):
        """Update trust in the source agent based on the accuracy of the information.
        
        Args:
            info (Information): The information that was shared.
        """
        pass

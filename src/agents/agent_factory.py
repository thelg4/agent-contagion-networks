import random
from typing import List

class AgentFactory:
    """Factory for creating agents with different psychological profiles"""
    
    @staticmethod
    def create_psychological_population(size: int, 
                                      trust_range: tuple = (0.3, 0.9),
                                      loss_sensitivity_range: tuple = (1.0, 2.5)) -> List[PsychologicalAgent]:
        """Create a population of psychological agents with varied psychology"""
        
        agents = []
        for i in range(size):
            trust = random.uniform(*trust_range)
            loss_sens = random.uniform(*loss_sensitivity_range)
            
            agent = PsychologicalAgent(
                agent_id=f"psych_agent_{i}",
                trust_level=trust,
                loss_sensitivity=loss_sens
            )
            agents.append(agent)
        
        return agents
    
    @staticmethod
    def create_rational_population(size: int) -> List[RationalAgent]:
        """Create a population of rational agents"""
        
        agents = []
        for i in range(size):
            agent = RationalAgent(agent_id=f"rational_agent_{i}")
            agents.append(agent)
        
        return agents
    
    @staticmethod
    def create_mixed_population(size: int, psychological_ratio: float = 0.5) -> List[BaseAgent]:
        """Create a mixed population of psychological and rational agents"""
        
        psych_count = int(size * psychological_ratio)
        rational_count = size - psych_count
        
        agents = []
        agents.extend(AgentFactory.create_psychological_population(psych_count))
        agents.extend(AgentFactory.create_rational_population(rational_count))
        
        # Shuffle to mix them up
        random.shuffle(agents)
        
        return agents
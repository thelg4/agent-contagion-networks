import random
from dataclasses import dataclass, field

@dataclass
class PsychologicalAgent(BaseAgent):
    """Agent with psychological biases from your prisoner's dilemma research"""
    
    def __init__(self, agent_id: str, trust_level: float = 0.6, loss_sensitivity: float = 1.5):
        super().__init__(agent_id)
        
        # Core psychological parameters (from your research)
        self.base_trust_level = trust_level  # 0.0 to 1.0
        self.loss_sensitivity = loss_sensitivity  # 1.0 to 3.0
        
        # Psychological state that evolves
        self.confirmation_bias = 0.3  # Tendency to accept confirming information
        self.social_proof_weight = 0.4  # How much others' beliefs matter
        self.emotional_state = 0.0  # -1.0 (stressed) to 1.0 (confident)
        
        # Initialize trust levels for new connections
        self.default_trust = trust_level
    
    def process_information(self, info: Information, source_trust: float) -> float:
        """Process information through psychological filters"""
        
        # Step 1: Apply loss aversion - negative information feels worse
        if info.value < 0:
            psychological_impact = info.value * self.loss_sensitivity
        else:
            psychological_impact = info.value
        
        # Step 2: Weight by source trust
        trusted_impact = psychological_impact * source_trust
        
        # Step 3: Apply confirmation bias
        current_belief = self.beliefs.get(info.topic, 0.0)
        
        # If information confirms existing belief, accept more readily
        if (current_belief > 0 and info.value > 0) or (current_belief < 0 and info.value < 0):
            confirmation_bonus = self.confirmation_bias
        else:
            confirmation_bonus = -self.confirmation_bias
        
        final_impact = trusted_impact + confirmation_bonus
        
        # Step 4: Update belief
        old_belief = self.beliefs.get(info.topic, 0.0)
        # Simple learning rate
        learning_rate = 0.3
        new_belief = old_belief + (learning_rate * final_impact)
        new_belief = max(-1.0, min(1.0, new_belief))  # Clamp to [-1, 1]
        
        self.beliefs[info.topic] = new_belief
        self.information_history.append(info)
        
        # Return the magnitude of belief change (for measuring cascade effects)
        return abs(new_belief - old_belief)
    
    def decide_to_share(self, info: Information) -> bool:
        """Decide whether to share information with neighbors"""
        
        # More likely to share if:
        # 1. We have strong belief about the topic
        # 2. Information is negative (loss aversion makes bad news "sticky")
        # 3. We trust the source
        
        belief_strength = abs(self.beliefs.get(info.topic, 0.0))
        source_trust = self.connections.get(info.source_id, self.default_trust)
        
        # Loss aversion: negative information is more "shareable"
        if info.value < 0:
            urgency_factor = self.loss_sensitivity
        else:
            urgency_factor = 1.0
        
        share_probability = (belief_strength * source_trust * urgency_factor) / 3.0
        
        return random.random() < share_probability
    
    def update_trust(self, other_agent_id: str, interaction_outcome: float):
        """Update trust based on interaction outcome (reuse your prisoner's dilemma logic)"""
        
        if other_agent_id not in self.connections:
            self.connections[other_agent_id] = self.default_trust
        
        current_trust = self.connections[other_agent_id]
        
        if interaction_outcome > 0:
            # Positive outcome: modest trust increase
            trust_change = 0.1 * interaction_outcome
        else:
            # Negative outcome: loss aversion amplifies trust damage
            trust_change = self.loss_sensitivity * interaction_outcome * 0.2
        
        new_trust = current_trust + trust_change
        new_trust = max(0.0, min(1.0, new_trust))  # Clamp to [0, 1]
        
        self.connections[other_agent_id] = new_trust
    
    def get_psychological_summary(self) -> Dict[str, Any]:
        """Get agent's psychological state for analysis"""
        return {
            'agent_id': self.agent_id,
            'base_trust': self.base_trust_level,
            'loss_sensitivity': self.loss_sensitivity,
            'avg_trust': sum(self.connections.values()) / len(self.connections) if self.connections else self.default_trust,
            'num_beliefs': len(self.beliefs),
            'belief_strength': sum(abs(b) for b in self.beliefs.values()) / len(self.beliefs) if self.beliefs else 0.0,
            'emotional_state': self.emotional_state
        }
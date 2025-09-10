from agents.recon_agent import ReconAgent
from agents.vuln_agent import VulnAgent
from agents.exploit_agent import ExploitAgent
from agents.analysis_agent import AnalysisAgent
from agents.executor_agent import ExecutorAgent
from agents.report_agent import ReportAgent

# State-of-the-art AI agents
from agents.webapp_agent import WebAppAgent
from agents.social_engineering_agent import SocialEngineeringAgent
from agents.crypto_analysis_agent import CryptoAnalysisAgent
from agents.iot_exploit_agent import IoTExploitAgent
from agents.payload_generation_agent import PayloadGenerationAgent
from agents.network_traffic_agent import NetworkTrafficAgent
from agents.blue_team_evasion_agent import BlueTeamEvasionAgent
from agents.lateral_movement_agent import LateralMovementAgent
from agents.data_exfiltration_agent import DataExfiltrationAgent
from agents.steganography_agent import SteganographyAgent

class AgentFactory:
    """
    🚀 Ultra-Agentic AI-Powered Agent Factory
    
    The most advanced penetration testing orchestration system with state-of-the-art AI agents.
    Intelligently selects and coordinates specialized agents based on task requirements.
    """
    def __init__(self, apis, lab_scope, tools_config):
        self.apis = apis
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.agents = {}
        self.advanced_agents = {}
        
        # Task-to-Agent mapping for intelligent selection
        self.task_agent_mapping = {
            "Full network reconnaissance": ["recon", "network_traffic"],
            "Advanced web application": ["webapp", "recon", "exploit", "payload_generation"],
            "Comprehensive vulnerability": ["recon", "vuln", "crypto_analysis"],
            "Automated exploitation": ["exploit", "payload_generation", "lateral_movement", "blue_team_evasion"],
            "Social engineering": ["social_engineering", "data_exfiltration"],
            "Cryptographic analysis": ["crypto_analysis", "network_traffic"],
            "IoT and embedded": ["iot_exploit", "network_traffic", "crypto_analysis"],
            "Lateral movement": ["lateral_movement", "exploit", "blue_team_evasion"],
            "Network traffic": ["network_traffic", "steganography", "blue_team_evasion"],
            "Steganography": ["steganography", "data_exfiltration", "blue_team_evasion"],
            "AI-powered custom payload": ["payload_generation", "exploit", "blue_team_evasion"],
            "Data exfiltration": ["data_exfiltration", "steganography", "blue_team_evasion"],
            "Blue team evasion": ["blue_team_evasion", "steganography", "payload_generation"],
            "Generate comprehensive": ["report", "analysis", "data_exfiltration"]
        }

    def _create_primary_team(self):
        """Create the core penetration testing agent team"""
        if 'recon' not in self.agents:
            print("[AgentFactory] 🚀 Creating primary agent team...")
            self.agents['recon'] = ReconAgent(self.apis, self.lab_scope, self.tools_config)
            self.agents['vuln'] = VulnAgent(self.apis, self.lab_scope, self.tools_config)
            self.agents['exploit'] = ExploitAgent(self.apis, self.lab_scope, self.tools_config)
            self.agents['analysis'] = AnalysisAgent(self.apis, self.lab_scope, self.tools_config)
            self.agents['executor'] = ExecutorAgent(self.apis, self.lab_scope, self.tools_config)
            self.agents['report'] = ReportAgent(self.apis, self.lab_scope, self.tools_config)

    def _create_advanced_agents(self):
        """Create state-of-the-art specialized agent team"""
        if 'webapp' not in self.advanced_agents:
            print("[AgentFactory] 🧬 Creating state-of-the-art AI agent team...")
            self.advanced_agents['webapp'] = WebAppAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['social_engineering'] = SocialEngineeringAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['crypto_analysis'] = CryptoAnalysisAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['iot_exploit'] = IoTExploitAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['payload_generation'] = PayloadGenerationAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['network_traffic'] = NetworkTrafficAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['blue_team_evasion'] = BlueTeamEvasionAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['lateral_movement'] = LateralMovementAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['data_exfiltration'] = DataExfiltrationAgent(self.apis, self.lab_scope, self.tools_config)
            self.advanced_agents['steganography'] = SteganographyAgent(self.apis, self.lab_scope, self.tools_config)

    def _get_agent(self, agent_name):
        """Get agent from either primary or advanced agent pools"""
        if agent_name in self.agents:
            return self.agents[agent_name]
        elif agent_name in self.advanced_agents:
            return self.advanced_agents[agent_name]
        else:
            print(f"[AgentFactory] ⚠️ Agent '{agent_name}' not found")
            return None

    def _intelligent_agent_selection(self, task):
        """AI-powered intelligent agent selection based on task requirements"""
        selected_agents = []
        
        # Analyze task keywords to determine required agents
        task_lower = task.lower()
        
        for keyword, agents in self.task_agent_mapping.items():
            if keyword.lower() in task_lower:
                selected_agents.extend(agents)
                print(f"[AgentFactory] 🧠 Detected '{keyword}' - Adding agents: {agents}")
        
        # Remove duplicates while preserving order
        unique_agents = []
        for agent in selected_agents:
            if agent not in unique_agents:
                unique_agents.append(agent)
        
        # If no specific agents found, use default comprehensive approach
        if not unique_agents:
            unique_agents = ['recon', 'vuln', 'exploit', 'analysis', 'report']
            print("[AgentFactory] 🧠 Using comprehensive default agent set")
        
        return unique_agents

    def execute_task_flow(self, context, max_iterations=3):
        """
        🚀 AI-Powered Task Execution Flow
        Intelligently orchestrates agents based on task requirements
        """
        self._create_primary_team()
        self._create_advanced_agents()
        
        # Intelligent agent selection
        required_agents = self._intelligent_agent_selection(context['task'])
        print(f"[AgentFactory] 🧠 Selected agents: {required_agents}")
        
        # Execute agents in intelligent order
        for agent_name in required_agents:
            agent = self._get_agent(agent_name)
            if agent:
                print(f"\n[AgentFactory] 🎯 Executing {agent_name.upper()} agent...")
                try:
                    if agent_name == 'recon':
                        context['recon']['results'] = agent.run(context['task'])
                        context['recon']['status'] = 'complete'
                    elif agent_name == 'vuln':
                        context['vuln']['results'] = agent.run(context['recon']['results'])
                        context['vuln']['status'] = 'complete'
                    elif agent_name == 'exploit':
                        context['exploit']['results'] = agent.run(context['vuln']['results'])
                        context['exploit']['status'] = 'complete'
                    elif agent_name == 'analysis':
                        context['analysis']['results'] = agent.run(context['exploit']['results'])
                        context['analysis']['status'] = 'complete'
                    elif agent_name == 'executor':
                        context['execution']['results'] = agent.run(context['analysis']['results'])
                        context['execution']['status'] = 'complete'
                    elif agent_name == 'report':
                        context['report']['results'] = agent.run(context)
                        context['report']['status'] = 'complete'
                    else:
                        # Advanced agents
                        results = agent.run(context)
                        context[agent_name] = {"status": "complete", "results": results}
                    
                    context['history'].append(f"{agent_name.title()} agent completed successfully")
                    print(f"[AgentFactory] ✅ {agent_name.upper()} agent completed")
                except Exception as e:
                    print(f"[AgentFactory] ❌ {agent_name.upper()} agent failed: {e}")
                    context['history'].append(f"{agent_name.title()} agent failed: {str(e)}")

        print("\n[AgentFactory] 🎉 AI-powered task execution completed!")

    def execute_custom_task_flow(self, context, custom_config):
        """
        🎲 Custom Task Execution Flow
        Handles user-defined custom penetration testing objectives
        """
        self._create_primary_team()
        self._create_advanced_agents()
        
        print(f"[AgentFactory] 🎲 Executing custom task: {custom_config['task']}")
        
        # Intelligent agent selection for custom task
        required_agents = self._intelligent_agent_selection(custom_config['task'])
        
        # Add additional context for custom targets
        if custom_config.get('target'):
            context['custom_targets'] = [custom_config['target']]
        
        print(f"[AgentFactory] 🧠 Custom task requires agents: {required_agents}")
        
        # Execute selected agents
        for agent_name in required_agents:
            agent = self._get_agent(agent_name)
            if agent:
                print(f"[AgentFactory] 🎯 Running {agent_name.upper()} for custom task...")
                try:
                    results = agent.run(context)
                    context[f"custom_{agent_name}"] = {"status": "complete", "results": results}
                    context['history'].append(f"Custom {agent_name} execution completed")
                except Exception as e:
                    print(f"[AgentFactory] ❌ Custom {agent_name} failed: {e}")
                    context['history'].append(f"Custom {agent_name} failed: {str(e)}")

        print(f"[AgentFactory] 🎉 Custom task '{custom_config['task']}' completed!")

    def create_and_run_sub_team(self, sub_task, context):
        """
        🔥 Dynamic Sub-Team Creation
        Creates specialized agent teams for complex sub-tasks
        """
        print(f"[AgentFactory] 🔥 Spawning AI sub-team for: {sub_task}")
        
        # Intelligent sub-agent selection
        sub_agents = self._intelligent_agent_selection(sub_task)
        sub_results = {}
        
        for agent_name in sub_agents[:3]:  # Limit sub-team size
            agent = self._get_agent(agent_name)
            if agent:
                try:
                    result = agent.run(context)
                    sub_results[agent_name] = result
                    print(f"[AgentFactory] 🔥 Sub-agent {agent_name} completed")
                except Exception as e:
                    print(f"[AgentFactory] ❌ Sub-agent {agent_name} failed: {e}")
        
        context['history'].append(f"Sub-team executed for: {sub_task}")
        return {"sub_task": sub_task, "results": sub_results, "confidence": 0.95}

    def get_available_agents(self):
        """Return list of all available agents"""
        primary = list(self.agents.keys()) if self.agents else ['recon', 'vuln', 'exploit', 'analysis', 'executor', 'report']
        advanced = ['webapp', 'social_engineering', 'crypto_analysis', 'iot_exploit', 'payload_generation', 
                   'network_traffic', 'blue_team_evasion', 'lateral_movement', 'data_exfiltration', 'steganography']
        return {"primary": primary, "advanced": advanced}

    def get_agent_capabilities(self, agent_name):
        """Return capabilities of a specific agent"""
        capabilities = {
            "webapp": "🌐 Advanced web application security testing",
            "social_engineering": "🕵️ OSINT and social engineering analysis", 
            "crypto_analysis": "🔐 Cryptographic security assessment",
            "iot_exploit": "📱 IoT and embedded device exploitation",
            "payload_generation": "🧬 AI-powered custom payload creation",
            "network_traffic": "📊 Network traffic analysis and monitoring",
            "blue_team_evasion": "🛡️ Anti-forensics and detection evasion",
            "lateral_movement": "🔄 Network pivoting and privilege escalation",
            "data_exfiltration": "💾 Sensitive data discovery and exfiltration",
            "steganography": "🎭 Covert communications and data hiding"
        }
        return capabilities.get(agent_name, "Standard penetration testing agent")
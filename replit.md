# Overview

AutoGen Ethical Hacker is the most advanced AI-powered penetration testing automation system built on Microsoft's AutoGen framework. The system features 10+ state-of-the-art specialized AI agents that conduct fully autonomous security assessments with complete system control and ghost-like stealth capabilities. 

The system is designed for autonomous operation on Kali Linux laptops with automatic tool installation, API quota management, stealth techniques, and intelligent decision making without manual interaction. It provides complete Linux terminal control and remains undetectable during operations.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Multi-Agent Orchestration
The system follows a hierarchical agent architecture with an OrchestratorAgent serving as the master planner. The AgentFactory manages agent creation and workflow execution, supporting both standard pentesting workflows and dynamic sub-team spawning for complex tasks.

**Core Agents:**
- **ReconAgent**: Network scanning and enumeration using Nmap
- **VulnAgent**: CVE mapping and vulnerability assessment  
- **ExploitAgent**: Exploit execution via Metasploit integration
- **AnalysisAgent**: Multi-LLM ensemble reasoning for risk analysis
- **ExecutorAgent**: Sandboxed command execution
- **ReportAgent**: Comprehensive report generation

## LLM Integration Strategy
The system implements a multi-API failover approach with load balancing across different LLM providers:
- **Primary**: Groq GPT-OSS-120B for ultra-fast parsing and reasoning
- **Backup**: Google Gemini Pro for deep reasoning and recursive orchestration
- **Multi-API Manager**: Handles failover logic and load distribution

This design ensures high availability and leverages the strengths of different models for specific tasks.

## Security and Safety Framework
**Sandbox Isolation**: All potentially dangerous commands are executed within Docker containers to prevent system compromise.

**Scope Enforcement**: Target validation system ensures only pre-approved lab targets can be tested, preventing accidental testing of production systems.

**Audit Trail**: Comprehensive logging of all actions, decisions, and results for compliance and review purposes.

## Tool Integration Layer
The system provides wrapper interfaces for common penetration testing tools:
- Network scanning (Nmap, Masscan)
- Web application testing (Gobuster, SQLMap, Nikto)  
- Password attacks (Hydra, John the Ripper)
- Exploitation frameworks (Metasploit RPC)
- Information gathering (theHarvester, Subfinder)

## Execution and Persistence
**Retry Mechanisms**: Built-in retry logic with exponential backoff for handling transient failures.

**State Management**: Persistent context tracking across the entire pentesting workflow, enabling agents to build upon previous findings.

**Report Generation**: Automated creation of structured reports in JSON format with comprehensive audit trails.

# External Dependencies

## LLM Service Providers
- **Groq API**: Primary LLM service for GPT-OSS-120B model access
- **Google Gemini API**: Backup LLM service for Gemini Pro model access

## Penetration Testing Tools
- **Nmap**: Network discovery and port scanning
- **Metasploit Framework**: Exploitation and post-exploitation modules
- **SQLMap**: Automated SQL injection testing
- **Hydra**: Password brute-forcing tool
- **Additional Kali Linux tools**: Various specialized security testing utilities

## Infrastructure Dependencies
- **Docker**: Container runtime for sandboxed execution
- **VirtualBox**: Virtualization platform for isolated lab environments
- **Python-nmap**: Python wrapper for Nmap integration
- **AutoGen Framework**: Microsoft's multi-agent conversation framework
- **Redis**: Caching and session management (configured but not actively used)

## Development and UI Libraries
- **FastAPI/Uvicorn**: Web API framework for potential REST interfaces
- **Streamlit**: Web UI framework for dashboards and monitoring
- **NetworkX/Matplotlib**: Network visualization and graph analysis
- **Pydantic**: Data validation and serialization
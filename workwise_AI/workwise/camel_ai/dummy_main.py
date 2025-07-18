import os
import json
import requests
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import google.generativeai as genai

api_key = "AIzaSyB0A8MFwq-y1gaH2WmcClMkwxwujfWjmSM"
# Configure Gemini API
genai.configure(api_key=api_key)

class MessageType(Enum):
    TASK_ASSIGNMENT = "task_assignment"
    TOOL_REQUEST = "tool_request"
    TOOL_RESPONSE = "tool_response"
    COLLABORATION = "collaboration"
    RESULT = "result"

@dataclass
class Message:
    sender: str
    receiver: str
    message_type: MessageType
    content: str
    timestamp: float
    metadata: Dict[str, Any] = None

    def to_dict(self):
        return asdict(self)

class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class WebSearchTool(Tool):
    def __init__(self):
        super().__init__("web_search", "Search the web for information")
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query", "")
        # Simulated web search - in real implementation, use actual search API
        results = [
            f"Search result 1 for '{query}': Lorem ipsum dolor sit amet",
            f"Search result 2 for '{query}': Consectetur adipiscing elit",
            f"Search result 3 for '{query}': Sed do eiusmod tempor incididunt"
        ]
        return {
            "status": "success",
            "results": results,
            "query": query
        }

class DataAnalysisTool(Tool):
    def __init__(self):
        super().__init__("data_analysis", "Analyze data and generate insights")
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        data = params.get("data", [])
        analysis_type = params.get("type", "summary")
        
        if analysis_type == "summary":
            return {
                "status": "success",
                "analysis": {
                    "total_records": len(data),
                    "data_type": type(data).__name__,
                    "summary": "Data analysis completed successfully"
                }
            }
        elif analysis_type == "trend":
            return {
                "status": "success",
                "analysis": {
                    "trend": "upward",
                    "confidence": 0.85,
                    "insights": ["Positive growth trend detected", "Data shows consistent improvement"]
                }
            }

class CodeGenerationTool(Tool):
    def __init__(self):
        super().__init__("code_generation", "Generate code based on requirements")
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        language = params.get("language", "python")
        requirements = params.get("requirements", "")
        
        # Simulated code generation
        if language == "python":
            code = f"""
def solve_problem():
    # Generated code for: {requirements}
    print("Solution implemented")
    return "success"

if __name__ == "__main__":
    solve_problem()
"""
        else:
            code = f"// Generated {language} code for: {requirements}"
        
        return {
            "status": "success",
            "code": code,
            "language": language,
            "requirements": requirements
        }

class Agent:
    def __init__(self, name: str, role: str, specialization: str):
        self.name = name
        self.role = role
        self.specialization = specialization
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Using Gemini 1.5 Flash
        self.message_history = []
        self.tools = {}
    
    def add_tool(self, tool: Tool):
        self.tools[tool.name] = tool
    
    def process_message(self, message: Message) -> Optional[Message]:
        self.message_history.append(message)
        
        # Create context for the AI model
        context = self._build_context(message)
        
        try:
            response = self.model.generate_content(context)
            response_text = response.text
            
            # Parse response for tool usage or collaboration
            if "TOOL_USE:" in response_text:
                return self._handle_tool_request(response_text, message.sender)
            elif "COLLABORATE:" in response_text:
                return self._handle_collaboration(response_text, message.sender)
            else:
                return Message(
                    sender=self.name,
                    receiver=message.sender,
                    message_type=MessageType.RESULT,
                    content=response_text,
                    timestamp=time.time()
                )
        except Exception as e:
            return Message(
                sender=self.name,
                receiver=message.sender,
                message_type=MessageType.RESULT,
                content=f"Error processing message: {str(e)}",
                timestamp=time.time()
            )
    
    def _build_context(self, message: Message) -> str:
        context = f"""
You are {self.name}, a {self.role} specialized in {self.specialization}.

Available tools:
{', '.join(self.tools.keys())}

Recent message history:
{self._format_message_history()}

Current message from {message.sender}:
{message.content}

Instructions:
1. If you need to use a tool, respond with: TOOL_USE: tool_name {{"param": "value"}}
2. If you need to collaborate with another agent, respond with: COLLABORATE: agent_name message
3. Otherwise, provide a direct response to complete the task.

Response:
"""
        return context
    
    def _format_message_history(self) -> str:
        recent_messages = self.message_history[-5:]  # Last 5 messages
        formatted = []
        for msg in recent_messages:
            formatted.append(f"{msg.sender}: {msg.content}")
        return "\n".join(formatted)
    
    def _handle_tool_request(self, response_text: str, original_sender: str) -> Message:
        try:
            # Parse tool request
            tool_part = response_text.split("TOOL_USE:")[1].strip()
            parts = tool_part.split(" ", 1)
            tool_name = parts[0]
            params = json.loads(parts[1]) if len(parts) > 1 else {}
            
            if tool_name in self.tools:
                result = self.tools[tool_name].execute(params)
                return Message(
                    sender=self.name,
                    receiver=original_sender,
                    message_type=MessageType.TOOL_RESPONSE,
                    content=f"Tool {tool_name} executed: {json.dumps(result)}",
                    timestamp=time.time()
                )
        except Exception as e:
            return Message(
                sender=self.name,
                receiver=original_sender,
                message_type=MessageType.RESULT,
                content=f"Tool execution failed: {str(e)}",
                timestamp=time.time()
            )
    
    def _handle_collaboration(self, response_text: str, original_sender: str) -> Message:
        try:
            # Parse collaboration request
            collab_part = response_text.split("COLLABORATE:")[1].strip()
            parts = collab_part.split(" ", 1)
            target_agent = parts[0]
            message_content = parts[1] if len(parts) > 1 else ""
            
            return Message(
                sender=self.name,
                receiver=target_agent,
                message_type=MessageType.COLLABORATION,
                content=message_content,
                timestamp=time.time()
            )
        except Exception as e:
            return Message(
                sender=self.name,
                receiver=original_sender,
                message_type=MessageType.RESULT,
                content=f"Collaboration failed: {str(e)}",
                timestamp=time.time()
            )

class CAMELSystem:
    def __init__(self):
        self.agents = {}
        self.tools = {}
        self.message_queue = []
        self.completed_tasks = []
        
        # Initialize tools
        self.tools["web_search"] = WebSearchTool()
        self.tools["data_analysis"] = DataAnalysisTool()
        self.tools["code_generation"] = CodeGenerationTool()
        
        # Initialize agents
        self.agents["researcher"] = Agent(
            "researcher", 
            "Research Specialist", 
            "information gathering and analysis"
        )
        self.agents["developer"] = Agent(
            "developer", 
            "Software Developer", 
            "coding and technical implementation"
        )
        self.agents["analyst"] = Agent(
            "analyst", 
            "Data Analyst", 
            "data processing and insights generation"
        )
        
        # Assign tools to agents
        self.agents["researcher"].add_tool(self.tools["web_search"])
        self.agents["developer"].add_tool(self.tools["code_generation"])
        self.agents["analyst"].add_tool(self.tools["data_analysis"])
        
        # Cross-assign some tools for collaboration
        self.agents["researcher"].add_tool(self.tools["data_analysis"])
        self.agents["analyst"].add_tool(self.tools["web_search"])
    
    def add_task(self, task_description: str, assigned_agent: str):
        message = Message(
            sender="system",
            receiver=assigned_agent,
            message_type=MessageType.TASK_ASSIGNMENT,
            content=task_description,
            timestamp=time.time()
        )
        self.message_queue.append(message)
    
    def process_messages(self):
        while self.message_queue:
            message = self.message_queue.pop(0)
            
            if message.receiver in self.agents:
                agent = self.agents[message.receiver]
                response = agent.process_message(message)
                
                if response:
                    if response.receiver in self.agents:
                        self.message_queue.append(response)
                    else:
                        # Task completed
                        self.completed_tasks.append({
                            "task": message.content,
                            "result": response.content,
                            "agent": message.receiver,
                            "timestamp": response.timestamp
                        })
                        print(f"Task completed by {message.receiver}:")
                        print(f"Result: {response.content}")
                        print("-" * 50)
            
            # Prevent infinite loops
            if len(self.message_queue) > 100:
                break
    
    def run_demo(self):
        print("🐪 CAMEL AI System Demo")
        print("=" * 50)
        
        # Task 1: Research and Analysis
        print("\n📝 Task 1: Research latest AI trends")
        self.add_task(
            "Research the latest trends in artificial intelligence for 2024-2025. Focus on multi-agent systems and their applications.",
            "researcher"
        )
        
        # Task 2: Data Analysis
        print("\n📊 Task 2: Analyze sample data")
        self.add_task(
            "Analyze the following sample data for trends: [100, 120, 135, 150, 180, 200, 220]. Generate insights and recommendations.",
            "analyst"
        )
        
        # Task 3: Code Generation
        print("\n💻 Task 3: Generate Python code")
        self.add_task(
            "Generate Python code for a simple multi-agent communication system with message passing capabilities.",
            "developer"
        )
        
        # Process all tasks
        self.process_messages()
        
        # Display summary
        print("\n📋 Summary of Completed Tasks:")
        print("=" * 50)
        for i, task in enumerate(self.completed_tasks, 1):
            print(f"Task {i}: {task['task'][:50]}...")
            print(f"Agent: {task['agent']}")
            print(f"Status: Completed")
            print("-" * 30)
        
        return self.completed_tasks

# Usage example
if __name__ == "__main__":
    # Check if API key is available
    if not api_key:
        print("Please set your GEMINI_API_KEY in your .env file")
        print("Create a .env file with: GEMINI_API_KEY=your_api_key_here")
        exit(1)
    
    # Create and run the CAMEL system
    camel_system = CAMELSystem()
    results = camel_system.run_demo()
    
    print(f"\n✅ Demo completed! {len(results)} tasks processed.")
import os
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class MessageType(Enum):
    TASK_ASSIGNMENT = "task_assignment"
    TOOL_REQUEST = "tool_request"
    TOOL_RESPONSE = "tool_response"
    COLLABORATION = "collaboration"
    RESULT = "result"
    ANALYSIS_COMPLETE = "analysis_complete"

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

@dataclass
class TicketData:
    ticket_id: str
    title: str
    description: str
    priority: str
    required_skills: List[str]
    estimated_hours: int
    deadline: str
    category: str

@dataclass
class EmployeeProfile:
    employee_id: str
    name: str
    skills: List[str]
    skill_levels: Dict[str, int]  # skill -> level (1-5)
    availability: Dict[str, bool]  # date -> available
    current_workload: int
    max_capacity: int
    department: str
    experience_years: int

class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class BaseAgent:
    def __init__(self, name: str, role: str, specialization: str):
        self.name = name
        self.role = role
        self.specialization = specialization
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.message_history = []
        self.tools = {}
    
    def add_tool(self, tool: Tool):
        self.tools[tool.name] = tool
    
    def process_message(self, message: Message) -> Optional[Message]:
        self.message_history.append(message)
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
                    timestamp=time.time(),
                    metadata={"analysis_type": self.specialization}
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
        recent_messages = self.message_history[-5:]
        formatted = []
        for msg in recent_messages:
            formatted.append(f"{msg.sender}: {msg.content}")
        return "\n".join(formatted)
    
    def _handle_tool_request(self, response_text: str, original_sender: str) -> Message:
        try:
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
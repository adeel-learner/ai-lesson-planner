from langchain_core.callbacks.base import BaseCallbackHandler
import tiktoken
from typing import Any, Dict, List, Optional, Union
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish

class TokenCounterHandler(BaseCallbackHandler):
    """
    Callback handler for counting tokens in LLM interactions.
    
    Supports:
    - Action agent flows with multiple LLM calls
    - Agent tool calls and their outputs
    - Streaming token generation
    - Both OpenAI and non-OpenAI models
    - Accumulation across agent steps
    - Chain and agent lifecycle tracking
    """
    
    def __init__(self):
        self.tokens = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        # For non-OpenAI models that don't report token counts
        self.encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
        
        # Track tokens per LLM call for debugging
        self.call_count = 0
        self.tokens_per_call = []
        
        # For streaming token tracking
        self.current_completion_tokens = 0
        self.streaming_mode = False
        
        # Track agent actions and tools
        self.tool_calls = 0
        self.agent_steps = 0
    
    def on_llm_start(
        self, 
        serialized: Dict[str, Any], 
        prompts: List[str], 
        **kwargs: Any
    ) -> None:
        """Calculate prompt tokens when LLM starts."""
        self.call_count += 1
        self.current_completion_tokens = 0
        self.streaming_mode = False
        
        call_prompt_tokens = 0
        # For models that don't report tokens, estimate
        for prompt in prompts:
            try:
                # Estimate token count
                call_prompt_tokens += len(self.encoder.encode(prompt))
            except Exception:
                # Fallback: rough estimation (4 chars per token)
                call_prompt_tokens += len(prompt) // 4
        
        self.tokens["prompt_tokens"] += call_prompt_tokens
    
    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any,
    ) -> None:
        """Calculate prompt tokens when chat model starts."""
        self.call_count += 1
        self.current_completion_tokens = 0
        self.streaming_mode = False
        
        call_prompt_tokens = 0
        # Process chat messages
        for message_list in messages:
            for message in message_list:
                try:
                    # Get message content
                    content = message.content if hasattr(message, 'content') else str(message)
                    call_prompt_tokens += len(self.encoder.encode(content))
                except Exception:
                    # Fallback estimation
                    content = message.content if hasattr(message, 'content') else str(message)
                    call_prompt_tokens += len(content) // 4
        
        self.tokens["prompt_tokens"] += call_prompt_tokens
    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Track tokens during streaming generation."""
        self.streaming_mode = True
        try:
            # Count the token
            token_count = len(self.encoder.encode(token))
            self.current_completion_tokens += token_count
        except Exception as e:
            # Fallback: count as 1 token
            self.current_completion_tokens += 1
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Record tokens reported by LLM or estimate if not available."""
        call_completion_tokens = 0
        
        # First, try to get official token counts from response
        if hasattr(response, "llm_output") and response.llm_output and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]
            
            # For action agent, we accumulate across multiple calls
            # So we add the completion tokens from this call
            call_completion_tokens = token_usage.get("completion_tokens", 0)
            
            # Update cumulative totals
            self.tokens["completion_tokens"] += call_completion_tokens
        else:
            # Model doesn't report tokens - use our estimates
            if self.streaming_mode and self.current_completion_tokens > 0:
                # Use streaming count
                call_completion_tokens = self.current_completion_tokens
            elif hasattr(response, "generations") and response.generations:
                # Estimate from generated text
                for gen in response.generations:
                    for g in gen:
                        try:
                            call_completion_tokens += len(self.encoder.encode(g.text))
                        except Exception:
                            # Fallback estimation
                            call_completion_tokens += len(g.text) // 4
            
            self.tokens["completion_tokens"] += call_completion_tokens
        
        # Update total
        self.tokens["total_tokens"] = self.tokens["prompt_tokens"] + self.tokens["completion_tokens"]
        
        # Store per-call statistics
        self.tokens_per_call.append({
            "call": self.call_count,
            "prompt_tokens": call_completion_tokens,  # Only this call's contribution
            "completion_tokens": call_completion_tokens
        })
    
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Called when a chain (including agent) starts."""
        pass
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Called when a chain (including agent) ends."""
        pass
    
    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when a chain encounters an error."""
        pass
    
    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> None:
        """Called when agent decides to take an action (use a tool)."""
        self.agent_steps += 1
        self.tool_calls += 1
        
        # Count tokens in the tool input
        tool_input_str = str(action.tool_input)
        try:
            tool_input_tokens = len(self.encoder.encode(tool_input_str))
            self.tokens["prompt_tokens"] += tool_input_tokens
        except Exception:
            # Fallback estimation
            tool_input_tokens = len(tool_input_str) // 4
            self.tokens["prompt_tokens"] += tool_input_tokens
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Called when agent finishes its execution."""
        # Count tokens in the final output
        output_str = str(finish.return_values)
        try:
            output_tokens = len(self.encoder.encode(output_str))
            self.tokens["completion_tokens"] += output_tokens
            self.tokens["total_tokens"] = self.tokens["prompt_tokens"] + self.tokens["completion_tokens"]
        except Exception:
            # Fallback estimation
            output_tokens = len(output_str) // 4
            self.tokens["completion_tokens"] += output_tokens
            self.tokens["total_tokens"] = self.tokens["prompt_tokens"] + self.tokens["completion_tokens"]
    
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """Called when a tool starts execution."""
        pass
    
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Called when a tool finishes execution."""
        # Count tokens in tool output
        try:
            tool_output_tokens = len(self.encoder.encode(output))
            self.tokens["completion_tokens"] += tool_output_tokens
            self.tokens["total_tokens"] = self.tokens["prompt_tokens"] + self.tokens["completion_tokens"]
        except Exception:
            # Fallback estimation
            tool_output_tokens = len(output) // 4
            self.tokens["completion_tokens"] += tool_output_tokens
            self.tokens["total_tokens"] = self.tokens["prompt_tokens"] + self.tokens["completion_tokens"]
    
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when a tool encounters an error."""
        pass
    
    def on_text(self, text: str, **kwargs: Any) -> None:
        """Called when arbitrary text is generated (e.g., agent reasoning)."""
        # Count tokens in intermediate text
        try:
            text_tokens = len(self.encoder.encode(text))
            # This could be either prompt or completion depending on context
            # For safety, we'll add to completion tokens as it's usually agent output
            if text_tokens > 10:  # Only count substantial text
                self.tokens["completion_tokens"] += text_tokens
                self.tokens["total_tokens"] = self.tokens["prompt_tokens"] + self.tokens["completion_tokens"]
        except Exception:
            pass  # Silent fail for on_text to avoid noise
    
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Called when LLM encounters an error."""
        pass
    
    def get_token_count(self) -> Dict[str, int]:
        """Get the current token count."""
        return self.tokens.copy()
    
    def reset(self) -> None:
        """Reset token counters for a new conversation/query."""
        self.tokens = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        self.call_count = 0
        self.tokens_per_call = []
        self.current_completion_tokens = 0
        self.streaming_mode = False
        self.tool_calls = 0
        self.agent_steps = 0
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed statistics including per-call breakdown."""
        return {
            "total": self.tokens.copy(),
            "num_calls": self.call_count,
            "tool_calls": self.tool_calls,
            "agent_steps": self.agent_steps,
            "per_call": self.tokens_per_call.copy(),
            "average_per_call": {
                "prompt_tokens": self.tokens["prompt_tokens"] / self.call_count if self.call_count > 0 else 0,
                "completion_tokens": self.tokens["completion_tokens"] / self.call_count if self.call_count > 0 else 0
            }
        }
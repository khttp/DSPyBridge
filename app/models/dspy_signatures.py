"""
DSPy signatures for different AI tasks
"""
import dspy


class BasicChat(dspy.Signature):
    """Basic chat completion signature."""
    message = dspy.InputField(desc="User message")
    response = dspy.OutputField(desc="Assistant response")


class QuestionAnswering(dspy.Signature):
    """Question answering signature."""
    question = dspy.InputField(desc="User question")
    context = dspy.InputField(desc="Relevant context", format=lambda x: x if x else "No additional context provided.")
    answer = dspy.OutputField(desc="Answer to the question")


class ChainOfThoughtQA(dspy.Signature):
    """Chain of thought question answering."""
    question = dspy.InputField(desc="User question")
    context = dspy.InputField(desc="Relevant context", format=lambda x: x if x else "No additional context provided.")
    reasoning = dspy.OutputField(desc="Step-by-step reasoning")
    answer = dspy.OutputField(desc="Final answer")


class RetrievalEnhanced(dspy.Signature):
    """Retrieval-enhanced generation signature."""
    query = dspy.InputField(desc="User query")
    context = dspy.InputField(desc="Retrieved context documents")
    response = dspy.OutputField(desc="Response based on retrieved context")


class ReActAgent(dspy.Signature):
    """ReAct (Reasoning + Acting) agent signature."""
    message = dspy.InputField(desc="User message")
    available_tools = dspy.InputField(desc="Available tools description")
    thought = dspy.OutputField(desc="Reasoning about what action to take")
    action = dspy.OutputField(desc="Action to take: 'joke_api', 'direct_response', or 'none'")
    response = dspy.OutputField(desc="Response to user or tool call description")

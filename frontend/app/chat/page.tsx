"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  intent?: string;
  suggested_actions?: string[];
}

// Simulated AI responses for demo
const demoResponses: Record<string, string> = {
  default: `Hello! I'm your AI assistant for property maintenance services. I can help you with:

- Scheduling service appointments
- Getting estimates for HVAC, plumbing, electrical work
- Answering questions about our services
- Handling urgent maintenance requests

How can I help you today?`,
  schedule: `I'd be happy to help you schedule an appointment! To get you set up, I'll need:

1. **Service type**: What kind of maintenance do you need? (HVAC, plumbing, electrical, etc.)
2. **Description**: Can you briefly describe the issue?
3. **Preferred time**: When would work best for you?

What service do you need help with?`,
  hvac: `For HVAC services, we offer:

- **AC Repair & Maintenance** - Starting at $89
- **Heating System Service** - Starting at $99
- **Full System Inspection** - $149
- **Emergency Service** - Available 24/7

Our technicians are certified and can usually come out within 24-48 hours. Would you like to schedule a service visit?`,
  emergency: `I understand this is urgent! For emergencies like gas leaks, flooding, or electrical hazards:

**Please call our 24/7 emergency line immediately.**

A technician will be dispatched as soon as possible. Can you tell me more about the emergency so I can prioritize appropriately?`,
  price: `Our pricing depends on the service type:

| Service | Starting Price |
|---------|---------------|
| HVAC | $89 |
| Plumbing | $79 |
| Electrical | $99 |
| Roofing | $149 |
| General Repairs | $69 |

Would you like a detailed estimate for a specific service?`,
};

function getAIResponse(message: string): { response: string; intent: string } {
  const lower = message.toLowerCase();

  if (lower.includes("emergency") || lower.includes("urgent") || lower.includes("leak")) {
    return { response: demoResponses.emergency, intent: "emergency" };
  }
  if (lower.includes("schedule") || lower.includes("appointment") || lower.includes("book")) {
    return { response: demoResponses.schedule, intent: "scheduling" };
  }
  if (lower.includes("hvac") || lower.includes("ac") || lower.includes("heating") || lower.includes("cooling")) {
    return { response: demoResponses.hvac, intent: "inquiry" };
  }
  if (lower.includes("price") || lower.includes("cost") || lower.includes("how much")) {
    return { response: demoResponses.price, intent: "inquiry" };
  }

  return { response: demoResponses.default, intent: "general" };
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: "assistant",
      content: demoResponses.default,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const { response, intent } = getAIResponse(userMessage.content);

    const assistantMessage: Message = {
      id: messages.length + 2,
      role: "assistant",
      content: response,
      timestamp: new Date(),
      intent,
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="bg-primary-100 p-2 rounded-lg">
            <Bot className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 className="font-semibold text-gray-900">AI Assistant</h1>
            <p className="text-sm text-gray-500">
              Property maintenance support powered by AI
            </p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            <span className="text-sm text-gray-500">Online</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-6 space-y-6">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              "flex gap-3",
              message.role === "user" ? "flex-row-reverse" : ""
            )}
          >
            <div
              className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
                message.role === "user"
                  ? "bg-primary-600"
                  : "bg-gray-100"
              )}
            >
              {message.role === "user" ? (
                <User className="w-5 h-5 text-white" />
              ) : (
                <Bot className="w-5 h-5 text-gray-600" />
              )}
            </div>
            <div
              className={cn(
                "max-w-[70%] rounded-2xl px-4 py-3",
                message.role === "user"
                  ? "bg-primary-600 text-white"
                  : "bg-white border border-gray-200"
              )}
            >
              <p className="whitespace-pre-wrap text-sm">{message.content}</p>
              {message.intent && message.role === "assistant" && (
                <p className="text-xs mt-2 opacity-60">
                  Intent: {message.intent}
                </p>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
              <Bot className="w-5 h-5 text-gray-600" />
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
              <Loader2 className="w-5 h-5 animate-spin text-gray-400" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="input flex-1"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
            Send
          </button>
        </form>
        <p className="text-xs text-gray-400 mt-2 text-center">
          Try asking about scheduling, pricing, or describe your maintenance issue
        </p>
      </div>
    </div>
  );
}

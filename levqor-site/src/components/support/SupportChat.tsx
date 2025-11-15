"use client";

import { useState, useRef, useEffect } from "react";
import { callPublicSupport, callPrivateSupport, escalateSupport, SupportReply } from "@/lib/supportClient";

interface Message {
  id: string;
  from: "user" | "bot";
  text: string;
}

type Mode = "public" | "private";

interface SupportChatProps {
  mode: Mode;
  title?: string;
  showEscalate?: boolean;
  defaultEmail?: string;
}

export default function SupportChat({ mode, title, showEscalate = false, defaultEmail }: SupportChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      from: "bot",
      text: mode === "public" 
        ? "Hi! I'm the Levqor Support AI. How can I help you today?" 
        : "Hi! I can help with your account, orders, and automations. What do you need help with?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      from: "user",
      text: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      let reply: SupportReply;

      if (mode === "public") {
        reply = await callPublicSupport(userMessage.text, conversationId);
      } else {
        reply = await callPrivateSupport(userMessage.text, defaultEmail, conversationId);
      }

      if (reply.conversationId) {
        setConversationId(reply.conversationId);
      }

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        from: "bot",
        text: reply.reply,
      };

      setMessages((prev) => [...prev, botMessage]);

      if (reply.escalationSuggested && showEscalate) {
        const escalateMessage: Message = {
          id: (Date.now() + 2).toString(),
          from: "bot",
          text: "It looks like you might need more help. Would you like to escalate this to our support team?",
        };
        setMessages((prev) => [...prev, escalateMessage]);
      }
    } catch (err) {
      setError("Failed to get response. Please try again or email support@levqor.ai");
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        from: "bot",
        text: "I'm having trouble connecting right now. Please try again or email support@levqor.ai for assistance.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleEscalate = async () => {
    let email = defaultEmail;
    if (!email) {
      email = window.prompt("Please enter your email address:") || "";
      if (!email) return;
    }

    const userMessages = messages.filter((m) => m.from === "user");
    const summary = userMessages.slice(-3).map((m) => m.text).join(" | ");

    setLoading(true);
    setError(null);

    try {
      const result = await escalateSupport(email, summary, { source: "chat", mode });
      
      const ticketMessage: Message = {
        id: Date.now().toString(),
        from: "bot",
        text: `✅ Support ticket created: #${result.ticketId}. Our team will respond within 24 hours via email.`,
      };
      setMessages((prev) => [...prev, ticketMessage]);
    } catch (err) {
      setError("Failed to create ticket. Please email support@levqor.ai directly.");
      const errorMessage: Message = {
        id: Date.now().toString(),
        from: "bot",
        text: "I couldn't create a ticket right now. Please email support@levqor.ai directly.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 rounded-lg border border-slate-700 overflow-hidden">
      {title && (
        <div className="px-4 py-3 bg-slate-800 border-b border-slate-700">
          <h3 className="font-semibold text-sm text-slate-100">{title}</h3>
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] px-4 py-2 rounded-lg ${
                msg.from === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-800 text-slate-100 border border-slate-700"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 border border-slate-700 px-4 py-2 rounded-lg">
              <p className="text-sm text-slate-400">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="px-4 py-2 bg-red-900/20 border-t border-red-800/50">
          <p className="text-xs text-red-400">{error}</p>
        </div>
      )}

      <div className="p-4 bg-slate-800 border-t border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={loading}
            className="flex-1 px-3 py-2 bg-slate-900 border border-slate-600 rounded text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white text-sm font-medium rounded transition-colors"
          >
            Send
          </button>
        </div>

        {showEscalate && (
          <button
            onClick={handleEscalate}
            disabled={loading}
            className="mt-2 w-full px-3 py-2 bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:cursor-not-allowed text-slate-200 text-xs font-medium rounded transition-colors"
          >
            Escalate to Human Support
          </button>
        )}

        <p className="mt-2 text-xs text-slate-500 text-center">
          Powered by AI. For sensitive issues, email support@levqor.ai
        </p>
      </div>
    </div>
  );
}

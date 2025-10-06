import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { ScrollArea } from "./components/ui/scroll-area";
import { Badge } from "./components/ui/badge";
import { ChatMessage } from "./components/ChatMessage";
import { ChatInput } from "./components/ChatInput";
import { Stethoscope, User } from "lucide-react";

interface FileInfo {
  name: string;
  size: number;
  type: string;
  file?: File;
  url?: string;
}

interface Message {
  id: string;
  message: string;
  isBot: boolean;
  files?: FileInfo[];
  timestamp: Date;
  sources?: Array<{
    id: number;
    text: string;
    score: number;
    metadata: any;
  }>;
  confidence?: number;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      message: "Hello! I'm your Medical Q&A assistant powered by advanced AI. I can answer medical questions using a knowledge base of medical information. Ask me anything about diseases, symptoms, treatments, or medications!",
      isBot: true,
      timestamp: new Date(),
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message: string, files: FileInfo[]) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      message,
      isBot: false,
      files: files.length > 0 ? files : undefined,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Call backend API
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          top_k: 5,
          use_kg: true,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from server');
      }

      const data = await response.json();
      
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        message: data.answer,
        isBot: true,
        timestamp: new Date(),
        sources: data.sources,
        confidence: data.confidence,
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error calling API:', error);
      
      // Fallback response if API fails
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        message: "I apologize, but I'm having trouble connecting to my knowledge base. Please ensure the backend server is running at " + API_URL + ". You can start it with: `cd backend && python main.py`",
        isBot: true,
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <Card className="flex-1 flex flex-col m-4 mb-0">
        <CardHeader className="border-b">
          <CardTitle className="flex items-center gap-2">
            <Stethoscope className="w-5 h-5" />
            Medical QA
            <Badge variant="secondary" className="ml-auto">
              {messages.length} messages
            </Badge>
          </CardTitle>
        </CardHeader>
        
        <CardContent className="flex-1 p-0 flex flex-col">
          <ScrollArea className="flex-1 p-4">
            {messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                message={msg.message}
                isBot={msg.isBot}
                files={msg.files}
                timestamp={msg.timestamp}
                sources={msg.sources}
                confidence={msg.confidence}
              />
            ))}
            
            {isTyping && (
              <div className="flex justify-start mb-4">
                <div className="max-w-[70%]">
                  <Card className="p-3 bg-muted">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                      <span className="text-sm text-muted-foreground">Bot is typing...</span>
                    </div>
                  </Card>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </ScrollArea>
          
          <ChatInput 
            onSendMessage={handleSendMessage}
            disabled={isTyping}
          />
        </CardContent>
      </Card>
    </div>
  );
}
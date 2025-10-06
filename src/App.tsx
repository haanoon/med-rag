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
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      message: "Hello! I'm your Medical Q&A assistant. I can help answer medical questions and analyze medical documents, lab results, and images. Please upload your medical files or ask any health-related questions you have.",
      isBot: true,
      timestamp: new Date(),
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateBotResponse = (userMessage: string, files: FileInfo[]) => {
    // Medical-focused bot responses based on content
    if (files.length > 0) {
      const fileTypes = files.map(f => f.type);
      const hasImages = fileTypes.some(type => type.startsWith('image/'));
      const hasDocuments = fileTypes.some(type => type.includes('text') || type.includes('document'));
      
      if (hasImages && hasDocuments) {
        return "I can see you've uploaded both medical images and documents. I can help analyze lab results, medical reports, X-rays, or other medical documentation. What specific questions do you have about these files?";
      } else if (hasImages) {
        return "Thanks for sharing the medical image(s)! I can help analyze X-rays, scans, lab charts, or other medical visuals. What would you like to know about these images?";
      } else if (hasDocuments) {
        return "I've received your medical document(s). I can help interpret lab results, medical reports, discharge summaries, or other medical documentation. What specific questions do you have?";
      } else {
        return `I see you've uploaded ${files.length} medical file(s). I'll help analyze them from a medical perspective. What questions do you have?`;
      }
    }

    // Medical text-based responses
    const lowerMessage = userMessage.toLowerCase();
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
      return "Hello! I'm here to help with your medical questions. What can I assist you with today?";
    }
    if (lowerMessage.includes('help')) {
      return "I can help with medical questions, interpret lab results, explain medical terms, analyze medical documents, and provide health information. What medical topic would you like to discuss?";
    }
    if (lowerMessage.includes('file') || lowerMessage.includes('upload')) {
      return "You can upload medical documents, lab results, X-rays, or other medical files. I support images, PDFs, and text files. What medical information would you like me to review?";
    }
    if (lowerMessage.includes('thank')) {
      return "You're welcome! Remember, I provide information for educational purposes. Always consult with healthcare professionals for medical advice. Is there anything else I can help clarify?";
    }
    if (lowerMessage.includes('symptom') || lowerMessage.includes('pain') || lowerMessage.includes('fever')) {
      return "I can provide general information about symptoms, but please remember that for any concerning symptoms, you should consult with a healthcare provider. What specific information are you looking for?";
    }

    // Default medical responses
    const responses = [
      "That's a good medical question! Can you provide more details about your specific situation?",
      "I understand your concern. Can you tell me more about the medical context?",
      "Thanks for sharing that medical information. What specific aspect would you like me to explain?",
      "I'm here to help with medical questions! What particular health topic can I assist you with?",
      "That sounds like an important health question. Can you provide more details so I can give you better information?"
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

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

    // Simulate bot thinking time
    setTimeout(() => {
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        message: generateBotResponse(message, files),
        isBot: true,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000); // 1-3 seconds delay
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
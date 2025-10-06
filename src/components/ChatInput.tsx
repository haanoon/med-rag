import { useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { FileUpload } from "./FileUpload";
import { Send } from "lucide-react";

interface FileInfo {
  name: string;
  size: number;
  type: string;
  file: File;
  url?: string;
}

interface ChatInputProps {
  onSendMessage: (message: string, files: FileInfo[]) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<FileInfo[]>([]);

  const handleSend = () => {
    if (message.trim() || selectedFiles.length > 0) {
      onSendMessage(message.trim(), selectedFiles);
      setMessage("");
      setSelectedFiles([]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t bg-background p-4 space-y-3">
      <FileUpload 
        onFilesChange={setSelectedFiles}
        selectedFiles={selectedFiles}
      />
      
      <div className="flex gap-2">
        <Textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
          className="min-h-[60px] resize-none"
          disabled={disabled}
        />
        <Button 
          onClick={handleSend}
          disabled={disabled || (!message.trim() && selectedFiles.length === 0)}
          size="sm"
          className="self-end px-3"
        >
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
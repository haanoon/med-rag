import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { FileText, Image, File } from "lucide-react";

interface ChatMessageProps {
  message: string;
  isBot: boolean;
  files?: FileInfo[];
  timestamp: Date;
}

interface FileInfo {
  name: string;
  size: number;
  type: string;
  url?: string;
}

export function ChatMessage({ message, isBot, files, timestamp }: ChatMessageProps) {
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return <Image className="w-4 h-4" />;
    if (type.includes('text') || type.includes('document')) return <FileText className="w-4 h-4" />;
    return <File className="w-4 h-4" />;
  };

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}>
      <div className={`max-w-[70%] ${isBot ? 'order-1' : 'order-2'}`}>
        <Card className={`p-3 ${isBot ? 'bg-muted' : 'bg-primary text-primary-foreground'}`}>
          {message && <p className="mb-2 last:mb-0">{message}</p>}
          
          {files && files.length > 0 && (
            <div className="space-y-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center gap-2 p-2 rounded bg-background/10 border border-border/20">
                  {getFileIcon(file.type)}
                  <div className="flex-1 min-w-0">
                    <p className="truncate text-sm">{file.name}</p>
                    <p className="text-xs opacity-70">{formatFileSize(file.size)}</p>
                  </div>
                  {file.type.startsWith('image/') && file.url && (
                    <img 
                      src={file.url} 
                      alt={file.name}
                      className="w-12 h-12 object-cover rounded"
                    />
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
        
        <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mt-1`}>
          <Badge variant="secondary" className="text-xs">
            {isBot ? 'Bot' : 'You'} • {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Badge>
        </div>
      </div>
    </div>
  );
}
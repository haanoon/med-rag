import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { FileText, Image, File, BookOpen, TrendingUp } from "lucide-react";
import { useState } from "react";

interface ChatMessageProps {
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

interface FileInfo {
  name: string;
  size: number;
  type: string;
  url?: string;
}

export function ChatMessage({ message, isBot, files, timestamp, sources, confidence }: ChatMessageProps) {
  const [showSources, setShowSources] = useState(false);
  
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
          {message && <p className="mb-2 last:mb-0 whitespace-pre-wrap">{message}</p>}
          
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

          {/* Show confidence and sources for bot messages */}
          {isBot && confidence !== undefined && (
            <div className="mt-3 pt-3 border-t border-border/20">
              <div className="flex items-center gap-2 text-xs">
                <TrendingUp className="w-3 h-3" />
                <span>Confidence: {(confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          )}

          {isBot && sources && sources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-border/20">
              <button
                onClick={() => setShowSources(!showSources)}
                className="flex items-center gap-2 text-xs hover:underline"
              >
                <BookOpen className="w-3 h-3" />
                <span>{showSources ? 'Hide' : 'Show'} {sources.length} source{sources.length > 1 ? 's' : ''}</span>
              </button>
              
              {showSources && (
                <div className="mt-2 space-y-2 max-h-48 overflow-y-auto">
                  {sources.map((source, idx) => (
                    <div key={idx} className="p-2 rounded bg-background/20 border border-border/20 text-xs">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="outline" className="text-[10px] px-1 py-0">
                          Source {idx + 1}
                        </Badge>
                        <span className="text-[10px] opacity-70">
                          Score: {(source.score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="text-[11px] line-clamp-3">{source.text}</p>
                      {source.metadata?.category && (
                        <Badge variant="secondary" className="text-[9px] px-1 py-0 mt-1">
                          {source.metadata.category}
                        </Badge>
                      )}
                    </div>
                  ))}
                </div>
              )}
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
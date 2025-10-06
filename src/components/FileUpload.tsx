import { useState, useRef } from "react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Paperclip, X, FileText, Image, File } from "lucide-react";

interface FileInfo {
  name: string;
  size: number;
  type: string;
  file: File;
  url?: string;
}

interface FileUploadProps {
  onFilesChange: (files: FileInfo[]) => void;
  selectedFiles: FileInfo[];
}

export function FileUpload({ onFilesChange, selectedFiles }: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    
    const fileInfos: FileInfo[] = files.map(file => {
      const fileInfo: FileInfo = {
        name: file.name,
        size: file.size,
        type: file.type,
        file: file
      };
      
      // Create URL for images
      if (file.type.startsWith('image/')) {
        fileInfo.url = URL.createObjectURL(file);
      }
      
      return fileInfo;
    });
    
    onFilesChange([...selectedFiles, ...fileInfos]);
    
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    
    // Revoke URL for removed image
    const removedFile = selectedFiles[index];
    if (removedFile.url) {
      URL.revokeObjectURL(removedFile.url);
    }
    
    onFilesChange(newFiles);
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return <Image className="w-3 h-3" />;
    if (type.includes('text') || type.includes('document')) return <FileText className="w-3 h-3" />;
    return <File className="w-3 h-3" />;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-2">
      {selectedFiles.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedFiles.map((file, index) => (
            <Badge key={index} variant="secondary" className="flex items-center gap-1 pr-1">
              {getFileIcon(file.type)}
              <span className="truncate max-w-24">{file.name}</span>
              <span className="text-xs opacity-70">({formatFileSize(file.size)})</span>
              <Button
                variant="ghost"
                size="sm"
                className="w-4 h-4 p-0 hover:bg-destructive hover:text-destructive-foreground"
                onClick={() => removeFile(index)}
              >
                <X className="w-3 h-3" />
              </Button>
            </Badge>
          ))}
        </div>
      )}
      
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        multiple
        className="hidden"
        accept="image/*,.pdf,.doc,.docx,.txt,.json,.csv"
      />
      
      <Button
        variant="outline"
        size="sm"
        onClick={() => fileInputRef.current?.click()}
        className="gap-2"
      >
        <Paperclip className="w-4 h-4" />
        Attach Files
      </Button>
    </div>
  );
}
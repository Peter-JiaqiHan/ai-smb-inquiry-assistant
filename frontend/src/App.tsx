import { useState, useEffect, useRef } from 'react';
import {
  AppShell,
  Box,
  TextInput,
  Button,
  Group,
  Avatar,
  Text,
  Paper,
  Loader,
  ScrollArea,
  Stack,
} from '@mantine/core';
import { IconSend } from '@tabler/icons-react';

interface Message {
  sender: 'user' | 'ai';
  text: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'ai', text: '您好！我是新艺窗帘的 AI 客服，请问有什么可以帮助您？' },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const viewport = useRef<HTMLDivElement>(null);

  const scrollToBottom = () =>
    viewport.current!.scrollTo({ top: viewport.current!.scrollHeight, behavior: 'smooth' });

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage: Message = { sender: 'user', text: inputValue };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const aiMessage: Message = { sender: 'ai', text: data.response };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);
      const errorMessage: Message = { sender: 'ai', text: '抱歉，服务暂时出现问题，请稍后再试。' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppShell
      header={{ height: 60 }}
      footer={{ height: 70 }}
      padding="md"
    >
      <AppShell.Header
        style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
      >
        <Text fw={700} size="xl">新艺窗帘 AI 助手</Text>
      </AppShell.Header>

      <AppShell.Main>
        <ScrollArea h="100%" viewportRef={viewport}>
          <Stack gap="lg" p="md">
            {messages.map((msg, index) => {
              const isUser = msg.sender === 'user';
              return (
                <Box
                  key={index}
                  style={{
                    display: 'flex',
                    justifyContent: isUser ? 'flex-end' : 'flex-start',
                  }}
                >
                  <Group gap="sm" wrap="nowrap" align="flex-start">
                    {!isUser && <Avatar color="blue" radius="xl">AI</Avatar>}
                    <Paper
                      p="md"
                      shadow="sm"
                      radius="lg"
                      withBorder
                      style={{
                        backgroundColor: isUser ? 'var(--mantine-color-blue-6)' : 'var(--mantine-color-body)',
                        color: isUser ? 'white' : 'var(--mantine-color-text)',
                        maxWidth: '80%',
                      }}
                    >
                      <Text size="sm">{msg.text}</Text>
                    </Paper>
                    {isUser && <Avatar color="gray" radius="xl">U</Avatar>}
                  </Group>
                </Box>
              );
            })}
            {isLoading && (
              <Group gap="sm" wrap="nowrap" align="flex-start">
                 <Avatar color="blue" radius="xl">AI</Avatar>
                 <Paper p="md" shadow="sm" radius="lg" withBorder>
                    <Loader size="sm" type="dots" />
                 </Paper>
              </Group>
            )}
          </Stack>
        </ScrollArea>
      </AppShell.Main>

      <AppShell.Footer p="md">
        <Box component="form" onSubmit={handleSendMessage} style={{ display: 'flex', gap: '8px' }}>
          <TextInput
            placeholder="请输入您的问题..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            radius="xl"
            style={{ flex: 1 }}
            size="md"
          />
          <Button 
            type="submit" 
            disabled={isLoading || !inputValue.trim()}
            radius="xl"
            size="md"
            aria-label="发送消息"
          >
            <IconSend size={18} />
          </Button>
        </Box>
      </AppShell.Footer>
    </AppShell>
  );
}

export default App;

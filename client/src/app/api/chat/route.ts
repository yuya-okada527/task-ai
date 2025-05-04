import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";
import { experimental_createMCPClient as createMCPClient } from "ai"; 

export async function POST(req: Request) {
    const mcpClient = await createMCPClient({
        transport: {
            type: "sse",
            url: "http://localhost:8000/sse",
        },
    });

    const { messages } = await req.json();

    const tools = await mcpClient.tools();

    const result = streamText({
        model: openai.chat("gpt-4.1-nano"),
        messages,
        tools,
        onFinish: () => {
            mcpClient.close();
        }
    });
    return result.toDataStreamResponse();
}
